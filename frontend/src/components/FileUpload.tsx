'use client';

import { useCallback, useState } from 'react';
import { useDropzone } from 'react-dropzone';
import { Upload, FileText, X } from 'lucide-react';
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
    <div className="w-full max-w-2xl mx-auto">
      {/* Dropzone */}
      <div
        {...getRootProps()}
        className={`border-2 border-dashed rounded-xl p-12 text-center cursor-pointer transition-all ${
          isDragActive
            ? 'border-blue-500 bg-blue-50 scale-[1.02]'
            : 'border-gray-300 hover:border-blue-400 bg-white hover:bg-gray-50'
        }`}
      >
        <input {...getInputProps()} />
        <Upload className="h-12 w-12 mx-auto text-gray-400 mb-4" />
        {isDragActive ? (
          <p className="text-lg text-blue-600">Drop the file here...</p>
        ) : (
          <>
            <p className="text-lg text-gray-700 mb-2">
              Drag and drop your disclosure document here
            </p>
            <p className="text-sm text-gray-500">
              or click to browse (PDF or DOCX, max {formatFileSize(maxSize)})
            </p>
          </>
        )}
      </div>

      {/* Selected file preview */}
      {selectedFile && (
        <div className="mt-4 p-4 bg-gray-50 rounded-lg border border-gray-200 animate-fade-in">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <FileText className="h-8 w-8 text-blue-600" />
              <div>
                <p className="font-medium text-gray-900">{selectedFile.name}</p>
                <p className="text-sm text-gray-500">
                  {formatFileSize(selectedFile.size)}
                </p>
              </div>
            </div>
            <button
              onClick={clearFile}
              className="p-2 hover:bg-gray-200 rounded-lg transition-colors"
              disabled={isUploading}
            >
              <X className="h-5 w-5 text-gray-500" />
            </button>
          </div>

          <button
            onClick={handleUpload}
            disabled={isUploading}
            className="mt-4 w-full bg-blue-600 text-white py-3.5 px-6 rounded-lg font-semibold hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-all min-h-[44px] shadow-sm hover:shadow-md flex items-center justify-center gap-2"
          >
            {isUploading ? (
              <>
                <div className="animate-spin h-4 w-4 border-2 border-white border-t-transparent rounded-full" />
                <span>Uploading...</span>
              </>
            ) : (
              'Start Analysis'
            )}
          </button>
        </div>
      )}

      {/* Error message */}
      {error && (
        <div className="mt-4 p-4 bg-red-50 border border-red-200 rounded-lg text-red-700 animate-fade-in">
          {error}
        </div>
      )}
    </div>
  );
}
