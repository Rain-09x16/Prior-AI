/**
 * API client for Prior Art Analyst backend with Clerk authentication
 */
import axios, { AxiosInstance, InternalAxiosRequestConfig } from 'axios';
import type { Analysis, AnalysisListResponse, ReportResponse } from './types';

class PriorAIClient {
  private client: AxiosInstance;
  private baseUrl: string;
  private getToken: (() => Promise<string | null>) | null = null;

  constructor() {
    this.baseUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';
    this.client = axios.create({
      baseURL: this.baseUrl,
      timeout: 300000, // 5 minutes for long-running analysis
      headers: {
        'Content-Type': 'application/json',
      },
    });

    // Add request interceptor for authentication
    this.client.interceptors.request.use(
      async (config: InternalAxiosRequestConfig) => {
        if (this.getToken) {
          try {
            const token = await this.getToken();
            if (token) {
              config.headers.Authorization = `Bearer ${token}`;
            }
          } catch (error) {
            console.error('Error getting auth token:', error);
          }
        }
        return config;
      },
      (error) => Promise.reject(error)
    );

    // Add response interceptor for error handling
    this.client.interceptors.response.use(
      (response) => response,
      (error) => {
        if (error.response?.status === 401) {
          console.error('Unauthorized - please sign in again');
        }
        console.error('API Error:', error.response?.data || error.message);
        return Promise.reject(error);
      }
    );
  }

  /**
   * Set the token retrieval function (called from React components)
   */
  setTokenGetter(getToken: () => Promise<string | null>): void {
    this.getToken = getToken;
  }

  /**
   * Upload disclosure and create analysis
   */
  async createAnalysis(file: File, title?: string): Promise<Analysis> {
    const formData = new FormData();
    formData.append('file', file);
    if (title) {
      formData.append('title', title);
    }

    const response = await this.client.post<Analysis>('/analyses', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });

    return response.data;
  }

  /**
   * Get analysis by ID
   */
  async getAnalysis(id: string): Promise<Analysis> {
    const response = await this.client.get<Analysis>(`/analyses/${id}`);
    return response.data;
  }

  /**
   * List all analyses with pagination
   */
  async listAnalyses(params?: {
    page?: number;
    limit?: number;
    status?: string;
  }): Promise<AnalysisListResponse> {
    const response = await this.client.get<AnalysisListResponse>('/analyses', {
      params,
    });
    return response.data;
  }

  /**
   * Generate PDF report for analysis
   */
  async generateReport(id: string): Promise<ReportResponse> {
    const response = await this.client.post<ReportResponse>(
      `/analyses/${id}/report`
    );
    return response.data;
  }

  /**
   * Delete analysis
   */
  async deleteAnalysis(id: string): Promise<void> {
    await this.client.delete(`/analyses/${id}`);
  }

  /**
   * Get report download URL
   */
  getReportUrl(reportPath: string): string {
    return `${this.baseUrl}${reportPath}`;
  }

  /**
   * Health check
   */
  async healthCheck(): Promise<{ status: string }> {
    const response = await this.client.get('/health');
    return response.data;
  }
}

// Export singleton instance
export const apiClient = new PriorAIClient();
