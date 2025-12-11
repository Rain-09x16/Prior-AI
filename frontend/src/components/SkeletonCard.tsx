export function SkeletonCard() {
  return (
    <div className="card p-6 animate-pulse">
      {/* Header skeleton */}
      <div className="flex items-start justify-between mb-4">
        <div className="flex-1">
          <div className="flex items-center gap-3 mb-2">
            <div className="h-10 w-10 bg-background-tertiary rounded-xl" />
            <div className="h-6 w-3/4 bg-background-tertiary rounded-lg" />
          </div>
          <div className="h-4 w-1/2 bg-background-tertiary rounded-lg ml-13" />
        </div>
        <div className="h-6 w-20 bg-background-tertiary rounded-full" />
      </div>

      {/* Content skeleton */}
      <div className="space-y-4">
        <div className="grid grid-cols-2 gap-4">
          <div className="bg-background-tertiary p-4 rounded-xl">
            <div className="h-3 w-20 bg-background-secondary rounded mb-2" />
            <div className="h-8 w-16 bg-background-secondary rounded-lg" />
          </div>
          <div className="bg-background-tertiary p-4 rounded-xl">
            <div className="h-3 w-24 bg-background-secondary rounded mb-2" />
            <div className="h-6 w-20 bg-background-secondary rounded-full" />
          </div>
        </div>
        <div className="h-4 w-40 bg-background-tertiary rounded-lg" />
      </div>

      {/* Actions skeleton */}
      <div className="mt-4 pt-4 border-t border-border flex items-center justify-between">
        <div className="h-4 w-24 bg-background-tertiary rounded-lg" />
        <div className="h-8 w-8 bg-background-tertiary rounded-lg" />
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
