'use client';

import { useEffect, useState } from 'react';
import api from '@/lib/api';
import { useAuthStore } from '@/lib/auth';
import { Card } from '@/components/ui/Card';
import { Button } from '@/components/ui/Button';
import { Select } from '@/components/ui/Select';
import { Input } from '@/components/ui/Input';
import { TextArea } from '@/components/ui/TextArea';
import { FormSection } from '@/components/ui/FormSection';
import { cleanPayload } from '@/lib/form';
import { PageHeader } from '@/components/ui/PageHeader';
import { Alert } from '@/components/ui/Alert';
import { Spinner } from '@/components/ui/Spinner';
import { EmptyState } from '@/components/ui/EmptyState';
import { LIFECYCLE_FLOW, formatStatus, getDemoTransitionOptions, getRecommendedNext, canTransitionLifecycle } from '@/lib/lifecycle';
import { formatINR } from '@/lib/format';
import { MetricCard } from '@/components/ui/MetricCard';

interface Opportunity {
  id: string;
  opportunity_name: string;
  current_status: string;
  expected_revenue?: number;
  quotation_value?: number;
  probability_of_conversion?: number;
  follow_up_date?: string;
  remarks?: string;
}

interface LifecycleEntry {
  previous_status?: string;
  new_status: string;
  changed_at: string;
  remarks?: string;
}

interface Ownership {
  lead_creator_id?: string;
  marketing_owner_id?: string;
  sales_owner_id?: string;
  revenue_credit?: number;
}

export default function OpportunitiesPage() {
  const { user } = useAuthStore();
  const [opportunities, setOpportunities] = useState<Opportunity[]>([]);
  const [selected, setSelected] = useState<Opportunity | null>(null);
  const [history, setHistory] = useState<LifecycleEntry[]>([]);
  const [loading, setLoading] = useState(true);
  const [transitioning, setTransitioning] = useState(false);
  const [newStatus, setNewStatus] = useState('');
  const [remarks, setRemarks] = useState('');
  const [savingDeal, setSavingDeal] = useState(false);
  const [dealForm, setDealForm] = useState({
    expected_revenue: '',
    quotation_value: '',
    probability_of_conversion: '',
    follow_up_date: '',
    remarks: '',
  });
  const [ownership, setOwnership] = useState<Ownership | null>(null);
  const [transferring, setTransferring] = useState(false);
  const [transferForm, setTransferForm] = useState({
    expected_visit_date: '',
    expected_quantity: '',
    priority: 'high',
    builder_name: '',
    architect_name: '',
    remarks: '',
  });
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  const load = async () => {
    try {
      const { data } = await api.get('/opportunities');
      setOpportunities(data);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to load pipeline');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { load(); }, []);

  const selectOpportunity = async (opp: Opportunity) => {
    setSelected(opp);
    setNewStatus(opp.current_status);
    setDealForm({
      expected_revenue: opp.expected_revenue ? String(opp.expected_revenue) : '',
      quotation_value: opp.quotation_value ? String(opp.quotation_value) : '',
      probability_of_conversion: opp.probability_of_conversion ? String(opp.probability_of_conversion) : '',
      follow_up_date: opp.follow_up_date ? new Date(opp.follow_up_date).toISOString().slice(0, 16) : '',
      remarks: opp.remarks || '',
    });
    setError('');
    try {
      const [histRes, ownRes] = await Promise.all([
        api.get(`/opportunities/${opp.id}/history`),
        api.get(`/opportunities/${opp.id}/ownership`),
      ]);
      setHistory(histRes.data);
      setOwnership(ownRes.data);
    } catch {
      setHistory([]);
      setOwnership(null);
    }
  };

  const handleLeadTransfer = async () => {
    if (!selected || !transferForm.expected_visit_date) return;
    setTransferring(true);
    setError('');
    setSuccess('');
    try {
      const { data } = await api.post(`/opportunities/${selected.id}/lead-transfer`, cleanPayload({
        ...transferForm,
        expected_visit_date: new Date(transferForm.expected_visit_date).toISOString(),
        expected_quantity: transferForm.expected_quantity ? Number(transferForm.expected_quantity) : undefined,
      }));
      setSelected(data);
      setOpportunities((prev) => prev.map((o) => (o.id === data.id ? { ...o, ...data } : o)));
      setSuccess('Lead transferred to sales — pipeline advanced to Showroom Visit Scheduled');
      const { data: hist } = await api.get(`/opportunities/${selected.id}/history`);
      setHistory(hist);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Lead transfer failed');
    } finally {
      setTransferring(false);
    }
  };

  const handleSaveDeal = async () => {
    if (!selected) return;
    setSavingDeal(true);
    setError('');
    setSuccess('');
    try {
      const payload = cleanPayload({
        expected_revenue: dealForm.expected_revenue ? Number(dealForm.expected_revenue) : undefined,
        quotation_value: dealForm.quotation_value ? Number(dealForm.quotation_value) : undefined,
        probability_of_conversion: dealForm.probability_of_conversion ? Number(dealForm.probability_of_conversion) : undefined,
        follow_up_date: dealForm.follow_up_date ? new Date(dealForm.follow_up_date).toISOString() : undefined,
        remarks: dealForm.remarks,
      });
      const { data } = await api.patch(`/opportunities/${selected.id}`, payload);
      setSelected(data);
      setOpportunities((prev) => prev.map((o) => (o.id === data.id ? { ...o, ...data } : o)));
      setSuccess('Deal details updated');
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to update deal');
    } finally {
      setSavingDeal(false);
    }
  };

  const handleTransition = async () => {
    if (!selected || !user) return;
    setTransitioning(true);
    setError('');
    setSuccess('');
    try {
      await api.post(`/opportunities/${selected.id}/transition`, { new_status: newStatus, remarks });
      setSuccess(`Moved to ${formatStatus(newStatus)}`);
      setSelected({ ...selected, current_status: newStatus });
      setOpportunities((prev) => prev.map((o) => (o.id === selected.id ? { ...o, current_status: newStatus } : o)));
      const { data } = await api.get(`/opportunities/${selected.id}/history`);
      setHistory(data);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Transition failed');
    } finally {
      setTransitioning(false);
    }
  };

  const transitionOptions = selected && user
    ? getDemoTransitionOptions(selected.current_status, user.role)
    : [];

  const totalValue = opportunities.reduce((s, o) => s + Number(o.expected_revenue || 0), 0);
  const confirmed = opportunities.filter((o) => o.current_status === 'order_confirmed').length;
  const inProgress = opportunities.filter((o) => o.current_status !== 'lost' && o.current_status !== 'order_confirmed').length;

  return (
    <div className="space-y-6">
      <PageHeader title="Opportunity Pipeline" subtitle="Track and advance sales opportunities" />

      {error && <Alert type="error">{error}</Alert>}
      {success && <Alert type="success">{success}</Alert>}

      {!loading && opportunities.length > 0 && (
        <div className="grid grid-cols-3 gap-3">
          <MetricCard label="Active Deals" value={inProgress} subtitle={`${opportunities.length} total`} accent="blue" />
          <MetricCard label="Pipeline Value" value={formatINR(totalValue)} subtitle="Expected revenue" accent="green" />
          <MetricCard label="Confirmed" value={confirmed} subtitle="Orders closed" accent="purple" />
        </div>
      )}

      {loading ? (
        <div className="flex justify-center py-12"><Spinner /></div>
      ) : (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
          <Card title="Pipeline">
            {opportunities.length === 0 ? (
              <EmptyState icon="pipeline" title="No opportunities yet" message="Field executives create opportunities when capturing new sites from the field." />
            ) : (
              <div className="space-y-2">
                {opportunities.map((opp) => (
                  <button
                    key={opp.id}
                    type="button"
                    onClick={() => selectOpportunity(opp)}
                    className={`w-full text-left rounded-xl p-4 border transition-colors ${
                      selected?.id === opp.id ? 'border-[#0071e3] bg-blue-50/50' : 'border-gray-100 hover:bg-gray-50'
                    }`}
                  >
                    <p className="font-medium text-sm">{opp.opportunity_name}</p>
                    <span className="demo-badge bg-indigo-100 text-indigo-700 mt-2 inline-block">{formatStatus(opp.current_status)}</span>
                    {opp.expected_revenue && (
                      <p className="text-xs text-gray-400 mt-1">₹{Number(opp.expected_revenue).toLocaleString('en-IN')}</p>
                    )}
                  </button>
                ))}
              </div>
            )}
          </Card>

          {selected && (
            <Card title="Detail">
              <h3 className="font-medium mb-4">{selected.opportunity_name}</h3>

              <div className="flex flex-wrap gap-1 mb-6">
                {LIFECYCLE_FLOW.map((step) => {
                  const idx = LIFECYCLE_FLOW.indexOf(selected.current_status as typeof LIFECYCLE_FLOW[number]);
                  const stepIdx = LIFECYCLE_FLOW.indexOf(step);
                  const isCurrent = step === selected.current_status;
                  const isPast = stepIdx < idx;
                  return (
                    <span
                      key={step}
                      className={`text-[10px] px-2 py-1 rounded-full ${
                        isCurrent ? 'bg-[#0071e3] text-white font-medium' :
                        isPast ? 'bg-green-100 text-green-700' : 'bg-gray-100 text-gray-400'
                      }`}
                    >
                      {formatStatus(step)}
                    </span>
                  );
                })}
              </div>

              {ownership && (
                <div className="mb-6 p-4 bg-indigo-50/50 rounded-xl border border-indigo-100">
                  <p className="text-xs font-medium text-gray-500 mb-2">Lead Ownership Model</p>
                  <div className="grid grid-cols-3 gap-2 text-xs">
                    <div><p className="text-gray-400">Creator</p><p className="font-medium truncate">{ownership.lead_creator_id?.slice(0, 8) || '—'}</p></div>
                    <div><p className="text-gray-400">Marketing</p><p className="font-medium truncate">{ownership.marketing_owner_id?.slice(0, 8) || '—'}</p></div>
                    <div><p className="text-gray-400">Sales</p><p className="font-medium truncate">{ownership.sales_owner_id?.slice(0, 8) || '—'}</p></div>
                  </div>
                  {ownership.revenue_credit != null && (
                    <p className="text-xs text-gray-500 mt-2">Revenue credit: {ownership.revenue_credit}%</p>
                  )}
                </div>
              )}

              {(user?.role === 'marketing_executive' || user?.role === 'manager') && (
                <FormSection title="Lead Transfer to Sales">
                  <p className="text-xs text-gray-500 -mt-2 mb-2">Hand off a qualified lead — auto-assigns sales owner and advances pipeline.</p>
                  <div className="grid grid-cols-2 gap-3">
                    <Input label="Expected Showroom Visit *" type="datetime-local" value={transferForm.expected_visit_date} onChange={(e) => setTransferForm({ ...transferForm, expected_visit_date: e.target.value })} />
                    <Input label="Expected Quantity (sq.ft)" type="number" value={transferForm.expected_quantity} onChange={(e) => setTransferForm({ ...transferForm, expected_quantity: e.target.value })} />
                    <Input label="Builder Name" value={transferForm.builder_name} onChange={(e) => setTransferForm({ ...transferForm, builder_name: e.target.value })} />
                    <Input label="Architect Name" value={transferForm.architect_name} onChange={(e) => setTransferForm({ ...transferForm, architect_name: e.target.value })} />
                  </div>
                  <Select label="Priority" value={transferForm.priority} onChange={(e) => setTransferForm({ ...transferForm, priority: e.target.value })}>
                    <option value="high">High</option>
                    <option value="medium">Medium</option>
                    <option value="low">Low</option>
                  </Select>
                  <TextArea label="Transfer Notes" value={transferForm.remarks} onChange={(e) => setTransferForm({ ...transferForm, remarks: e.target.value })} placeholder="Client expectations, urgency, competitor context..." />
                  <Button variant="secondary" size="sm" onClick={handleLeadTransfer} disabled={transferring || !transferForm.expected_visit_date}>
                    {transferring ? 'Transferring...' : 'Transfer Lead to Sales'}
                  </Button>
                </FormSection>
              )}

              <FormSection title="Deal Intelligence">
                <div className="grid grid-cols-2 gap-3">
                  <Input label="Expected Revenue (₹)" type="number" value={dealForm.expected_revenue} onChange={(e) => setDealForm({ ...dealForm, expected_revenue: e.target.value })} />
                  <Input label="Quotation Value (₹)" type="number" value={dealForm.quotation_value} onChange={(e) => setDealForm({ ...dealForm, quotation_value: e.target.value })} />
                  <Input label="Conversion Probability (%)" type="number" min="0" max="100" value={dealForm.probability_of_conversion} onChange={(e) => setDealForm({ ...dealForm, probability_of_conversion: e.target.value })} />
                  <Input label="Follow-up Date" type="datetime-local" value={dealForm.follow_up_date} onChange={(e) => setDealForm({ ...dealForm, follow_up_date: e.target.value })} />
                </div>
                <TextArea label="Opportunity Remarks" value={dealForm.remarks} onChange={(e) => setDealForm({ ...dealForm, remarks: e.target.value })} placeholder="Negotiation notes, client constraints, competitor pricing..." />
                <Button variant="secondary" size="sm" onClick={handleSaveDeal} disabled={savingDeal}>
                  {savingDeal ? 'Saving...' : 'Save Deal Details'}
                </Button>
              </FormSection>

              {user && canTransitionLifecycle(user.role) && (
                <div className="space-y-3 mb-6 p-4 bg-gray-50 rounded-xl">
                  {user.role === 'sales_executive' && getRecommendedNext(selected.current_status, user.role) && (
                    <p className="text-xs text-gray-500">
                      Tip: jump ahead to <span className="font-medium text-[#0071e3]">{formatStatus(getRecommendedNext(selected.current_status, user.role)!)}</span> or any later sales stage.
                    </p>
                  )}
                  <Select label="Move to" value={newStatus} onChange={(e) => setNewStatus(e.target.value)}>
                    {transitionOptions.map((s) => (
                      <option key={s} value={s}>{formatStatus(s)}</option>
                    ))}
                  </Select>
                  <Input label="Transition Remarks" placeholder="Reason for status change" value={remarks} onChange={(e) => setRemarks(e.target.value)} />
                  <Button
                    onClick={handleTransition}
                    disabled={transitioning || newStatus === selected.current_status}
                    className="w-full"
                  >
                    {transitioning ? 'Updating...' : 'Update Status'}
                  </Button>
                </div>
              )}

              <h4 className="text-sm font-medium text-gray-700 mb-2">History</h4>
              {history.length === 0 ? (
                <p className="text-sm text-gray-400">No transitions recorded yet.</p>
              ) : (
                <div className="space-y-2">
                  {history.map((h, i) => (
                    <div key={i} className="text-sm border-l-2 border-[#0071e3]/30 pl-3 py-1">
                      <p>{formatStatus(h.previous_status || 'start')} → {formatStatus(h.new_status)}</p>
                      <p className="text-xs text-gray-400">{new Date(h.changed_at).toLocaleString()}</p>
                    </div>
                  ))}
                </div>
              )}
            </Card>
          )}
        </div>
      )}
    </div>
  );
}
