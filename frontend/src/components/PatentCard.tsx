'use client';

import { useState } from 'react';
import { ChevronDown, ChevronUp, ExternalLink, Award, Users, Tag } from 'lucide-react';
import type { PatentMatch } from '@/lib/types';
import { truncate } from '@/lib/utils';

interface PatentCardProps {
  patent: PatentMatch;
  rank?: number;
}

export function PatentCard({ patent, rank }: PatentCardProps) {
  const [isExpanded, setIsExpanded] = useState(false);

  const getSimilarityStyle = (score: number) => {
    if (score >= 70) return { bg: 'bg-error/10', border: 'border-error/30', text: 'text-error' };
    if (score >= 50) return { bg: 'bg-warning/10', border: 'border-warning/30', text: 'text-warning' };
    return { bg: 'bg-success/10', border: 'border-success/30', text: 'text-success' };
  };

  const similarityStyle = getSimilarityStyle(patent.similarityScore);

  return (
    <div className="card overflow-hidden hover:border-primary/50 transition-all group">
      {/* Header */}
      <div className="p-5 bg-background-tertiary border-b border-border">
        <div className="flex items-start justify-between gap-4">
          <div className="flex-1 min-w-0">
            <div className="flex items-center gap-3 mb-2">
              {rank && (
                <span className="inline-flex items-center justify-center w-8 h-8 rounded-lg bg-gradient-to-br from-primary to-accent text-white text-sm font-bold shadow-lg shadow-primary/25">
                  #{rank}
                </span>
              )}
              <h3 className="text-lg font-bold text-foreground line-clamp-2 group-hover:text-primary transition-colors">
                {patent.title}
              </h3>
            </div>
            <div className="flex items-center gap-4 text-sm text-foreground-muted">
              <span className="font-mono">{patent.patentId}</span>
              {patent.publicationDate && (
                <span>{new Date(patent.publicationDate).getFullYear()}</span>
              )}
            </div>
          </div>

          {/* Similarity Score */}
          <div className={`px-4 py-3 rounded-xl border ${similarityStyle.bg} ${similarityStyle.border}`}>
            <div className={`text-2xl font-bold ${similarityStyle.text}`}>
              {patent.similarityScore.toFixed(1)}%
            </div>
            <div className="text-xs text-foreground-muted">Similarity</div>
          </div>
        </div>
      </div>

      {/* Content */}
      <div className="p-5">
        {/* Assignee */}
        {patent.assignee && (
          <div className="flex items-center gap-2 mb-4 text-sm">
            <Award className="w-4 h-4 text-foreground-muted" />
            <span className="text-foreground-muted">Assignee:</span>
            <span className="text-foreground font-medium">{patent.assignee}</span>
          </div>
        )}

        {/* Abstract */}
        {patent.abstract && (
          <div className="mb-4">
            <p className="text-sm text-foreground-muted leading-relaxed">
              {isExpanded ? patent.abstract : truncate(patent.abstract, 200)}
            </p>
          </div>
        )}

        {/* Overlapping Concepts */}
        {patent.overlappingConcepts && patent.overlappingConcepts.length > 0 && (
          <div className="mb-4">
            <div className="flex items-center gap-2 mb-2">
              <Tag className="w-4 h-4 text-warning" />
              <span className="text-sm font-medium text-foreground">Overlapping Concepts</span>
            </div>
            <div className="flex flex-wrap gap-2">
              {patent.overlappingConcepts.map((concept, idx) => (
                <span key={idx} className="tag tag-primary">
                  {concept}
                </span>
              ))}
            </div>
          </div>
        )}

        {/* Key Differences (expanded) */}
        {patent.keyDifferences && patent.keyDifferences.length > 0 && isExpanded && (
          <div className="mb-4">
            <div className="flex items-center gap-2 mb-2">
              <Tag className="w-4 h-4 text-success" />
              <span className="text-sm font-medium text-foreground">Key Differences</span>
            </div>
            <div className="flex flex-wrap gap-2">
              {patent.keyDifferences.map((diff, idx) => (
                <span key={idx} className="tag tag-accent">
                  {diff}
                </span>
              ))}
            </div>
          </div>
        )}

        {/* Inventors (expanded) */}
        {patent.inventors && patent.inventors.length > 0 && isExpanded && (
          <div className="mb-4">
            <div className="flex items-center gap-2 mb-2">
              <Users className="w-4 h-4 text-foreground-muted" />
              <span className="text-sm font-medium text-foreground">Inventors</span>
            </div>
            <p className="text-sm text-foreground-muted">{patent.inventors.join(', ')}</p>
          </div>
        )}

        {/* IPC Classifications (expanded) */}
        {patent.ipcClassifications && patent.ipcClassifications.length > 0 && isExpanded && (
          <div className="mb-4">
            <p className="text-sm font-medium text-foreground mb-2">IPC Classifications</p>
            <div className="flex flex-wrap gap-2">
              {patent.ipcClassifications.map((ipc, idx) => (
                <span key={idx} className="badge badge-neutral badge-pill font-mono text-xs">
                  {ipc}
                </span>
              ))}
            </div>
          </div>
        )}

        {/* Actions */}
        <div className="flex items-center justify-between pt-4 border-t border-border">
          <button
            onClick={() => setIsExpanded(!isExpanded)}
            className="btn btn-ghost btn-sm"
          >
            {isExpanded ? (
              <>
                <ChevronUp className="w-4 h-4" />
                <span>Show less</span>
              </>
            ) : (
              <>
                <ChevronDown className="w-4 h-4" />
                <span>Show more</span>
              </>
            )}
          </button>

          <a
            href={`https://patents.google.com/patent/${patent.patentId}`}
            target="_blank"
            rel="noopener noreferrer"
            className="btn btn-secondary btn-sm"
          >
            <span>View Patent</span>
            <ExternalLink className="w-4 h-4" />
          </a>
        </div>
      </div>
    </div>
  );
}
