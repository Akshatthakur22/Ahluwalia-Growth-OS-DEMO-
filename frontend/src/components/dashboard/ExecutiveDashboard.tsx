'use client';

import Link from 'next/link';
import { formatINR } from '@/lib/format';
import { formatStatus, LIFECYCLE_FLOW } from '@/lib/lifecycle';

export interface ExecutiveDashboardData {
  revenue: {
    total_pipeline_value: number;
    weighted_pipeline_value: number;
    confirmed_revenue: number;
    quotations_outstanding: number;
    avg_deal_size: number;
  };
  opportunities: {
    total: number;
    active_pipeline: number;
    confirmed_orders: number;
    lost: number;
    win_rate_percent: number;
    in_negotiation: number;
    quotations_sent: number;
  };
  pipeline_by_status: Record<string, number>;
  growth: {
    sites_this_month: number;
    total_sites: number;
    showroom_visits_this_month: number;
    total_meetings: number;
  };
  team_pulse: {
    attendance_percentage: number;
    checked_in_today: number;
    total_active_employees: number;
  };
  top_deals: {
    id: string;
    opportunity_name: string;
    current_status: string;
    expected_revenue?: number;
    probability_of_conversion?: number;
  }[];
}

const STAGE_COLORS: Record<string, string> = {
  new_site: '#94a3b8',
  relationship_building: '#3b82f6',
  showroom_visit_scheduled: '#6366f1',
  showroom_visit_done: '#8b5cf6',
  selection_done: '#a855f7',
  quotation_sent: '#d946ef',
  negotiation: '#f97316',
  order_confirmed: '#22c55e',
  lost: '#fca5a5',
};

function RingGauge({
  value,
  max = 100,
  label,
  sublabel,
  color,
  size = 120,
}: {
  value: number;
  max?: number;
  label: string;
  sublabel?: string;
  color: string;
  size?: number;
}) {
  const pct = Math.min(100, Math.max(0, (value / max) * 100));
  const r = (size - 14) / 2;
  const c = 2 * Math.PI * r;
  const offset = c - (pct / 100) * c;

  return (
    <div className="flex flex-col items-center">
      <div className="relative" style={{ width: size, height: size }}>
        <svg width={size} height={size} className="-rotate-90">
          <circle cx={size / 2} cy={size / 2} r={r} fill="none" stroke="#f1f5f9" strokeWidth="10" />
          <circle
            cx={size / 2}
            cy={size / 2}
            r={r}
            fill="none"
            stroke={color}
            strokeWidth="10"
            strokeLinecap="round"
            strokeDasharray={c}
            strokeDashoffset={offset}
            className="transition-all duration-700 ease-out"
          />
        </svg>
        <div className="absolute inset-0 flex flex-col items-center justify-center">
          <span className="text-2xl font-bold text-gray-900">{Math.round(pct)}%</span>
        </div>
      </div>
      <p className="text-sm font-semibold text-gray-800 mt-2">{label}</p>
      {sublabel && <p className="text-[11px] text-gray-400 text-center">{sublabel}</p>}
    </div>
  );
}

function RevenueComposition({ data }: { data: ExecutiveDashboardData }) {
  const total = data.revenue.total_pipeline_value || 1;
  const segments = [
    { label: 'Confirmed', value: data.revenue.confirmed_revenue, color: '#22c55e' },
    { label: 'Quotations Out', value: data.revenue.quotations_outstanding, color: '#f97316' },
    { label: 'Weighted Forecast', value: data.revenue.weighted_pipeline_value, color: '#8b5cf6' },
    { label: 'Remaining Pipeline', value: Math.max(0, total - data.revenue.weighted_pipeline_value), color: '#3b82f6' },
  ];
  const segTotal = segments.reduce((s, x) => s + x.value, 0) || 1;

  return (
    <div className="space-y-4">
      <div className="flex h-4 rounded-full overflow-hidden bg-gray-100 shadow-inner">
        {segments.map((seg) => {
          const w = (seg.value / segTotal) * 100;
          if (w < 0.5) return null;
          return (
            <div
              key={seg.label}
              style={{ width: `${w}%`, backgroundColor: seg.color }}
              className="transition-all duration-500"
              title={`${seg.label}: ${formatINR(seg.value)}`}
            />
          );
        })}
      </div>
      <div className="grid grid-cols-2 gap-3">
        {segments.map((seg) => (
          <div key={seg.label} className="flex items-center gap-2">
            <span className="w-3 h-3 rounded-full shrink-0" style={{ backgroundColor: seg.color }} />
            <div className="min-w-0">
              <p className="text-[11px] text-gray-500 truncate">{seg.label}</p>
              <p className="text-sm font-semibold text-gray-900">{formatINR(seg.value)}</p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

function SalesFunnel({ pipeline }: { pipeline: Record<string, number> }) {
  const tiers = [
    {
      label: 'Discovery',
      stages: ['new_site', 'relationship_building'],
      color: 'from-slate-500 to-blue-500',
    },
    {
      label: 'Engagement',
      stages: ['showroom_visit_scheduled', 'showroom_visit_done'],
      color: 'from-indigo-500 to-violet-500',
    },
    {
      label: 'Conversion',
      stages: ['selection_done', 'quotation_sent', 'negotiation'],
      color: 'from-fuchsia-500 to-orange-500',
    },
    {
      label: 'Won',
      stages: ['order_confirmed'],
      color: 'from-green-500 to-emerald-600',
    },
  ];

  const counts = tiers.map((t) => ({
    ...t,
    count: t.stages.reduce((s, st) => s + (pipeline[st] || 0), 0),
  }));
  const max = Math.max(...counts.map((c) => c.count), 1);

  return (
    <div className="space-y-2">
      {counts.map((tier, i) => {
        const widthPct = 40 + (tier.count / max) * 60;
        return (
          <div key={tier.label} className="flex items-center gap-3">
            <span className="text-[10px] text-gray-400 w-20 text-right shrink-0">{tier.label}</span>
            <div className="flex-1 flex justify-center">
              <div
                className={`h-10 rounded-lg bg-gradient-to-r ${tier.color} flex items-center justify-center text-white text-sm font-semibold shadow-sm transition-all duration-500`}
                style={{ width: `${widthPct}%`, minWidth: '80px' }}
              >
                {tier.count} deals
              </div>
            </div>
            {i < counts.length - 1 && (
              <span className="text-gray-200 text-lg hidden sm:block">↓</span>
            )}
          </div>
        );
      })}
      {(pipeline.lost || 0) > 0 && (
        <p className="text-center text-[11px] text-red-400 pt-1">{pipeline.lost} lost · excluded from funnel</p>
      )}
    </div>
  );
}

function VerticalBarChart({ pipeline }: { pipeline: Record<string, number> }) {
  const stages = [...LIFECYCLE_FLOW, 'lost' as const];
  const max = Math.max(...stages.map((s) => pipeline[s] || 0), 1);

  return (
    <div className="flex items-end justify-between gap-1 sm:gap-2 h-40 pt-4">
      {stages.map((stage) => {
        const count = pipeline[stage] || 0;
        const h = count ? Math.max(12, (count / max) * 100) : 4;
        return (
          <div key={stage} className="flex-1 flex flex-col items-center gap-1 min-w-0">
            <span className="text-[10px] font-semibold text-gray-700">{count || ''}</span>
            <div
              className="w-full rounded-t-md transition-all duration-500"
              style={{
                height: `${h}%`,
                backgroundColor: STAGE_COLORS[stage] || '#cbd5e1',
                opacity: count ? 1 : 0.25,
              }}
            />
            <span className="text-[8px] sm:text-[9px] text-gray-400 text-center leading-tight h-8 flex items-start justify-center">
              {formatStatus(stage).split(' ').slice(0, 2).join(' ')}
            </span>
          </div>
        );
      })}
    </div>
  );
}

function TopDealsChart({ deals }: { deals: ExecutiveDashboardData['top_deals'] }) {
  const max = Math.max(...deals.map((d) => d.expected_revenue || 0), 1);

  return (
    <div className="space-y-3">
      {deals.map((d, i) => {
        const rev = d.expected_revenue || 0;
        const pct = (rev / max) * 100;
        return (
          <div key={d.id}>
            <div className="flex justify-between items-baseline gap-2 mb-1">
              <div className="flex items-center gap-2 min-w-0">
                <span className="text-xs font-bold text-gray-300 w-4">#{i + 1}</span>
                <p className="text-sm font-medium text-gray-900 truncate">{d.opportunity_name}</p>
              </div>
              <p className="text-sm font-semibold text-green-600 shrink-0">{formatINR(rev)}</p>
            </div>
            <div className="h-2.5 bg-gray-100 rounded-full overflow-hidden">
              <div
                className="h-full rounded-full bg-gradient-to-r from-[#0071e3] to-emerald-500 transition-all duration-700"
                style={{ width: `${pct}%` }}
              />
            </div>
            <div className="flex justify-between mt-1">
              <span className="demo-badge bg-indigo-50 text-indigo-600 text-[10px]">{formatStatus(d.current_status)}</span>
              {d.probability_of_conversion != null && (
                <span className="text-[10px] text-gray-400">{d.probability_of_conversion}% probability</span>
              )}
            </div>
          </div>
        );
      })}
    </div>
  );
}

function GrowthPulse({ growth }: { growth: ExecutiveDashboardData['growth'] }) {
  const items = [
    { label: 'New Sites', value: growth.sites_this_month, max: growth.total_sites, color: '#22c55e', icon: '🏗️' },
    { label: 'Showroom Visits', value: growth.showroom_visits_this_month, max: Math.max(growth.showroom_visits_this_month, 10), color: '#f97316', icon: '✨' },
    { label: 'Meetings', value: growth.total_meetings, max: growth.total_meetings, color: '#8b5cf6', icon: '🤝' },
  ];

  return (
    <div className="grid grid-cols-3 gap-3">
      {items.map((item) => {
        const pct = item.max ? Math.min(100, (item.value / item.max) * 100) : 0;
        return (
          <div key={item.label} className="bg-gray-50 rounded-xl p-3 border border-gray-100 text-center">
            <span className="text-xl">{item.icon}</span>
            <p className="text-2xl font-bold text-gray-900 mt-1">{item.value}</p>
            <p className="text-[10px] text-gray-500">{item.label}</p>
            <div className="h-1 bg-gray-200 rounded-full mt-2 overflow-hidden">
              <div className="h-full rounded-full transition-all duration-500" style={{ width: `${pct}%`, backgroundColor: item.color }} />
            </div>
          </div>
        );
      })}
    </div>
  );
}

export function ExecutiveDashboard({ data }: { data: ExecutiveDashboardData }) {
  const forecastGap = data.revenue.total_pipeline_value - data.revenue.confirmed_revenue;
  const conversionHealth = data.opportunities.quotations_sent + data.opportunities.in_negotiation;

  return (
    <div className="space-y-5">
      {/* Hero KPI strip */}
      <div className="rounded-2xl bg-gradient-to-br from-slate-900 via-indigo-950 to-slate-900 text-white p-6 sm:p-8 shadow-lg overflow-hidden relative">
        <div className="absolute top-0 right-0 w-64 h-64 bg-blue-500/10 rounded-full blur-3xl -translate-y-1/2 translate-x-1/4" />
        <div className="absolute bottom-0 left-0 w-48 h-48 bg-emerald-500/10 rounded-full blur-3xl translate-y-1/2 -translate-x-1/4" />
        <div className="relative">
          <p className="text-indigo-300 text-xs font-medium uppercase tracking-widest">Ahluwalia Marbles · Executive KPIs</p>
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-6 mt-5">
            <div>
              <p className="text-white/60 text-sm">Total Pipeline</p>
              <p className="text-3xl sm:text-4xl font-bold tracking-tight mt-1">{formatINR(data.revenue.total_pipeline_value)}</p>
              <p className="text-emerald-400 text-xs mt-2">{data.opportunities.active_pipeline} active opportunities</p>
            </div>
            <div className="sm:border-x sm:border-white/10 sm:px-6">
              <p className="text-white/60 text-sm">Confirmed Revenue</p>
              <p className="text-3xl sm:text-4xl font-bold tracking-tight mt-1 text-emerald-400">{formatINR(data.revenue.confirmed_revenue)}</p>
              <p className="text-white/50 text-xs mt-2">{data.opportunities.confirmed_orders} orders closed</p>
            </div>
            <div>
              <p className="text-white/60 text-sm">Upside Remaining</p>
              <p className="text-3xl sm:text-4xl font-bold tracking-tight mt-1 text-amber-300">{formatINR(forecastGap)}</p>
              <p className="text-white/50 text-xs mt-2">Pipeline − confirmed</p>
            </div>
          </div>
        </div>
      </div>

      {/* Ring gauges + quick stats */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
        <div className="demo-card lg:col-span-1 flex justify-around items-center py-6">
          <RingGauge
            value={data.opportunities.win_rate_percent}
            label="Win Rate"
            sublabel={`${data.opportunities.confirmed_orders}W · ${data.opportunities.lost}L`}
            color="#22c55e"
          />
          <RingGauge
            value={data.team_pulse.attendance_percentage}
            label="Team Pulse"
            sublabel={`${data.team_pulse.checked_in_today}/${data.team_pulse.total_active_employees} in`}
            color="#8b5cf6"
          />
        </div>

        <div className="demo-card lg:col-span-2">
          <h3 className="text-sm font-semibold text-gray-900 mb-1">Revenue Composition</h3>
          <p className="text-xs text-gray-400 mb-4">How pipeline value breaks down across stages</p>
          <RevenueComposition data={data} />
        </div>
      </div>

      {/* KPI tiles */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-3">
        {[
          { label: 'Weighted Forecast', value: formatINR(data.revenue.weighted_pipeline_value), hint: 'Probability-adjusted', accent: 'text-purple-600' },
          { label: 'Quotations Out', value: formatINR(data.revenue.quotations_outstanding), hint: 'Awaiting client', accent: 'text-orange-600' },
          { label: 'Avg Deal Size', value: formatINR(data.revenue.avg_deal_size), hint: 'Per opportunity', accent: 'text-blue-600' },
          { label: 'Late Stage', value: conversionHealth, hint: 'Quote + negotiation', accent: 'text-fuchsia-600' },
        ].map((kpi) => (
          <div key={kpi.label} className="demo-card !p-4 border-l-4 border-l-[#0071e3]">
            <p className="text-[11px] text-gray-500 font-medium uppercase tracking-wide">{kpi.label}</p>
            <p className={`text-2xl font-bold mt-1 ${kpi.accent}`}>{kpi.value}</p>
            <p className="text-[10px] text-gray-400 mt-1">{kpi.hint}</p>
          </div>
        ))}
      </div>

      {/* Funnel + bar chart */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
        <div className="demo-card">
          <h3 className="text-sm font-semibold text-gray-900">Sales Funnel</h3>
          <p className="text-xs text-gray-400 mb-4">Deal concentration by lifecycle tier</p>
          <SalesFunnel pipeline={data.pipeline_by_status} />
        </div>
        <div className="demo-card">
          <h3 className="text-sm font-semibold text-gray-900">Pipeline by Stage</h3>
          <p className="text-xs text-gray-400 mb-2">Deal count across lifecycle</p>
          <VerticalBarChart pipeline={data.pipeline_by_status} />
        </div>
      </div>

      {/* Growth + top deals */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
        <div className="demo-card">
          <h3 className="text-sm font-semibold text-gray-900">Growth Pulse</h3>
          <p className="text-xs text-gray-400 mb-4">Field & showroom activity this month</p>
          <GrowthPulse growth={data.growth} />
          <p className="text-xs text-gray-400 mt-3 text-center">{data.growth.total_sites} sites in portfolio</p>
        </div>
        {data.top_deals?.length > 0 && (
          <div className="demo-card">
            <h3 className="text-sm font-semibold text-gray-900">Top Deals by Value</h3>
            <p className="text-xs text-gray-400 mb-4">Highest-value active opportunities</p>
            <TopDealsChart deals={data.top_deals} />
          </div>
        )}
      </div>

      {/* Executive shortcuts */}
      <div className="grid grid-cols-3 gap-3">
        <Link href="/opportunities" className="demo-card !p-4 text-center hover:border-indigo-200 hover:bg-indigo-50/30 transition-colors group">
          <span className="text-2xl">📈</span>
          <p className="text-sm font-semibold text-gray-900 mt-2 group-hover:text-indigo-700">Full Pipeline</p>
        </Link>
        <Link href="/search" className="demo-card !p-4 text-center hover:border-blue-200 hover:bg-blue-50/30 transition-colors group">
          <span className="text-2xl">🔍</span>
          <p className="text-sm font-semibold text-gray-900 mt-2 group-hover:text-blue-700">Master Search</p>
        </Link>
        <Link href="/attendance/team" className="demo-card !p-4 text-center hover:border-purple-200 hover:bg-purple-50/30 transition-colors group">
          <span className="text-2xl">👥</span>
          <p className="text-sm font-semibold text-gray-900 mt-2 group-hover:text-purple-700">Team Pulse</p>
        </Link>
      </div>
    </div>
  );
}
