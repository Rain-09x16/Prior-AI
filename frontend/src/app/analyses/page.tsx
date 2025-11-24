'use client';

import { useEffect, useState } from 'react';
import { useAnalysisStore } from '@/stores/analysisStore';
import { AnalysisCard } from '@/components/AnalysisCard';
import { SkeletonList } from '@/components/SkeletonCard';
import { Filter } from 'lucide-react';

export default function AnalysesPage() {
  const { analyses, isLoading, fetchAnalyses, deleteAnalysis } = useAnalysisStore();
  const [statusFilter, setStatusFilter] = useState<string>('all');

  useEffect(() => {
    const params = statusFilter === 'all' ? {} : { status: statusFilter };
    fetchAnalyses(params);
  }, [statusFilter, fetchAnalyses]);

  const handleDelete = async (id: string) => {
    try {
      await deleteAnalysis(id);
    } catch (error) {
      console.error('Delete failed:', error);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">All Analyses</h1>
          <p className="text-gray-600">
            View and manage your prior art analysis history
          </p>
        </div>

      {/* Filters */}
      <div className="mb-6 flex items-center space-x-4">
        <div className="flex items-center space-x-2">
          <Filter className="h-4 w-4 text-gray-500" />
          <span className="text-sm font-medium text-gray-700">Filter by status:</span>
        </div>
        <div className="flex space-x-2">
          {['all', 'processing', 'completed', 'failed'].map((status) => (
            <button
              key={status}
              onClick={() => setStatusFilter(status)}
              className={`px-5 py-2.5 text-sm font-semibold rounded-lg transition-all min-h-[40px] ${
                statusFilter === status
                  ? 'bg-blue-600 text-white shadow-sm'
                  : 'bg-white text-gray-700 border-2 border-gray-300 hover:bg-gray-50 hover:border-gray-400'
              }`}
            >
              {status.charAt(0).toUpperCase() + status.slice(1)}
            </button>
          ))}
        </div>
      </div>

      {/* Loading state */}
      {isLoading && <SkeletonList count={6} />}

      {/* Empty state */}
      {!isLoading && analyses.length === 0 && (
        <div className="text-center py-16">
          <p className="text-gray-600 mb-4">No analyses found</p>
          <a
            href="/"
            className="inline-flex items-center px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-all font-semibold shadow-sm hover:shadow-md min-h-11"
          >
            Upload New Disclosure
          </a>
        </div>
      )}

      {/* Analyses grid */}
      {!isLoading && analyses.length > 0 && (
        <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
          {analyses.map((analysis) => (
            <AnalysisCard
              key={analysis.id}
              analysis={analysis}
              onDelete={handleDelete}
            />
          ))}
        </div>
      )}
      </div>
    </div>
  );
}
