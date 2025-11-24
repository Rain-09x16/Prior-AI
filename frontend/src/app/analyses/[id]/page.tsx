'use client';

import { useEffect, useState } from 'react';
import { useParams, useRouter } from 'next/navigation';
import { useAnalysisStore } from '@/stores/analysisStore';
import { PatentCard } from '@/components/PatentCard';
import { PatentabilityAlert } from '@/components/PatentabilityAlert';
import {
  ArrowLeft,
  Download,
  Loader2,
  FileText,
  AlertCircle,
  CheckCircle2,
  XCircle,
  TrendingUp,
} from 'lucide-react';
import {
  formatDateTime,
  getRecommendationColor,
  getNoveltyScoreColor,
} from '@/lib/utils';

export default function AnalysisDetailsPage() {
  const params = useParams();
  const router = useRouter();
  const id = params.id as string;

  const {
    currentAnalysis,
    isLoading,
    error,
    fetchAnalysis,
    pollAnalysis,
    generateReport,
  } = useAnalysisStore();

  const [isGeneratingReport, setIsGeneratingReport] = useState(false);

  useEffect(() => {
    if (id) {
      fetchAnalysis(id);
    }
  }, [id, fetchAnalysis]);

  useEffect(() => {
    if (currentAnalysis?.status === 'processing') {
      pollAnalysis(id);
    }
  }, [currentAnalysis?.status, id, pollAnalysis]);

  const handleGenerateReport = async () => {
    setIsGeneratingReport(true);
    try {
      const reportUrl = await generateReport(id);
      window.open(reportUrl, '_blank');
    } catch (error) {
      console.error('Report generation failed:', error);
    } finally {
      setIsGeneratingReport(false);
    }
  };

  if (isLoading && !currentAnalysis) {
    return (
      <div className="container mx-auto px-4 py-16">
        <div className="flex items-center justify-center">
          <Loader2 className="h-8 w-8 animate-spin text-blue-600" />
        </div>
      </div>
    );
  }

  if (error && !currentAnalysis) {
    return (
      <div className="container mx-auto px-4 py-16">
        <div className="max-w-2xl mx-auto text-center">
          <AlertCircle className="h-16 w-16 text-red-600 mx-auto mb-4" />
          <h2 className="text-2xl font-bold text-gray-900 mb-2">Error Loading Analysis</h2>
          <p className="text-gray-600 mb-6">{error}</p>
          <button
            onClick={() => router.push('/analyses')}
            className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
          >
            Back to Analyses
          </button>
        </div>
      </div>
    );
  }

  if (!currentAnalysis) {
    return (
      <div className="container mx-auto px-4 py-16">
        <div className="text-center">
          <p className="text-gray-600">Analysis not found</p>
        </div>
      </div>
    );
  }

  const { status, title, disclosure, extractedClaims, patents, noveltyScore, recommendation, reasoning } = currentAnalysis;

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="container mx-auto px-4 py-8">
      {/* Back button */}
      <button
        onClick={() => router.push('/analyses')}
        className="flex items-center space-x-2 text-gray-600 hover:text-gray-900 mb-6"
      >
        <ArrowLeft className="h-4 w-4" />
        <span>Back to all analyses</span>
      </button>

      {/* Header */}
      <div className="bg-white rounded-lg border border-gray-200 p-6 mb-6">
        <div className="flex items-start justify-between mb-4">
          <div className="flex-1">
            <h1 className="text-3xl font-bold text-gray-900 mb-2">{title}</h1>
            <div className="flex items-center space-x-4 text-sm text-gray-600">
              <span className="flex items-center space-x-1">
                <FileText className="h-4 w-4" />
                <span>{disclosure.filename}</span>
              </span>
              <span>{formatDateTime(disclosure.uploadedAt)}</span>
            </div>
          </div>

          {status === 'completed' && (
            <button
              onClick={handleGenerateReport}
              disabled={isGeneratingReport}
              className="flex items-center space-x-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:bg-gray-400"
            >
              {isGeneratingReport ? (
                <Loader2 className="h-4 w-4 animate-spin" />
              ) : (
                <Download className="h-4 w-4" />
              )}
              <span>Download Report</span>
            </button>
          )}
        </div>

        {/* Status indicator */}
        {status === 'processing' && (
          <div className="flex items-center space-x-3 p-4 bg-blue-50 rounded-lg border border-blue-200">
            <Loader2 className="h-5 w-5 animate-spin text-blue-600" />
            <div>
              <p className="font-medium text-blue-900">Analysis in progress...</p>
              <p className="text-sm text-blue-700">
                This may take a few minutes. The page will update automatically.
              </p>
            </div>
          </div>
        )}

        {status === 'failed' && (
          <div className="flex items-center space-x-3 p-4 bg-red-50 rounded-lg border border-red-200">
            <XCircle className="h-5 w-5 text-red-600" />
            <div>
              <p className="font-medium text-red-900">Analysis failed</p>
              <p className="text-sm text-red-700">{reasoning || 'An error occurred during analysis'}</p>
            </div>
          </div>
        )}
      </div>

      {/* Results (if completed) */}
      {status === 'completed' && (
        <>
          {/* NEW: Patentability Assessment Alert (v2.1) */}
          {currentAnalysis.patentabilityAssessment && (
            <PatentabilityAlert
              assessment={currentAnalysis.patentabilityAssessment}
              onUploadNew={() => router.push('/')}
            />
          )}

          {/* Overall Assessment */}
          <div className="bg-white rounded-lg border border-gray-200 p-6 mb-6">
            <h2 className="text-2xl font-bold text-gray-900 mb-6 flex items-center space-x-2">
              <TrendingUp className="h-6 w-6 text-blue-600" />
              <span>Overall Assessment</span>
            </h2>

            <div className="grid md:grid-cols-2 gap-6 mb-6">
              {/* Novelty Score */}
              <div className="bg-gradient-to-br from-blue-50 to-blue-100 p-6 rounded-lg border border-blue-200">
                <p className="text-sm text-blue-800 mb-2 font-medium">Novelty Score</p>
                <div className="flex items-baseline space-x-2">
                  <span className={`text-5xl font-bold ${getNoveltyScoreColor(noveltyScore || 0)}`}>
                    {noveltyScore?.toFixed(1)}
                  </span>
                  <span className="text-2xl text-gray-600">/100</span>
                </div>
                <div className="mt-3 h-2 bg-white rounded-full overflow-hidden">
                  <div
                    className="h-full bg-blue-600 rounded-full transition-all"
                    style={{ width: `${noveltyScore}%` }}
                  />
                </div>
              </div>

              {/* Recommendation */}
              <div className="bg-gradient-to-br from-gray-50 to-gray-100 p-6 rounded-lg border border-gray-200">
                <p className="text-sm text-gray-800 mb-2 font-medium">Recommendation</p>
                <span
                  className={`inline-block px-4 py-2 text-2xl font-bold rounded-lg border-2 ${getRecommendationColor(
                    recommendation || ''
                  )}`}
                >
                  {recommendation?.toUpperCase()}
                </span>
              </div>
            </div>

            {/* Reasoning */}
            {reasoning && (
              <div className="bg-gray-50 p-4 rounded-lg border border-gray-200">
                <p className="text-gray-800 leading-relaxed">{reasoning}</p>
              </div>
            )}
          </div>

          {/* Extracted Claims */}
          {extractedClaims && (
            <div className="bg-white rounded-lg border border-gray-200 p-6 mb-6">
              <h2 className="text-2xl font-bold text-gray-900 mb-6">Extracted Claims</h2>

              <div className="space-y-6">
                {/* Background */}
                {extractedClaims.background && (
                  <div>
                    <h3 className="text-lg font-semibold text-gray-900 mb-2">Background</h3>
                    <p className="text-gray-700 leading-relaxed">{extractedClaims.background}</p>
                  </div>
                )}

                {/* Innovations */}
                {extractedClaims.innovations && extractedClaims.innovations.length > 0 && (
                  <div>
                    <h3 className="text-lg font-semibold text-gray-900 mb-3">Key Innovations</h3>
                    <ul className="space-y-2">
                      {extractedClaims.innovations.map((innovation, idx) => (
                        <li key={idx} className="flex items-start space-x-2">
                          <CheckCircle2 className="h-5 w-5 text-green-600 flex-shrink-0 mt-0.5" />
                          <span className="text-gray-700">{innovation}</span>
                        </li>
                      ))}
                    </ul>
                  </div>
                )}

                {/* Keywords */}
                {extractedClaims.keywords && extractedClaims.keywords.length > 0 && (
                  <div>
                    <h3 className="text-lg font-semibold text-gray-900 mb-3">Keywords</h3>
                    <div className="flex flex-wrap gap-2">
                      {extractedClaims.keywords.map((keyword, idx) => (
                        <span
                          key={idx}
                          className="px-3 py-1 bg-blue-100 text-blue-800 rounded-full text-sm font-medium"
                        >
                          {keyword}
                        </span>
                      ))}
                    </div>
                  </div>
                )}

                {/* IPC Classifications */}
                {extractedClaims.ipcClassifications && extractedClaims.ipcClassifications.length > 0 && (
                  <div>
                    <h3 className="text-lg font-semibold text-gray-900 mb-3">IPC Classifications</h3>
                    <div className="flex flex-wrap gap-2">
                      {extractedClaims.ipcClassifications.map((ipc, idx) => (
                        <span
                          key={idx}
                          className="px-3 py-1 bg-purple-100 text-purple-800 rounded text-sm font-mono font-medium"
                        >
                          {ipc}
                        </span>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            </div>
          )}

          {/* Similar Patents (only show if patentable or no assessment) */}
          {(!currentAnalysis.patentabilityAssessment ||
            currentAnalysis.patentabilityAssessment.isPatentable) &&
           patents && patents.length > 0 && (
            <div className="bg-white rounded-lg border border-gray-200 p-6">
              <div className="mb-6">
                <h2 className="text-2xl font-bold text-gray-900 mb-2">Similar Patents</h2>
                <p className="text-gray-600">
                  Found {patents.length} similar patent{patents.length !== 1 ? 's' : ''}, sorted by similarity score
                </p>
              </div>

              <div className="space-y-4">
                {patents.map((patent, idx) => (
                  <PatentCard key={patent.id} patent={patent} rank={idx + 1} />
                ))}
              </div>
            </div>
          )}

          {/* Show message if prior art search was skipped */}
          {currentAnalysis.patentabilityAssessment &&
           !currentAnalysis.patentabilityAssessment.isPatentable && (
            <div className="bg-gray-50 rounded-lg border-2 border-gray-200 p-6 text-center">
              <AlertCircle className="h-12 w-12 text-gray-400 mx-auto mb-3" />
              <h3 className="text-lg font-semibold text-gray-900 mb-2">
                Prior Art Search Skipped
              </h3>
              <p className="text-gray-600">
                The expensive prior art search was not performed because the disclosure
                was determined to be not patentable during the initial assessment.
                This saved approximately $500-$1,000 in search costs.
              </p>
            </div>
          )}
        </>
      )}
      </div>
    </div>
  );
}
