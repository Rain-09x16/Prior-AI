'use client';

import { AlertCircle, CheckCircle2, AlertTriangle, Lightbulb } from 'lucide-react';
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
        containerClass: 'bg-red-50 border-red-200',
        iconClass: 'text-red-600',
        titleClass: 'text-red-900',
        textClass: 'text-red-800',
        icon: AlertCircle,
        title: 'Not Patentable',
        message: 'This disclosure appears to be publishable research but lacks key elements required for patent protection.',
      };
    }

    if (confidence < 60) {
      return {
        containerClass: 'bg-red-50 border-red-200',
        iconClass: 'text-red-600',
        titleClass: 'text-red-900',
        textClass: 'text-red-800',
        icon: AlertCircle,
        title: 'Low Patentability',
        message: 'This disclosure has low patentability. Consider significant revisions before filing.',
      };
    }

    if (confidence < 80) {
      return {
        containerClass: 'bg-yellow-50 border-yellow-200',
        iconClass: 'text-yellow-600',
        titleClass: 'text-yellow-900',
        textClass: 'text-yellow-800',
        icon: AlertTriangle,
        title: 'Borderline Patentability',
        message: 'This disclosure may be patentable but could benefit from improvements.',
      };
    }

    return {
      containerClass: 'bg-green-50 border-green-200',
      iconClass: 'text-green-600',
      titleClass: 'text-green-900',
      textClass: 'text-green-800',
      icon: CheckCircle2,
      title: 'Likely Patentable',
      message: 'This disclosure appears to have strong patentability. Proceeding with prior art search.',
    };
  };

  const style = getAlertStyle();
  const Icon = style.icon;

  return (
    <div className={`rounded-xl border-2 p-6 mb-6 shadow-md ${style.containerClass}`}>
      {/* Header */}
      <div className="flex items-start space-x-3 mb-4">
        <Icon className={`h-6 w-6 ${style.iconClass} flex-shrink-0 mt-0.5`} />
        <div className="flex-1">
          <h3 className={`text-lg font-bold ${style.titleClass} mb-1`}>
            {style.title}
          </h3>
          <p className={`text-sm ${style.textClass}`}>
            {style.message}
          </p>
        </div>
        <div className="text-right">
          <div className={`text-2xl font-bold ${style.titleClass}`}>
            {confidence.toFixed(0)}%
          </div>
          <div className={`text-xs ${style.textClass}`}>Confidence</div>
        </div>
      </div>

      {/* Cost Savings Badge (if not patentable) */}
      {!isPatentable && (
        <div className="bg-white border-2 border-red-300 rounded-lg p-3 mb-4">
          <div className="flex items-center space-x-2">
            <Lightbulb className="h-5 w-5 text-yellow-600" />
            <div>
              <p className="text-sm font-semibold text-gray-900">
                Cost Savings: $500 - $1,000
              </p>
              <p className="text-xs text-gray-600">
                Prior art search skipped to avoid wasting resources on non-patentable research
              </p>
            </div>
          </div>
        </div>
      )}

      {/* Missing Elements (if any) */}
      {missingElements && missingElements.length > 0 && (
        <div className="mb-4">
          <h4 className={`text-sm font-semibold ${style.titleClass} mb-2`}>
            Missing Elements:
          </h4>
          <ul className={`space-y-1 text-sm ${style.textClass}`}>
            {missingElements.map((element, idx) => (
              <li key={idx} className="flex items-start space-x-2">
                <span className="text-red-600 font-bold">•</span>
                <span>{element}</span>
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Recommendations */}
      {recommendations && recommendations.length > 0 && (
        <div className="mb-4">
          <h4 className={`text-sm font-semibold ${style.titleClass} mb-2`}>
            Recommendations:
          </h4>
          <ul className={`space-y-2 text-sm ${style.textClass}`}>
            {recommendations.map((rec, idx) => (
              <li key={idx} className="flex items-start space-x-2">
                <CheckCircle2 className={`h-4 w-4 ${style.iconClass} flex-shrink-0 mt-0.5`} />
                <span>{rec}</span>
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Action Buttons (only if not patentable) */}
      {!isPatentable && (onContinue || onUploadNew) && (
        <div className="flex items-center space-x-3 pt-4 border-t-2 border-red-200">
          {onUploadNew && (
            <button
              onClick={onUploadNew}
              className="flex-1 px-5 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 font-semibold text-sm transition-all shadow-sm hover:shadow-md min-h-11"
            >
              Upload Revised Disclosure
            </button>
          )}
          {onContinue && (
            <button
              onClick={onContinue}
              className="px-5 py-3 bg-white border-2 border-red-300 text-red-700 rounded-lg hover:bg-red-50 font-semibold text-sm transition-all min-h-11"
            >
              Continue Anyway
            </button>
          )}
        </div>
      )}
    </div>
  );
}
