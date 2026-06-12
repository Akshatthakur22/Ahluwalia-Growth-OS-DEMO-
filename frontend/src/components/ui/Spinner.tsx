export function Spinner({ className = 'h-8 w-8' }: { className?: string }) {
  return (
    <div className={`rounded-full border-2 border-gray-200 border-t-blue-600 animate-spin ${className}`} />
  );
}
