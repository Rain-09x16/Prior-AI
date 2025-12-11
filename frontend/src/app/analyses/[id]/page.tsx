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
  Tag,
  Lightbulb,
  BookOpen,
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
      <div className="min-h-screen bg-background flex items-center justify-center">
        <div className="text-center">
          <div className="processing-ring w-12 h-12 mx-auto mb-4" />
          <p className="text-foreground-muted">Loading analysis...</p>
        </div>
      </div>
    );
  }

  if (error && !currentAnalysis) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center">
        <div className="max-w-md mx-auto text-center p-8">
          <div className="w-16 h-16 rounded-2xl bg-error/10 flex items-center justify-center mx-auto mb-4">
            <AlertCircle className="h-8 w-8 text-error" />
          </div>
          <h2 className="text-2xl font-bold text-foreground mb-2">Error Loading Analysis</h2>
          <p className="text-foreground-muted mb-6">{error}</p>
          <button
            onClick={() => router.push('/analyses')}
            className="btn btn-primary"
          >
            Back to Analyses
          </button>
        </div>
      </div>
    );
  }

  if (!currentAnalysis) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center">
        <div className="text-center">
          <p className="text-foreground-muted">Analysis not found</p>
        </div>
      </div>
    );
  }

  const { status, title, disclosure, extractedClaims, patents, noveltyScore, recommendation, reasoning } = currentAnalysis;

  return (
    <div className="min-h-screen bg-background">
      {/* Hero gradient background */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <div className="absolute top-0 left-1/4 w-96 h-96 bg-primary/20 rounded-full blur-3xl" />
        <div className="absolute top-20 right-1/4 w-80 h-80 bg-accent/20 rounded-full blur-3xl" />
      </div>

      <div className="container mx-auto px-4 py-8 relative">
        {/* Back button */}
        <button
          onClick={() => router.push('/analyses')}
          className="flex items-center gap-2 text-foreground-muted hover:text-foreground transition-colors mb-6 group"
        >
          <ArrowLeft className="h-4 w-4 group-hover:-translate-x-1 transition-transform" />
          <span>Back to all analyses</span>
        </button>

        {/* Header */}
        <div className="card p-6 mb-6">
          <div className="flex items-start justify-between mb-4">
            <div className="flex-1">
              <div className="flex items-center gap-3 mb-3">
                <div className="w-12 h-12 rounded-2xl bg-gradient-to-br from-primary to-accent flex items-center justify-center shadow-lg shadow-primary/25">
                  <FileText className="w-6 h-6 text-white" />
                </div>
                <h1 className="text-3xl font-bold text-foreground">{title}</h1>
              </div>
              <div className="flex items-center gap-4 text-sm text-foreground-muted">
                <span className="flex items-center gap-1">
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
                className="btn btn-gradient"
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
            <div className="flex items-center gap-3 p-4 rounded-xl bg-info/10 border border-info/30">
              <div className="processing-ring w-5 h-5" />
              <div>
                <p className="font-medium text-info">Analysis in progress...</p>
                <p className="text-sm text-foreground-muted">
                  This may take a few minutes. The page will update automatically.
                </p>
              </div>
            </div>
          )}

          {status === 'failed' && (
            <div className="flex items-center gap-3 p-4 rounded-xl bg-error/10 border border-error/30">
              <XCircle className="h-5 w-5 text-error" />
              <div>
                <p className="font-medium text-error">Analysis failed</p>
                <p className="text-sm text-foreground-muted">{reasoning || 'An error occurred during analysis'}</p>
              </div>
            </div>
          )}
        </div>

        {/* Results (if completed) */}
        {status === 'completed' && (
          <>
            {/* Patentability Assessment Alert */}
            {currentAnalysis.patentabilityAssessment && (
              <PatentabilityAlert
                assessment={currentAnalysis.patentabilityAssessment}
                onUploadNew={() => router.push('/')}
              />
            )}

            {/* Overall Assessment */}
            <div className="card p-6 mb-6">
              <h2 className="text-2xl font-bold text-foreground mb-6 flex items-center gap-3">
                <div className="w-10 h-10 rounded-xl bg-primary/10 flex items-center justify-center">
                  <TrendingUp className="h-5 w-5 text-primary" />
                </div>
                <span>Overall Assessment</span>
              </h2>

              <div className="grid md:grid-cols-2 gap-6 mb-6">
                {/* Novelty Score */}
                <div className="p-6 rounded-2xl bg-gradient-to-br from-primary/10 to-accent/10 border border-primary/20">
                  <p className="text-sm text-foreground-muted mb-2 font-medium">Novelty Score</p>
                  <div className="flex items-baseline gap-2">
                    <span className={`text-5xl font-bold ${getNoveltyScoreColor(noveltyScore || 0)}`}>
                      {noveltyScore?.toFixed(1)}
                    </span>
                    <span className="text-2xl text-foreground-muted">/100</span>
                  </div>
                  <div className="mt-4 h-2 bg-background-tertiary rounded-full overflow-hidden">
                    <div
                      className="h-full bg-gradient-to-r from-primary to-accent rounded-full transition-all"
                      style={{ width: `${noveltyScore}%` }}
                    />
                  </div>
                </div>

                {/* Recommendation */}
                <div className="p-6 rounded-2xl bg-background-tertiary border border-border">
                  <p className="text-sm text-foreground-muted mb-2 font-medium">Recommendation</p>
                  <span
                    className={`inline-block px-4 py-2 text-xl font-bold rounded-xl ${getRecommendationColor(
                      recommendation || ''
                    )}`}
                  >
                    {recommendation?.toUpperCase()}
                  </span>
                </div>
              </div>

              {/* Reasoning */}
              {reasoning && (
                <div className="p-4 rounded-xl bg-background-tertiary border border-border">
                  <p className="text-foreground-muted leading-relaxed">{reasoning}</p>
                </div>
              )}
            </div>

            {/* Extracted Claims */}
            {extractedClaims && (
              <div className="card p-6 mb-6">
                <h2 className="text-2xl font-bold text-foreground mb-6 flex items-center gap-3">
                  <div className="w-10 h-10 rounded-xl bg-accent/10 flex items-center justify-center">
                    <BookOpen className="h-5 w-5 text-accent" />
                  </div>
                  <span>Extracted Claims</span>
                </h2>

                <div className="space-y-6">
                  {/* Background */}
                  {extractedClaims.background && (
                    <div>
                      <h3 className="text-lg font-semibold text-foreground mb-2">Background</h3>
                      <p className="text-foreground-muted leading-relaxed">{extractedClaims.background}</p>
                    </div>
                  )}

                  {/* Innovations */}
                  {extractedClaims.innovations && extractedClaims.innovations.length > 0 && (
                    <div>
                      <h3 className="text-lg font-semibold text-foreground mb-3 flex items-center gap-2">
                        <Lightbulb className="h-5 w-5 text-warning" />
                        Key Innovations
                      </h3>
                      <ul className="space-y-2">
                        {extractedClaims.innovations.map((innovation, idx) => (
                          <li key={idx} className="flex items-start gap-3 p-3 rounded-lg bg-background-tertiary">
                            <CheckCircle2 className="h-5 w-5 text-success flex-shrink-0 mt-0.5" />
                            <span className="text-foreground-muted">{innovation}</span>
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}

                  {/* Keywords */}
                  {extractedClaims.keywords && extractedClaims.keywords.length > 0 && (
                    <div>
                      <h3 className="text-lg font-semibold text-foreground mb-3 flex items-center gap-2">
                        <Tag className="h-5 w-5 text-primary" />
                        Keywords
                      </h3>
                      <div className="flex flex-wrap gap-2">
                        {extractedClaims.keywords.map((keyword, idx) => (
                          <span key={idx} className="tag tag-primary">
                            {keyword}
                          </span>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* IPC Classifications */}
                  {extractedClaims.ipcClassifications && extractedClaims.ipcClassifications.length > 0 && (
                    <div>
                      <h3 className="text-lg font-semibold text-foreground mb-3">IPC Classifications</h3>
                      <div className="flex flex-wrap gap-2">
                        {extractedClaims.ipcClassifications.map((ipc, idx) => (
                          <span key={idx} className="badge badge-neutral badge-pill font-mono text-sm">
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
              <div className="card p-6">
                <div className="mb-6">
                  <h2 className="text-2xl font-bold text-foreground mb-2">Similar Patents</h2>
                  <p className="text-foreground-muted">
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
              <div className="glass-card p-8 text-center">
                <div className="w-16 h-16 rounded-2xl bg-foreground-muted/10 flex items-center justify-center mx-auto mb-4">
                  <AlertCircle className="h-8 w-8 text-foreground-muted" />
                </div>
                <h3 className="text-xl font-semibold text-foreground mb-2">
                  Prior Art Search Skipped
                </h3>
                <p className="text-foreground-muted max-w-md mx-auto">
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
