'use client';

import { AlertCircle, CheckCircle2, AlertTriangle, Lightbulb, Sparkles } from 'lucide-react';
import type { PatentabilityAssessment } from '@/lib/types';

interface PatentabilityAlertProps {
  assessment: PatentabilityAssessment;
  onContinue?: () => void;
  onUploadNew?: () => void;
}

export function PatentabilityAlert({ assessment, onContinue, onUploadNew }: PatentabilityAlertProps) {
  const { isPatentable, confidence, missingElements, recommendations } = assessment;

  // Determine alert style based on patentability and confidence
  const getAlertStyle = () => {
    if (!isPatentable) {
      return {
        containerClass: 'bg-error/10 border-error/30',
        iconClass: 'text-error',
        titleClass: 'text-error',
        textClass: 'text-foreground-muted',
        icon: AlertCircle,
        title: 'Not Patentable',
        message: 'This disclosure appears to be publishable research but lacks key elements required for patent protection.',
      };
    }

    if (confidence < 60) {
      return {
        containerClass: 'bg-error/10 border-error/30',
        iconClass: 'text-error',
        titleClass: 'text-error',
        textClass: 'text-foreground-muted',
        icon: AlertCircle,
        title: 'Low Patentability',
        message: 'This disclosure has low patentability. Consider significant revisions before filing.',
      };
    }

    if (confidence < 80) {
      return {
        containerClass: 'bg-warning/10 border-warning/30',
        iconClass: 'text-warning',
        titleClass: 'text-warning',
        textClass: 'text-foreground-muted',
        icon: AlertTriangle,
        title: 'Borderline Patentability',
        message: 'This disclosure may be patentable but could benefit from improvements.',
      };
    }

    return {
      containerClass: 'bg-success/10 border-success/30',
      iconClass: 'text-success',
      titleClass: 'text-success',
      textClass: 'text-foreground-muted',
      icon: CheckCircle2,
      title: 'Likely Patentable',
      message: 'This disclosure appears to have strong patentability. Proceeding with prior art search.',
    };
  };

  const style = getAlertStyle();
  const Icon = style.icon;

  return (
    <div className={`rounded-2xl border-2 p-6 mb-6 ${style.containerClass} animate-fade-in`}>
      {/* Header */}
      <div className="flex items-start gap-4 mb-4">
        <div className={`w-12 h-12 rounded-xl flex items-center justify-center ${style.containerClass}`}>
          <Icon className={`h-6 w-6 ${style.iconClass}`} />
        </div>
        <div className="flex-1">
          <h3 className={`text-xl font-bold ${style.titleClass} mb-1`}>
            {style.title}
          </h3>
          <p className={`text-sm ${style.textClass}`}>
            {style.message}
          </p>
        </div>
        <div className={`px-4 py-3 rounded-xl border ${style.containerClass} text-center`}>
          <div className={`text-3xl font-bold ${style.titleClass}`}>
            {confidence.toFixed(0)}%
          </div>
          <div className="text-xs text-foreground-muted">Confidence</div>
        </div>
      </div>

      {/* Cost Savings Badge (if not patentable) */}
      {!isPatentable && (
        <div className="glass-card p-4 mb-4">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-warning/10 flex items-center justify-center">
              <Lightbulb className="h-5 w-5 text-warning" />
            </div>
            <div>
              <p className="text-sm font-semibold text-foreground">
                Cost Savings: $500 - $1,000
              </p>
              <p className="text-xs text-foreground-muted">
                Prior art search skipped to avoid wasting resources on non-patentable research
              </p>
            </div>
          </div>
        </div>
      )}

      {/* Missing Elements (if any) */}
      {missingElements && missingElements.length > 0 && (
        <div className="mb-4">
          <h4 className="text-sm font-semibold text-foreground mb-3">
            Missing Elements
          </h4>
          <ul className="space-y-2">
            {missingElements.map((element, idx) => (
              <li key={idx} className="flex items-start gap-2 text-sm">
                <span className="text-error font-bold mt-0.5">•</span>
                <span className="text-foreground-muted">{element}</span>
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Recommendations */}
      {recommendations && recommendations.length > 0 && (
        <div className="mb-4">
          <h4 className="text-sm font-semibold text-foreground mb-3">
            Recommendations
          </h4>
          <ul className="space-y-2">
            {recommendations.map((rec, idx) => (
              <li key={idx} className="flex items-start gap-2 text-sm">
                <CheckCircle2 className={`h-4 w-4 ${style.iconClass} flex-shrink-0 mt-0.5`} />
                <span className="text-foreground-muted">{rec}</span>
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Action Buttons (only if not patentable) */}
      {!isPatentable && (onContinue || onUploadNew) && (
        <div className="flex items-center gap-3 pt-4 border-t border-border">
          {onUploadNew && (
            <button
              onClick={onUploadNew}
              className="btn btn-gradient flex-1"
            >
              <Sparkles className="w-4 h-4" />
              <span>Upload Revised Disclosure</span>
            </button>
          )}
          {onContinue && (
            <button
              onClick={onContinue}
              className="btn btn-secondary"
            >
              Continue Anyway
            </button>
          )}
        </div>
      )}
    </div>
  );
}
