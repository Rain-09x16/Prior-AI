'use client';

import { useState } from 'react';
import { ChevronDown, ChevronUp, ExternalLink } from 'lucide-react';
import type { PatentMatch } from '@/lib/types';
import { truncate } from '@/lib/utils';

interface PatentCardProps {
  patent: PatentMatch;
  rank?: number;
}

export function PatentCard({ patent, rank }: PatentCardProps) {
  const [isExpanded, setIsExpanded] = useState(false);

  const getSimilarityColor = (score: number): string => {
    if (score >= 70) return 'text-red-700 bg-red-50 border-red-300';
    if (score >= 50) return 'text-orange-700 bg-orange-50 border-orange-300';
    return 'text-green-700 bg-green-50 border-green-300';
  };

  return (
    <div className="border-2 border-gray-200 rounded-xl overflow-hidden bg-white hover:shadow-lg hover:border-blue-200 transition-all">
      {/* Header */}
      <div className="p-5 bg-gradient-to-r from-gray-50 to-gray-100 border-b-2 border-gray-200">
        <div className="flex items-start justify-between">
          <div className="flex-1">
            {rank && (
              <span className="inline-block px-3 py-1.5 text-xs font-bold bg-blue-600 text-white rounded-full mr-2 shadow-sm">
                #{rank}
              </span>
            )}
            <h3 className="text-lg font-bold text-gray-900 mb-2 leading-tight">
              {patent.title}
            </h3>
            <div className="flex items-center space-x-4 text-sm text-gray-600">
              <span className="font-mono">{patent.patentId}</span>
              {patent.publicationDate && (
                <span>{new Date(patent.publicationDate).getFullYear()}</span>
              )}
            </div>
          </div>

          {/* Similarity Score */}
          <div className={`px-5 py-3 rounded-xl font-bold text-xl border-2 shadow-sm ${getSimilarityColor(patent.similarityScore)}`}>
            {patent.similarityScore.toFixed(1)}%
          </div>
        </div>
      </div>

      {/* Content */}
      <div className="p-4">
        {/* Assignee */}
        {patent.assignee && (
          <div className="mb-3">
            <span className="text-sm font-medium text-gray-700">Assignee: </span>
            <span className="text-sm text-gray-600">{patent.assignee}</span>
          </div>
        )}

        {/* Abstract */}
        {patent.abstract && (
          <div className="mb-3">
            <p className="text-sm text-gray-700">
              {isExpanded ? patent.abstract : truncate(patent.abstract, 200)}
            </p>
          </div>
        )}

        {/* Overlapping Concepts */}
        {patent.overlappingConcepts && patent.overlappingConcepts.length > 0 && (
          <div className="mb-3">
            <p className="text-sm font-medium text-gray-700 mb-2">Overlapping Concepts:</p>
            <div className="flex flex-wrap gap-2">
              {patent.overlappingConcepts.map((concept, idx) => (
                <span
                  key={idx}
                  className="px-2 py-1 text-xs bg-orange-100 text-orange-800 rounded"
                >
                  {concept}
                </span>
              ))}
            </div>
          </div>
        )}

        {/* Key Differences */}
        {patent.keyDifferences && patent.keyDifferences.length > 0 && isExpanded && (
          <div className="mb-3">
            <p className="text-sm font-medium text-gray-700 mb-2">Key Differences:</p>
            <div className="flex flex-wrap gap-2">
              {patent.keyDifferences.map((diff, idx) => (
                <span
                  key={idx}
                  className="px-2 py-1 text-xs bg-green-100 text-green-800 rounded"
                >
                  {diff}
                </span>
              ))}
            </div>
          </div>
        )}

        {/* Inventors */}
        {patent.inventors && patent.inventors.length > 0 && isExpanded && (
          <div className="mb-3">
            <p className="text-sm font-medium text-gray-700">Inventors:</p>
            <p className="text-sm text-gray-600">{patent.inventors.join(', ')}</p>
          </div>
        )}

        {/* IPC Classifications */}
        {patent.ipcClassifications && patent.ipcClassifications.length > 0 && isExpanded && (
          <div className="mb-3">
            <p className="text-sm font-medium text-gray-700 mb-1">IPC Classifications:</p>
            <div className="flex flex-wrap gap-2">
              {patent.ipcClassifications.map((ipc, idx) => (
                <span
                  key={idx}
                  className="px-2 py-1 text-xs bg-blue-100 text-blue-800 rounded font-mono"
                >
                  {ipc}
                </span>
              ))}
            </div>
          </div>
        )}

        {/* Actions */}
        <div className="flex items-center justify-between pt-3 border-t border-gray-200">
          <button
            onClick={() => setIsExpanded(!isExpanded)}
            className="flex items-center space-x-1 text-sm text-blue-600 hover:text-blue-800"
          >
            {isExpanded ? (
              <>
                <ChevronUp className="h-4 w-4" />
                <span>Show less</span>
              </>
            ) : (
              <>
                <ChevronDown className="h-4 w-4" />
                <span>Show more</span>
              </>
            )}
          </button>

          <a
            href={`https://patents.google.com/patent/${patent.patentId}`}
            target="_blank"
            rel="noopener noreferrer"
            className="flex items-center space-x-1 text-sm text-blue-600 hover:text-blue-800"
          >
            <span>View on Google Patents</span>
            <ExternalLink className="h-4 w-4" />
          </a>
        </div>
      </div>
    </div>
  );
}
