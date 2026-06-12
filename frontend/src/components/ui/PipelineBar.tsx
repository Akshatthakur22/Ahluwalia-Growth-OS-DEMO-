import { LIFECYCLE_FLOW, formatStatus } from '@/lib/lifecycle';

export function PipelineBar({ pipeline }: { pipeline: Record<string, number> }) {
  const total = Object.values(pipeline).reduce((a, b) => a + b, 0) || 1;
  const stages = [...LIFECYCLE_FLOW, 'lost' as const];
  const colors = [
    'bg-slate-400', 'bg-blue-400', 'bg-indigo-400', 'bg-violet-400',
    'bg-purple-400', 'bg-fuchsia-500', 'bg-orange-400', 'bg-green-500', 'bg-red-300',
  ];

  return (
    <div className="space-y-4">
      <div className="flex h-3 rounded-full overflow-hidden bg-gray-100">
        {stages.map((stage, i) => {
          const count = pipeline[stage] || 0;
          if (count === 0) return null;
          const pct = (count / total) * 100;
          return (
            <div
              key={stage}
              className={`${colors[i]} transition-all`}
              style={{ width: `${pct}%` }}
              title={`${formatStatus(stage)}: ${count}`}
            />
          );
        })}
      </div>
      <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-2">
        {stages.map((stage, i) => {
          const count = pipeline[stage] || 0;
          return (
            <div key={stage} className="bg-gray-50 rounded-xl p-3 border border-gray-100">
              <div className="flex items-center gap-1.5 mb-1">
                <span className={`w-2 h-2 rounded-full ${colors[i]}`} />
                <p className="text-[10px] text-gray-500 leading-tight">{formatStatus(stage)}</p>
              </div>
              <p className="text-xl font-semibold text-gray-900">{count}</p>
            </div>
          );
        })}
      </div>
    </div>
  );
}
