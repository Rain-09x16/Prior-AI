'use client';

import { useCallback, useState } from 'react';
import { useDropzone } from 'react-dropzone';
import { Upload, FileText, X, Loader2, Sparkles } from 'lucide-react';
import { formatFileSize } from '@/lib/utils';

interface FileUploadProps {
  onUpload: (file: File) => Promise<void>;
  accept?: string;
  maxSize?: number;
}

export function FileUpload({
  onUpload,
  accept = '.pdf,.docx',
  maxSize = 10 * 1024 * 1024, // 10MB
}: FileUploadProps) {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [isUploading, setIsUploading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const onDrop = useCallback((acceptedFiles: File[]) => {
    setError(null);
    if (acceptedFiles.length > 0) {
      const file = acceptedFiles[0];
      if (file.size > maxSize) {
        setError(`File size exceeds ${formatFileSize(maxSize)}`);
        return;
      }
      setSelectedFile(file);
    }
  }, [maxSize]);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/pdf': ['.pdf'],
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx'],
    },
    maxFiles: 1,
    multiple: false,
  });

  const handleUpload = async () => {
    if (!selectedFile) return;

    setIsUploading(true);
    setError(null);

    try {
      await onUpload(selectedFile);
      setSelectedFile(null);
    } catch (err: any) {
      setError(err.message || 'Upload failed');
    } finally {
      setIsUploading(false);
    }
  };

  const clearFile = () => {
    setSelectedFile(null);
    setError(null);
  };

  return (
    <div className="w-full">
      {/* Dropzone */}
      <div
        {...getRootProps()}
        className={`dropzone relative overflow-hidden ${
          isDragActive ? 'active' : ''
        } ${selectedFile ? 'border-primary' : ''}`}
      >
        <input {...getInputProps()} />

        {/* Background pattern */}
        <div className="absolute inset-0 hero-grid opacity-20 pointer-events-none" />

        <div className="relative">
          <div className="inline-flex items-center justify-center w-16 h-16 rounded-2xl bg-primary/10 mb-6 mx-auto">
            <Upload className={`w-8 h-8 ${isDragActive ? 'text-primary animate-pulse' : 'text-foreground-muted'}`} />
          </div>

          {isDragActive ? (
            <div className="animate-fade-in">
              <p className="text-xl font-semibold text-primary mb-2">Drop your file here</p>
              <p className="text-sm text-foreground-muted">Release to upload</p>
            </div>
          ) : (
            <>
              <p className="text-lg font-semibold text-foreground mb-2">
                Drag and drop your disclosure document
              </p>
              <p className="text-sm text-foreground-muted mb-4">
                or click to browse
              </p>
              <div className="flex items-center justify-center gap-3">
                <span className="badge badge-neutral badge-pill">PDF</span>
                <span className="badge badge-neutral badge-pill">DOCX</span>
                <span className="badge badge-neutral badge-pill">Max {formatFileSize(maxSize)}</span>
              </div>
            </>
          )}
        </div>
      </div>

      {/* Selected file preview */}
      {selectedFile && (
        <div className="mt-6 p-5 rounded-xl bg-background-secondary border border-border animate-fade-in">
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center gap-4">
              <div className="w-12 h-12 rounded-xl bg-primary/10 flex items-center justify-center">
                <FileText className="w-6 h-6 text-primary" />
              </div>
              <div>
                <p className="font-semibold text-foreground">{selectedFile.name}</p>
                <p className="text-sm text-foreground-muted">
                  {formatFileSize(selectedFile.size)}
                </p>
              </div>
            </div>
            <button
              onClick={clearFile}
              className="btn btn-ghost btn-sm"
              disabled={isUploading}
            >
              <X className="w-5 h-5" />
            </button>
          </div>

          <button
            onClick={handleUpload}
            disabled={isUploading}
            className="btn btn-gradient w-full"
          >
            {isUploading ? (
              <>
                <Loader2 className="w-5 h-5 animate-spin" />
                <span>Analyzing...</span>
              </>
            ) : (
              <>
                <Sparkles className="w-5 h-5" />
                <span>Start Analysis</span>
              </>
            )}
          </button>
        </div>
      )}

      {/* Error message */}
      {error && (
        <div className="mt-4 p-4 rounded-xl alert alert-error animate-fade-in">
          <span>{error}</span>
        </div>
      )}
    </div>
  );
}
