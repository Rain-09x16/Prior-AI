'use client';

import Link from 'next/link';
import { FileText, Trash2, Download, Eye, CheckCircle2, AlertTriangle } from 'lucide-react';
import { formatRelativeTime, getStatusColor, getRecommendationColor } from '@/lib/utils';
import type { Analysis } from '@/lib/types';

interface AnalysisCardProps {
  analysis: Analysis;
  onDelete?: (id: string) => void;
}

export function AnalysisCard({ analysis, onDelete }: AnalysisCardProps) {
  const handleDelete = (e: React.MouseEvent) => {
    e.preventDefault();
    if (onDelete && confirm('Are you sure you want to delete this analysis?')) {
      onDelete(analysis.id);
    }
  };

  return (
    <Link href={`/analyses/${analysis.id}`}>
      <div className="block p-6 bg-white border-2 border-gray-200 rounded-xl hover:border-blue-300 hover:shadow-xl transition-all cursor-pointer animate-fade-in transform hover:-translate-y-1">
        {/* Header */}
        <div className="flex items-start justify-between mb-4">
          <div className="flex-1">
            <div className="flex items-center space-x-3 mb-2">
              <FileText className="h-5 w-5 text-blue-600" />
              <h3 className="text-lg font-semibold text-gray-900 line-clamp-1">
                {analysis.title}
              </h3>
            </div>
            <p className="text-sm text-gray-500">
              {analysis.disclosure.filename} • {formatRelativeTime(analysis.createdAt)}
            </p>
          </div>

          {/* Status badge */}
          <span
            className={`px-3 py-1.5 text-xs font-semibold rounded-full border-2 ${getStatusColor(
              analysis.status
            )}`}
          >
            {analysis.status.charAt(0).toUpperCase() + analysis.status.slice(1)}
          </span>
        </div>

        {/* NEW: Patentability Badge (v2.1) */}
        {analysis.status === 'completed' && analysis.patentabilityAssessment && (
          <div className="mb-3">
            {analysis.patentabilityAssessment.isPatentable ? (
              <div className="flex items-center space-x-2 px-4 py-2.5 bg-green-50 border-2 border-green-300 rounded-lg">
                <CheckCircle2 className="h-5 w-5 text-green-600" />
                <span className="text-sm font-semibold text-green-900">
                  Patentable ({analysis.patentabilityAssessment.confidence.toFixed(0)}% confidence)
                </span>
              </div>
            ) : (
              <div className="flex items-center space-x-2 px-4 py-2.5 bg-red-50 border-2 border-red-300 rounded-lg">
                <AlertTriangle className="h-5 w-5 text-red-600" />
                <span className="text-sm font-semibold text-red-900">
                  Publishable Only ({analysis.patentabilityAssessment.confidence.toFixed(0)}% confidence)
                </span>
              </div>
            )}
          </div>
        )}

        {/* Results (if completed) */}
        {analysis.status === 'completed' && (
          <div className="space-y-3">
            <div className="grid grid-cols-2 gap-4">
              {/* Novelty Score */}
              {analysis.noveltyScore !== undefined && (
                <div className="bg-gradient-to-br from-blue-50 to-blue-100 p-4 rounded-lg border border-blue-200">
                  <p className="text-xs font-medium text-gray-700 mb-1">Novelty Score</p>
                  <p className="text-3xl font-bold text-blue-600">
                    {analysis.noveltyScore.toFixed(1)}
                    <span className="text-base font-normal text-gray-500">/100</span>
                  </p>
                </div>
              )}

              {/* Recommendation */}
              {analysis.recommendation && (
                <div className="bg-gray-50 p-4 rounded-lg border border-gray-200">
                  <p className="text-xs font-medium text-gray-700 mb-2">Recommendation</p>
                  <span
                    className={`inline-block px-3 py-1.5 text-sm font-bold rounded-md border-2 ${getRecommendationColor(
                      analysis.recommendation
                    )}`}
                  >
                    {analysis.recommendation.toUpperCase()}
                  </span>
                </div>
              )}
            </div>

            {/* Patents found */}
            {analysis.patents && analysis.patents.length > 0 && (
              <p className="text-sm text-gray-600">
                Found {analysis.patents.length} similar patent{analysis.patents.length !== 1 ? 's' : ''}
              </p>
            )}
          </div>
        )}

        {/* Processing status */}
        {analysis.status === 'processing' && (
          <div className="flex items-center space-x-2 text-blue-600">
            <div className="animate-spin h-4 w-4 border-2 border-blue-600 border-t-transparent rounded-full" />
            <span className="text-sm">Analyzing disclosure...</span>
          </div>
        )}

        {/* Failed status */}
        {analysis.status === 'failed' && (
          <div className="text-red-600 text-sm">
            Analysis failed. Please try again.
          </div>
        )}

        {/* Actions */}
        <div className="mt-4 pt-4 border-t border-gray-200 flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <Eye className="h-4 w-4 text-gray-400" />
            <span className="text-sm text-gray-600">View details</span>
          </div>

          {onDelete && (
            <button
              onClick={handleDelete}
              className="p-2 text-red-600 hover:bg-red-50 rounded-lg transition-colors"
              title="Delete analysis"
            >
              <Trash2 className="h-4 w-4" />
            </button>
          )}
        </div>
      </div>
    </Link>
  );
}
