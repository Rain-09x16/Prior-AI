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
 * Get status color
 */
export function getStatusColor(status: string): string {
  switch (status) {
    case 'completed':
      return 'text-green-600 bg-green-50 border-green-200';
    case 'processing':
      return 'text-blue-600 bg-blue-50 border-blue-200';
    case 'failed':
      return 'text-red-600 bg-red-50 border-red-200';
    default:
      return 'text-gray-600 bg-gray-50 border-gray-200';
  }
}

/**
 * Get recommendation color
 */
export function getRecommendationColor(recommendation: string): string {
  switch (recommendation) {
    case 'pursue':
      return 'text-green-700 bg-green-100 border-green-300';
    case 'reconsider':
      return 'text-orange-700 bg-orange-100 border-orange-300';
    case 'reject':
      return 'text-red-700 bg-red-100 border-red-300';
    default:
      return 'text-gray-700 bg-gray-100 border-gray-300';
  }
}

/**
 * Get novelty score color
 */
export function getNoveltyScoreColor(score: number): string {
  if (score >= 70) {
    return 'text-green-600';
  } else if (score >= 40) {
    return 'text-orange-600';
  } else {
    return 'text-red-600';
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
