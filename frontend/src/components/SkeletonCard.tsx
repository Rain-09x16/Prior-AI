export function SkeletonCard() {
  return (
    <div className="block p-6 bg-white border-2 border-gray-200 rounded-xl animate-pulse">
      {/* Header skeleton */}
      <div className="flex items-start justify-between mb-4">
        <div className="flex-1">
          <div className="flex items-center space-x-3 mb-2">
            <div className="h-5 w-5 bg-gray-200 rounded" />
            <div className="h-6 w-3/4 bg-gray-200 rounded" />
          </div>
          <div className="h-4 w-1/2 bg-gray-200 rounded" />
        </div>
        <div className="h-6 w-20 bg-gray-200 rounded-full" />
      </div>

      {/* Content skeleton */}
      <div className="space-y-3">
        <div className="grid grid-cols-2 gap-4">
          <div className="bg-gray-100 p-4 rounded-lg">
            <div className="h-3 w-20 bg-gray-200 rounded mb-2" />
            <div className="h-8 w-16 bg-gray-200 rounded" />
          </div>
          <div className="bg-gray-100 p-4 rounded-lg">
            <div className="h-3 w-24 bg-gray-200 rounded mb-2" />
            <div className="h-6 w-20 bg-gray-200 rounded" />
          </div>
        </div>
        <div className="h-4 w-40 bg-gray-200 rounded" />
      </div>

      {/* Actions skeleton */}
      <div className="mt-4 pt-4 border-t border-gray-200 flex items-center justify-between">
        <div className="h-4 w-24 bg-gray-200 rounded" />
        <div className="h-8 w-8 bg-gray-200 rounded" />
      </div>
    </div>
  );
}

export function SkeletonList({ count = 3 }: { count?: number }) {
  return (
    <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
      {Array.from({ length: count }).map((_, i) => (
        <SkeletonCard key={i} />
      ))}
    </div>
  );
}
