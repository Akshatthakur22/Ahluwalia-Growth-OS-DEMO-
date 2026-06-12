const ICONS: Record<string, string> = {
  sites: '🏗️',
  meetings: '🤝',
  pipeline: '📊',
  attendance: '📍',
  showroom: '✨',
  search: '🔍',
  assignments: '📋',
  default: '📋',
};

export function EmptyState({
  icon,
  title,
  message,
  action,
}: {
  icon?: string;
  title?: string;
  message: string;
  action?: React.ReactNode;
}) {
  const emoji = icon || ICONS.default;
  return (
    <div className="text-center py-12 px-4">
      <div className="text-4xl mb-3 opacity-80">{emoji}</div>
      {title && <p className="text-sm font-medium text-gray-700 mb-1">{title}</p>}
      <p className="text-gray-500 text-sm max-w-xs mx-auto">{message}</p>
      {action && <div className="mt-5">{action}</div>}
    </div>
  );
}
