'use client';

import { useEffect, useState } from 'react';
import { useAnalysisStore } from '@/stores/analysisStore';
import { AnalysisCard } from '@/components/AnalysisCard';
import { SkeletonList } from '@/components/SkeletonCard';
import { Filter, FileSearch, Plus, Sparkles } from 'lucide-react';
import Link from 'next/link';

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
    <div className="min-h-screen bg-background">
      {/* Hero gradient background */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <div className="absolute top-0 left-1/4 w-96 h-96 bg-primary/20 rounded-full blur-3xl" />
        <div className="absolute top-20 right-1/4 w-80 h-80 bg-accent/20 rounded-full blur-3xl" />
      </div>

      <div className="container mx-auto px-4 pt-24 pb-8 relative">
        {/* Header */}
        <div className="mb-8">
          <div className="flex items-start justify-between">
            <div>
              <div className="flex items-center gap-3 mb-3">
                <div className="w-12 h-12 rounded-2xl bg-gradient-to-br from-primary to-accent flex items-center justify-center shadow-lg shadow-primary/25">
                  <FileSearch className="w-6 h-6 text-white" />
                </div>
                <h1 className="text-4xl font-bold text-foreground">All Analyses</h1>
              </div>
              <p className="text-foreground-muted text-lg">
                View and manage your prior art analysis history
              </p>
            </div>
            <Link href="/dashboard" className="btn btn-gradient">
              <Plus className="w-4 h-4" />
              <span>New Analysis</span>
            </Link>
          </div>
        </div>

        {/* Filters */}
        <div className="mb-8 glass-card p-4">
          <div className="flex items-center gap-4 flex-wrap">
            <div className="flex items-center gap-2">
              <Filter className="h-4 w-4 text-foreground-muted" />
              <span className="text-sm font-medium text-foreground">Filter by status:</span>
            </div>
            <div className="flex gap-2 flex-wrap">
              {['all', 'processing', 'completed', 'failed'].map((status) => (
                <button
                  key={status}
                  onClick={() => setStatusFilter(status)}
                  className={`px-4 py-2 text-sm font-medium rounded-lg transition-all ${
                    statusFilter === status
                      ? 'bg-primary text-white shadow-lg shadow-primary/25'
                      : 'bg-background-tertiary text-foreground-muted hover:bg-background-secondary hover:text-foreground border border-border'
                  }`}
                >
                  {status.charAt(0).toUpperCase() + status.slice(1)}
                </button>
              ))}
            </div>
          </div>
        </div>

        {/* Loading state */}
        {isLoading && <SkeletonList count={6} />}

        {/* Empty state */}
        {!isLoading && analyses.length === 0 && (
          <div className="text-center py-20">
            <div className="w-20 h-20 rounded-3xl bg-primary/10 flex items-center justify-center mx-auto mb-6">
              <FileSearch className="w-10 h-10 text-primary" />
            </div>
            <h3 className="text-xl font-semibold text-foreground mb-2">No analyses found</h3>
            <p className="text-foreground-muted mb-6">
              {statusFilter === 'all'
                ? "You haven't created any analyses yet. Upload a disclosure to get started."
                : `No ${statusFilter} analyses found. Try a different filter.`}
            </p>
            <Link href="/dashboard" className="btn btn-gradient">
              <Sparkles className="w-4 h-4" />
              <span>Upload New Disclosure</span>
            </Link>
          </div>
        )}

        {/* Analyses grid */}
        {!isLoading && analyses.length > 0 && (
          <>
            <div className="flex items-center justify-between mb-4">
              <p className="text-sm text-foreground-muted">
                Showing {analyses.length} {statusFilter !== 'all' ? statusFilter : ''} {analyses.length === 1 ? 'analysis' : 'analyses'}
              </p>
            </div>
            <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
              {analyses.map((analysis) => (
                <AnalysisCard
                  key={analysis.id}
                  analysis={analysis}
                  onDelete={handleDelete}
                />
              ))}
            </div>
          </>
        )}
      </div>
    </div>
  );
}
