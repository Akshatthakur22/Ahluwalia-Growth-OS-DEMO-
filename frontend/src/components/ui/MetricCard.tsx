const ACCENTS: Record<string, string> = {
  blue: 'text-[#0071e3]',
  green: 'text-green-600',
  purple: 'text-purple-600',
  orange: 'text-orange-600',
  red: 'text-red-600',
  gray: 'text-gray-500',
};

export function MetricCard({
  label,
  value,
  subtitle,
  accent = 'blue',
}: {
  label: string;
  value: string | number;
  subtitle?: string;
  accent?: string;
}) {
  return (
    <div className="demo-card !p-4">
      <p className="text-xs text-gray-500 font-medium">{label}</p>
      <p className={`text-2xl sm:text-3xl font-semibold mt-1 ${ACCENTS[accent] || ACCENTS.blue}`}>{value}</p>
      {subtitle && <p className="text-xs text-gray-400 mt-1">{subtitle}</p>}
    </div>
  );
}
