interface ProgressBarProps {
  progress: number;
  label?: string;
  showPercentage?: boolean;
}

export function ProgressBar({ progress, label, showPercentage = true }: ProgressBarProps) {
  return (
    <div className="w-full">
      {(label || showPercentage) && (
        <div className="flex items-center justify-between mb-2">
          {label && <span className="text-sm font-medium text-gray-700">{label}</span>}
          {showPercentage && (
            <span className="text-sm font-semibold text-blue-600">{Math.round(progress)}%</span>
          )}
        </div>
      )}
      <div className="w-full h-2.5 bg-gray-200 rounded-full overflow-hidden shadow-inner">
        <div
          className="h-full bg-gradient-to-r from-blue-500 to-blue-600 rounded-full transition-all duration-300 ease-out shadow-sm"
          style={{ width: `${Math.min(100, Math.max(0, progress))}%` }}
        />
      </div>
    </div>
  );
}
