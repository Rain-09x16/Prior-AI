/**
 * Zustand store for analysis state management
 */
import { create } from 'zustand';
import { apiClient } from '@/lib/api';
import type { Analysis } from '@/lib/types';

interface AnalysisStore {
  // State
  analyses: Analysis[];
  currentAnalysis: Analysis | null;
  isLoading: boolean;
  error: string | null;
  uploadProgress: number;

  // Actions
  setCurrentAnalysis: (analysis: Analysis | null) => void;
  setError: (error: string | null) => void;
  fetchAnalyses: (params?: { page?: number; limit?: number; status?: string }) => Promise<void>;
  fetchAnalysis: (id: string) => Promise<void>;
  createAnalysis: (file: File, title?: string) => Promise<string>;
  deleteAnalysis: (id: string) => Promise<void>;
  pollAnalysis: (id: string, maxAttempts?: number) => Promise<void>;
  generateReport: (id: string) => Promise<string>;
  clearError: () => void;
}

export const useAnalysisStore = create<AnalysisStore>((set, get) => ({
  // Initial state
  analyses: [],
  currentAnalysis: null,
  isLoading: false,
  error: null,
  uploadProgress: 0,

  // Actions
  setCurrentAnalysis: (analysis) => set({ currentAnalysis: analysis }),

  setError: (error) => set({ error }),

  clearError: () => set({ error: null }),

  fetchAnalyses: async (params) => {
    set({ isLoading: true, error: null });
    try {
      const response = await apiClient.listAnalyses(params);
      set({ analyses: response.data, isLoading: false });
    } catch (error: any) {
      set({
        error: error.response?.data?.detail || 'Failed to fetch analyses',
        isLoading: false,
      });
    }
  },

  fetchAnalysis: async (id) => {
    set({ isLoading: true, error: null });
    try {
      const analysis = await apiClient.getAnalysis(id);
      set({ currentAnalysis: analysis, isLoading: false });
    } catch (error: any) {
      set({
        error: error.response?.data?.detail || 'Failed to fetch analysis',
        isLoading: false,
      });
    }
  },

  createAnalysis: async (file, title) => {
    set({ isLoading: true, error: null, uploadProgress: 0 });
    try {
      const analysis = await apiClient.createAnalysis(file, title);
      set({
        currentAnalysis: analysis,
        isLoading: false,
        uploadProgress: 100,
      });
      return analysis.id;
    } catch (error: any) {
      set({
        error: error.response?.data?.detail || 'Failed to create analysis',
        isLoading: false,
        uploadProgress: 0,
      });
      throw error;
    }
  },

  deleteAnalysis: async (id) => {
    set({ isLoading: true, error: null });
    try {
      await apiClient.deleteAnalysis(id);
      const { analyses, currentAnalysis } = get();
      set({
        analyses: analyses.filter((a) => a.id !== id),
        currentAnalysis: currentAnalysis?.id === id ? null : currentAnalysis,
        isLoading: false,
      });
    } catch (error: any) {
      set({
        error: error.response?.data?.detail || 'Failed to delete analysis',
        isLoading: false,
      });
      throw error;
    }
  },

  pollAnalysis: async (id, maxAttempts = 60) => {
    let attempts = 0;

    const poll = async (): Promise<void> => {
      try {
        const analysis = await apiClient.getAnalysis(id);
        set({ currentAnalysis: analysis });

        if (analysis.status === 'completed' || analysis.status === 'failed') {
          return;
        }

        attempts++;
        if (attempts >= maxAttempts) {
          set({ error: 'Analysis polling timeout' });
          return;
        }

        // Poll every 3 seconds
        setTimeout(() => poll(), 3000);
      } catch (error: any) {
        set({
          error: error.response?.data?.detail || 'Failed to poll analysis',
        });
      }
    };

    await poll();
  },

  generateReport: async (id) => {
    set({ isLoading: true, error: null });
    try {
      const response = await apiClient.generateReport(id);
      set({ isLoading: false });
      return apiClient.getReportUrl(response.reportUrl);
    } catch (error: any) {
      set({
        error: error.response?.data?.detail || 'Failed to generate report',
        isLoading: false,
      });
      throw error;
    }
  },
}));
