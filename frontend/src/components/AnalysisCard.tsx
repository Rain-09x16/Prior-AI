'use client';

import Link from 'next/link';
import { FileText, Trash2, Eye, CheckCircle2, AlertTriangle, Loader2, XCircle } from 'lucide-react';
import { formatRelativeTime } from '@/lib/utils';
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

  const getStatusBadge = () => {
    switch (analysis.status) {
      case 'processing':
        return (
          <span className="badge badge-info badge-pill">
            <Loader2 className="w-3 h-3 animate-spin" />
            Processing
          </span>
        );
      case 'completed':
        return (
          <span className="badge badge-success badge-pill">
            <CheckCircle2 className="w-3 h-3" />
            Completed
          </span>
        );
      case 'failed':
        return (
          <span className="badge badge-error badge-pill">
            <XCircle className="w-3 h-3" />
            Failed
          </span>
        );
      default:
        return null;
    }
  };

  return (
    <Link href={`/analyses/${analysis.id}`}>
      <div className="card-interactive p-6 h-full animate-fade-in group">
        {/* Header */}
        <div className="flex items-start justify-between mb-4">
          <div className="flex-1 min-w-0">
            <div className="flex items-center gap-3 mb-2">
              <div className="w-10 h-10 rounded-xl bg-primary/10 flex items-center justify-center shrink-0">
                <FileText className="w-5 h-5 text-primary" />
              </div>
              <h3 className="text-lg font-semibold text-foreground line-clamp-1 group-hover:text-primary transition-colors">
                {analysis.title}
              </h3>
            </div>
            <p className="text-sm text-foreground-muted pl-13">
              {analysis.disclosure.filename} • {formatRelativeTime(analysis.createdAt)}
            </p>
          </div>
          {getStatusBadge()}
        </div>

        {/* Patentability Badge (v2.1) */}
        {analysis.status === 'completed' && analysis.patentabilityAssessment && (
          <div className="mb-4">
            {analysis.patentabilityAssessment.isPatentable ? (
              <div className="flex items-center gap-2 px-4 py-3 rounded-xl bg-success/10 border border-success/30">
                <CheckCircle2 className="w-5 h-5 text-success" />
                <span className="text-sm font-semibold text-success">
                  Patentable ({analysis.patentabilityAssessment.confidence.toFixed(0)}% confidence)
                </span>
              </div>
            ) : (
              <div className="flex items-center gap-2 px-4 py-3 rounded-xl bg-error/10 border border-error/30">
                <AlertTriangle className="w-5 h-5 text-error" />
                <span className="text-sm font-semibold text-error">
                  Publishable Only ({analysis.patentabilityAssessment.confidence.toFixed(0)}% confidence)
                </span>
              </div>
            )}
          </div>
        )}

        {/* Results (if completed) */}
        {analysis.status === 'completed' && (
          <div className="space-y-4">
            <div className="grid grid-cols-2 gap-4">
              {/* Novelty Score */}
              {analysis.noveltyScore !== undefined && (
                <div className="p-4 rounded-xl bg-background-tertiary border border-border">
                  <p className="text-xs font-medium text-foreground-muted mb-1">Novelty Score</p>
                  <p className="text-2xl font-bold text-primary">
                    {analysis.noveltyScore.toFixed(1)}
                    <span className="text-sm font-normal text-foreground-muted">/100</span>
                  </p>
                </div>
              )}

              {/* Recommendation */}
              {analysis.recommendation && (
                <div className="p-4 rounded-xl bg-background-tertiary border border-border">
                  <p className="text-xs font-medium text-foreground-muted mb-2">Recommendation</p>
                  <span className={`badge badge-pill ${
                    analysis.recommendation === 'pursue' ? 'badge-success' :
                    analysis.recommendation === 'reconsider' ? 'badge-warning' :
                    'badge-error'
                  }`}>
                    {analysis.recommendation.toUpperCase()}
                  </span>
                </div>
              )}
            </div>

            {/* Patents found */}
            {analysis.patents && analysis.patents.length > 0 && (
              <p className="text-sm text-foreground-muted">
                Found {analysis.patents.length} similar patent{analysis.patents.length !== 1 ? 's' : ''}
              </p>
            )}
          </div>
        )}

        {/* Processing status */}
        {analysis.status === 'processing' && (
          <div className="flex items-center gap-3 p-4 rounded-xl bg-info/10 border border-info/30">
            <div className="processing-ring w-5 h-5" />
            <span className="text-sm text-info font-medium">Analyzing disclosure...</span>
          </div>
        )}

        {/* Failed status */}
        {analysis.status === 'failed' && (
          <div className="p-4 rounded-xl bg-error/10 border border-error/30">
            <p className="text-sm text-error font-medium">
              Analysis failed. Please try again.
            </p>
          </div>
        )}

        {/* Actions */}
        <div className="mt-4 pt-4 border-t border-border flex items-center justify-between">
          <div className="flex items-center gap-2 text-foreground-muted group-hover:text-primary transition-colors">
            <Eye className="w-4 h-4" />
            <span className="text-sm font-medium">View details</span>
          </div>

          {onDelete && (
            <button
              onClick={handleDelete}
              className="btn btn-danger btn-sm opacity-0 group-hover:opacity-100 transition-opacity"
              title="Delete analysis"
            >
              <Trash2 className="w-4 h-4" />
            </button>
          )}
        </div>
      </div>
    </Link>
  );
}
