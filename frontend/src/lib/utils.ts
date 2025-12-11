/**
 * Utility functions
 */
import { type ClassValue, clsx } from 'clsx';
import { formatDistanceToNow, format } from 'date-fns';

/**
 * Merge Tailwind CSS classes
 */
export function cn(...inputs: ClassValue[]) {
  return clsx(inputs);
}

/**
 * Format date to relative time (e.g., "2 hours ago")
 */
export function formatRelativeTime(date: string | Date): string {
  try {
    return formatDistanceToNow(new Date(date), { addSuffix: true });
  } catch {
    return 'Unknown';
  }
}

/**
 * Format date to readable string
 */
export function formatDate(date: string | Date): string {
  try {
    return format(new Date(date), 'PPP');
  } catch {
    return 'Unknown';
  }
}

/**
 * Format date and time
 */
export function formatDateTime(date: string | Date): string {
  try {
    return format(new Date(date), 'PPpp');
  } catch {
    return 'Unknown';
  }
}

/**
 * Get status color - using theme variables
 */
export function getStatusColor(status: string): string {
  switch (status) {
    case 'completed':
      return 'text-success bg-success/10 border-success/30';
    case 'processing':
      return 'text-info bg-info/10 border-info/30';
    case 'failed':
      return 'text-error bg-error/10 border-error/30';
    default:
      return 'text-foreground-muted bg-background-tertiary border-border';
  }
}

/**
 * Get recommendation color - using theme variables
 */
export function getRecommendationColor(recommendation: string): string {
  switch (recommendation) {
    case 'pursue':
      return 'text-success bg-success/10 border border-success/30';
    case 'reconsider':
      return 'text-warning bg-warning/10 border border-warning/30';
    case 'reject':
      return 'text-error bg-error/10 border border-error/30';
    default:
      return 'text-foreground-muted bg-background-tertiary border border-border';
  }
}

/**
 * Get novelty score color - using theme variables
 */
export function getNoveltyScoreColor(score: number): string {
  if (score >= 70) {
    return 'text-success';
  } else if (score >= 40) {
    return 'text-warning';
  } else {
    return 'text-error';
  }
}

/**
 * Format file size
 */
export function formatFileSize(bytes: number): string {
  if (bytes === 0) return '0 Bytes';
  const k = 1024;
  const sizes = ['Bytes', 'KB', 'MB', 'GB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
}

/**
 * Truncate text
 */
export function truncate(text: string, length: number = 100): string {
  if (text.length <= length) return text;
  return text.substring(0, length) + '...';
}
