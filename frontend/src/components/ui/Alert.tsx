export function Alert({ type, children }: { type: 'error' | 'success' | 'info'; children: React.ReactNode }) {
  const styles = {
    error: 'bg-red-50 border-red-100 text-red-700',
    success: 'bg-green-50 border-green-100 text-green-700',
    info: 'bg-blue-50 border-blue-100 text-blue-700',
  };
  return (
    <div className={`border px-4 py-3 rounded-xl text-sm ${styles[type]}`}>{children}</div>
  );
}
