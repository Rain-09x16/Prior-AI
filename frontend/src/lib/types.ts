/**
 * TypeScript types for Prior Art Analyst
 */

export interface ExtractedClaims {
  background: string;
  innovations: string[];
  technicalSpecs: Record<string, string>;
  keywords: string[];
  ipcClassifications: string[];
}

export interface DisclosureInfo {
  filename: string;
  uploadedAt: string;
}

export interface PatentMatch {
  id: string;
  patentId: string;
  title: string;
  abstract?: string;
  claims?: string[];
  publicationDate?: string;
  assignee?: string;
  inventors?: string[];
  ipcClassifications?: string[];
  similarityScore: number;
  overlappingConcepts?: string[];
  keyDifferences?: string[];
  source: string;
}

/**
 * NEW in v2.1: Patentability Assessment
 * This runs BEFORE the expensive prior art search to filter out
 * publishable-only research from patentable inventions.
 */
export interface PatentabilityAssessment {
  isPatentable: boolean;
  confidence: number; // 0-100
  missingElements: string[];
  recommendations: string[];
}

export type AnalysisStatus = 'processing' | 'completed' | 'failed';
export type Recommendation = 'pursue' | 'reconsider' | 'reject';

export interface Analysis {
  id: string;
  title: string;
  status: AnalysisStatus;
  disclosure: DisclosureInfo;
  extractedClaims?: ExtractedClaims;
  patents?: PatentMatch[];
  noveltyScore?: number;
  recommendation?: Recommendation;
  reasoning?: string;

  // NEW in v2.1: Patentability assessment
  patentabilityAssessment?: PatentabilityAssessment;
  isPatentable?: boolean;
  patentabilityConfidence?: number;
  missingElements?: string;

  createdAt: string;
  updatedAt?: string;
  completedAt?: string;
}

export interface AnalysisListResponse {
  data: Analysis[];
  total: number;
  page: number;
  limit: number;
  pages: number;
}

export interface ReportResponse {
  reportUrl: string;
  expiresAt?: string;
}
