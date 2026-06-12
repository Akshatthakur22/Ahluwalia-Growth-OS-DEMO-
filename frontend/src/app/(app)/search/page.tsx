'use client';

import { useEffect, useState, useRef } from 'react';
import api from '@/lib/api';
import { Card } from '@/components/ui/Card';
import { Button } from '@/components/ui/Button';
import { Input } from '@/components/ui/Input';
import { PageHeader } from '@/components/ui/PageHeader';
import { Alert } from '@/components/ui/Alert';
import { Spinner } from '@/components/ui/Spinner';
import { EmptyState } from '@/components/ui/EmptyState';
import { formatStatus } from '@/lib/lifecycle';
import { formatINR, formatRelativeDate } from '@/lib/format';

const DEMO_CONTACTS = [
  { mobile: '9812345678', name: 'Ravi Mehta', firm: 'Mehta Constructions' },
  { mobile: '9844455667', name: 'Vikram Malhotra', firm: 'Malhotra Infra' },
  { mobile: '9866677889', name: 'Rahul Bansal', firm: 'Horizon Tech Parks' },
];

type SearchMode = 'mobile' | 'name';

export default function SearchPage() {
  const [mode, setMode] = useState<SearchMode>('mobile');
  const [query, setQuery] = useState(DEMO_CONTACTS[0].mobile);
  const [suggestions, setSuggestions] = useState<any[]>([]);
  const [results, setResults] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const suggestAbort = useRef<AbortController | null>(null);

  useEffect(() => {
    if (query.length < 2) {
      setSuggestions([]);
      return;
    }
    const timer = setTimeout(() => {
      suggestAbort.current?.abort();
      const controller = new AbortController();
      suggestAbort.current = controller;
      api.get('/search/suggest', { params: { q: query }, signal: controller.signal })
        .then((res) => setSuggestions(res.data.suggestions || []))
        .catch(() => { if (!controller.signal.aborted) setSuggestions([]); });
    }, 300);
    return () => clearTimeout(timer);
  }, [query]);

  const runSearch = async (e?: React.FormEvent, overrideQuery?: string) => {
    e?.preventDefault();
    const q = overrideQuery || query;
    if (overrideQuery) setQuery(overrideQuery);
    setLoading(true);
    setError('');
    setResults(null);
    setSuggestions([]);
    try {
      const endpoint = mode === 'mobile'
        ? `/search/mobile/${encodeURIComponent(q)}`
        : `/search/name/${encodeURIComponent(q)}`;
      const { data } = await api.get(endpoint);
      setResults(data);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Search failed');
    } finally {
      setLoading(false);
    }
  };

  const pickSuggestion = (s: any) => {
    if (s.mobile) {
      setMode('mobile');
      setQuery(s.mobile);
      runSearch(undefined, s.mobile);
    } else {
      setMode('name');
      setQuery(s.label);
      runSearch(undefined, s.label);
    }
  };

  const totalResults = results
    ? (results.contacts?.length || 0) + (results.sites?.length || 0) + (results.meetings?.length || 0)
      + (results.showroom_visits?.length || 0) + (results.opportunities?.length || 0)
    : 0;

  const totalRevenue = results?.opportunities?.reduce(
    (sum: number, o: any) => sum + Number(o.expected_revenue || 0), 0
  ) || 0;

  const timeline = results ? [
    ...(results.meetings || []).map((m: any) => ({
      type: 'meeting', date: m.meeting_date, title: m.stakeholder_name,
      subtitle: [m.met_with && `Met: ${m.met_with}`, m.firm_name, m.summary].filter(Boolean).join(' · ') || 'Meeting recorded',
      icon: '🤝',
    })),
    ...(results.showroom_visits || []).map((v: any) => ({
      type: 'showroom', date: v.visit_date, title: v.selected_material || 'Showroom visit',
      subtitle: v.estimated_quantity ? `${v.estimated_quantity} sq.ft estimated` : 'Material selection', icon: '✨',
    })),
    ...(results.opportunities || []).map((o: any) => ({
      type: 'opportunity', date: o.created_at || o.follow_up_date || new Date().toISOString(),
      title: o.opportunity_name, subtitle: formatStatus(o.current_status), icon: '📈',
      revenue: o.expected_revenue,
    })),
    ...(results.sites || []).map((s: any) => ({
      type: 'site', date: s.created_at || new Date().toISOString(), title: s.site_name,
      subtitle: `${s.address}, ${s.city}`, icon: '🏗️',
    })),
  ].sort((a, b) => new Date(b.date).getTime() - new Date(a.date).getTime()) : [];

  return (
    <div className="space-y-6">
      <PageHeader title="Master Search" subtitle="Mobile, name, auto-suggest — complete relationship history with ownership" />

      <Card title="Search">
        <div className="flex gap-2 mb-4">
          {(['mobile', 'name'] as SearchMode[]).map((m) => (
            <button
              key={m}
              type="button"
              onClick={() => setMode(m)}
              className={`text-sm px-4 py-2 rounded-full border transition-colors ${
                mode === m ? 'bg-[#0071e3] text-white border-[#0071e3]' : 'border-gray-200 text-gray-600 hover:bg-gray-50'
              }`}
            >
              {m === 'mobile' ? 'By Mobile' : 'By Name'}
            </button>
          ))}
        </div>
        <form onSubmit={runSearch} className="flex flex-col sm:flex-row gap-3 relative">
          <div className="flex-1 relative">
            <Input
              placeholder={mode === 'mobile' ? 'Mobile number' : 'Contact or stakeholder name'}
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              className="w-full"
            />
            {suggestions.length > 0 && (
              <div className="absolute z-20 top-full left-0 right-0 mt-1 bg-white border border-gray-100 rounded-xl shadow-lg overflow-hidden">
                {suggestions.map((s, i) => (
                  <button
                    key={i}
                    type="button"
                    onClick={() => pickSuggestion(s)}
                    className="w-full text-left px-4 py-3 hover:bg-blue-50 border-b border-gray-50 last:border-0"
                  >
                    <p className="text-sm font-medium text-gray-900">{s.label}</p>
                    <p className="text-xs text-gray-500">{s.sublabel}</p>
                  </button>
                ))}
              </div>
            )}
          </div>
          <Button type="submit" disabled={loading} className="sm:self-end">{loading ? 'Searching...' : 'Search'}</Button>
        </form>
        {mode === 'mobile' && (
          <div className="flex flex-wrap gap-2 mt-3">
            {DEMO_CONTACTS.map((c) => (
              <button
                key={c.mobile}
                type="button"
                onClick={() => runSearch(undefined, c.mobile)}
                className="text-xs bg-gray-50 hover:bg-blue-50 text-gray-600 hover:text-[#0071e3] px-3 py-1.5 rounded-full border border-gray-100 transition-colors"
              >
                {c.name} · {c.mobile}
              </button>
            ))}
          </div>
        )}
      </Card>

      {error && <Alert type="error">{error}</Alert>}
      {loading && <div className="flex justify-center py-8"><Spinner /></div>}

      {results && totalResults === 0 && (
        <EmptyState icon="search" title="No records found" message="Try a different mobile number or contact name." />
      )}

      {results && totalResults > 0 && (
        <>
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
            <div className="demo-card !p-4 col-span-2 sm:col-span-1">
              <p className="text-xs text-gray-500">Total Touchpoints</p>
              <p className="text-3xl font-semibold text-[#0071e3] mt-1">{totalResults}</p>
            </div>
            <div className="demo-card !p-4">
              <p className="text-xs text-gray-500">Pipeline Value</p>
              <p className="text-2xl font-semibold text-green-600 mt-1">{formatINR(totalRevenue)}</p>
            </div>
            <div className="demo-card !p-4">
              <p className="text-xs text-gray-500">Contacts</p>
              <p className="text-2xl font-semibold text-gray-900 mt-1">{results.contacts?.length || 0}</p>
            </div>
            <div className="demo-card !p-4">
              <p className="text-xs text-gray-500">Meetings</p>
              <p className="text-2xl font-semibold text-gray-900 mt-1">{results.meetings?.length || 0}</p>
            </div>
          </div>

          {results.contacts?.length > 0 && (
            <Card title="Contact Profile">
              {results.contacts.map((c: any) => (
                <div key={c.id} className="flex items-start gap-4">
                  <div className="w-12 h-12 rounded-full bg-gradient-to-br from-[#0071e3] to-indigo-600 flex items-center justify-center text-white font-semibold text-lg shrink-0">
                    {c.name.charAt(0)}
                  </div>
                  <div>
                    <p className="font-semibold text-gray-900">{c.name}</p>
                    <p className="text-sm text-gray-500 capitalize">{c.contact_type} · {c.firm_name || '—'}</p>
                    <p className="text-sm text-gray-400 mt-0.5">{c.mobile_number} · {c.designation || 'Stakeholder'}{c.category ? ` · Cat ${c.category}` : ''}</p>
                  </div>
                </div>
              ))}
            </Card>
          )}

          {results.opportunity_ownership?.length > 0 && (
            <Card title="Lead Ownership">
              {results.opportunity_ownership.map((item: any, i: number) => (
                <div key={i} className="py-3 border-b border-gray-100 last:border-0">
                  <p className="font-medium text-sm">{item.opportunity.opportunity_name}</p>
                  <span className="demo-badge bg-indigo-100 text-indigo-700 mt-1 inline-block">{formatStatus(item.opportunity.current_status)}</span>
                  <div className="grid grid-cols-3 gap-2 mt-2 text-xs text-gray-500">
                    {['lead_creator', 'marketing_owner', 'sales_owner'].map((role) => (
                      <div key={role}>
                        <p className="text-gray-400 capitalize">{role.replace('_', ' ')}</p>
                        <p className="font-medium text-gray-700">{item.ownership?.[role]?.name || '—'}</p>
                      </div>
                    ))}
                  </div>
                </div>
              ))}
            </Card>
          )}

          <Card title="Relationship Timeline">
            <div className="relative">
              <div className="absolute left-[15px] top-2 bottom-2 w-px bg-gray-200" />
              <div className="space-y-4">
                {timeline.map((item, i) => (
                  <div key={`${item.type}-${i}`} className="flex gap-4 relative">
                    <span className="w-8 h-8 rounded-full bg-white border-2 border-gray-100 flex items-center justify-center text-sm shrink-0 z-10">
                      {item.icon}
                    </span>
                    <div className="flex-1 pb-2">
                      <div className="flex justify-between items-start gap-2">
                        <p className="text-sm font-medium text-gray-900">{item.title}</p>
                        <span className="text-[10px] text-gray-400 shrink-0">{formatRelativeDate(item.date)}</span>
                      </div>
                      <p className="text-xs text-gray-500 mt-0.5">{item.subtitle}</p>
                      {'revenue' in item && item.revenue && (
                        <p className="text-xs text-green-600 mt-1">{formatINR(Number(item.revenue))}</p>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </Card>
        </>
      )}
    </div>
  );
}
