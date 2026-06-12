'use client';

import { useEffect, useState } from 'react';
import api from '@/lib/api';
import { captureGeolocation } from '@/lib/geolocation';
import { cleanPayload } from '@/lib/form';
import {
  MET_WITH_OPTIONS,
  MEETING_CATEGORIES,
  RELATIONSHIP_STAGES,
  metWithLabel,
  relationshipStageLabel,
  meetingTypeLabel,
} from '@/lib/meeting';
import { Card } from '@/components/ui/Card';
import { Button } from '@/components/ui/Button';
import { Input } from '@/components/ui/Input';
import { TextArea } from '@/components/ui/TextArea';
import { Select } from '@/components/ui/Select';
import { FormSection } from '@/components/ui/FormSection';
import { PageHeader } from '@/components/ui/PageHeader';
import { Alert } from '@/components/ui/Alert';
import { Spinner } from '@/components/ui/Spinner';
import { EmptyState } from '@/components/ui/EmptyState';
import { fetchSitesLookup, fetchMeetings, siteLookupMap } from '@/lib/query';

interface Meeting {
  id: string;
  site_id: string;
  met_with?: string;
  stakeholder_name: string;
  stakeholder_mobile?: string;
  firm_name?: string;
  address?: string;
  area?: string;
  city?: string;
  category?: string;
  relationship_stage?: string;
  meeting_date: string;
  meeting_type?: string;
  summary?: string;
  influence_score?: number;
  opportunity_score?: number;
  loyalty_score?: number;
  showroom_visit_commitment?: boolean;
  time_spent_minutes?: number;
  follow_up_date?: string;
}

interface Site {
  id: string;
  site_name: string;
}

const EMPTY_FORM = {
  site_id: '',
  meeting_date: '',
  meeting_type: 'site_visit',
  met_with: 'builder',
  stakeholder_name: '',
  stakeholder_mobile: '',
  firm_name: '',
  address: '',
  area: '',
  city: 'Gurgaon',
  category: 'B',
  relationship_stage: 'rapport_building',
  summary: '',
  influence_score: '',
  opportunity_score: '',
  loyalty_score: '',
  showroom_visit_commitment: false,
  time_spent_minutes: '',
  current_requirement: '',
  estimated_project_size: '',
  latitude: '',
  longitude: '',
  follow_up_date: '',
  remarks: '',
};

function stakeholderFromDetail(detail: any, metWith: string) {
  const sh = detail.stakeholders || {};
  const site = detail;
  if (metWith === 'owner') {
    return {
      stakeholder_name: sh.owner_name || '',
      stakeholder_mobile: sh.owner_mobile || '',
      firm_name: '',
      address: sh.owner_address || '',
      area: site.area || '',
      city: site.city || 'Gurgaon',
      category: 'A',
    };
  }
  if (metWith === 'builder') {
    return {
      stakeholder_name: sh.builder_name || '',
      stakeholder_mobile: sh.builder_mobile || '',
      firm_name: sh.builder_firm_name || '',
      address: '',
      area: site.area || '',
      city: site.city || 'Gurgaon',
      category: sh.builder_category || 'A',
    };
  }
  if (metWith === 'architect') {
    return {
      stakeholder_name: sh.architect_name || '',
      stakeholder_mobile: sh.architect_mobile || '',
      firm_name: sh.architect_firm_name || '',
      address: '',
      area: site.area || '',
      city: site.city || 'Gurgaon',
      category: sh.architect_category || 'B',
    };
  }
  const contact = (detail.contacts || []).find((c: any) => c.contact_type === metWith);
  if (contact) {
    return {
      stakeholder_name: contact.name || '',
      stakeholder_mobile: contact.mobile_number || '',
      firm_name: contact.firm_name || '',
      address: contact.address || '',
      area: site.area || '',
      city: site.city || 'Gurgaon',
      category: contact.category || 'C',
    };
  }
  return { area: site.area || '', city: site.city || 'Gurgaon' };
}

export default function MeetingsPage() {
  const [meetings, setMeetings] = useState<Meeting[]>([]);
  const [sites, setSites] = useState<Site[]>([]);
  const [siteMap, setSiteMap] = useState<Record<string, string>>({});
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [capturingGps, setCapturingGps] = useState(false);
  const [prefilling, setPrefilling] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [form, setForm] = useState(EMPTY_FORM);

  useEffect(() => {
    Promise.all([fetchMeetings(), fetchSitesLookup()])
      .then(([m, s]) => {
        setMeetings(m);
        setSites(s);
        setSiteMap(siteLookupMap(s));
      })
      .catch((err) => setError(err.response?.data?.detail || 'Failed to load'))
      .finally(() => setLoading(false));
  }, []);

  const prefillStakeholder = async (siteId: string, metWith: string) => {
    if (!siteId || !metWith) return;
    setPrefilling(true);
    try {
      const { data } = await api.get(`/sites/${siteId}/detail`);
      const fields = stakeholderFromDetail(data, metWith);
      setForm((f) => ({ ...f, ...fields }));
    } catch {
      /* keep manual entry */
    } finally {
      setPrefilling(false);
    }
  };

  const handleSiteChange = (siteId: string) => {
    setForm((f) => ({ ...f, site_id: siteId }));
    if (siteId && form.met_with) prefillStakeholder(siteId, form.met_with);
  };

  const handleMetWithChange = (metWith: string) => {
    setForm((f) => ({ ...f, met_with: metWith }));
    if (form.site_id) prefillStakeholder(form.site_id, metWith);
  };

  const captureGps = () => {
    setCapturingGps(true);
    captureGeolocation().then((coords) => {
      setForm((f) => ({ ...f, ...coords }));
      setCapturingGps(false);
    });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setSubmitting(true);
    setError('');
    setSuccess('');
    try {
      const payload = cleanPayload({
        ...form,
        meeting_date: new Date(form.meeting_date).toISOString(),
        follow_up_date: form.follow_up_date ? new Date(form.follow_up_date).toISOString() : undefined,
        influence_score: form.influence_score ? Number(form.influence_score) : undefined,
        opportunity_score: form.opportunity_score ? Number(form.opportunity_score) : undefined,
        loyalty_score: form.loyalty_score ? Number(form.loyalty_score) : undefined,
        time_spent_minutes: form.time_spent_minutes ? Number(form.time_spent_minutes) : undefined,
        estimated_project_size: form.estimated_project_size ? Number(form.estimated_project_size) : undefined,
        showroom_visit_commitment: form.showroom_visit_commitment,
      });
      const { data } = await api.post('/meetings', payload);
      setMeetings([data, ...meetings]);
      setShowForm(false);
      setForm(EMPTY_FORM);
      setSuccess(
        form.showroom_visit_commitment
          ? 'Meeting recorded — pipeline auto-advanced to Showroom Visit Scheduled'
          : 'Meeting recorded — pipeline advanced to Relationship Building'
      );
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to save meeting');
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-start gap-4">
        <PageHeader title="Meetings" subtitle="PDF-complete stakeholder meetings — met with, firm, location, category & relationship stage" />
        <Button onClick={() => setShowForm(!showForm)} size="sm">{showForm ? 'Cancel' : '+ Record'}</Button>
      </div>

      {error && <Alert type="error">{error}</Alert>}
      {success && <Alert type="success">{success}</Alert>}

      {showForm && (
        <Card title="New Meeting">
          <form onSubmit={handleSubmit} className="space-y-5">
            <FormSection title="Meeting Details">
              <Select label="Site *" value={form.site_id} onChange={(e) => handleSiteChange(e.target.value)} required>
                <option value="">Select site</option>
                {sites.map((s) => <option key={s.id} value={s.id}>{s.site_name}</option>)}
              </Select>
              <div className="grid grid-cols-2 gap-4">
                <Select label="Channel (How)" value={form.meeting_type} onChange={(e) => setForm({ ...form, meeting_type: e.target.value })}>
                  <option value="site_visit">Site Visit</option>
                  <option value="office_visit">Office Visit</option>
                  <option value="phone_call">Phone Call</option>
                  <option value="video_call">Video Call</option>
                </Select>
                <Input label="Date & Time *" type="datetime-local" value={form.meeting_date} onChange={(e) => setForm({ ...form, meeting_date: e.target.value })} required />
              </div>
              <Input label="Time Spent (minutes)" type="number" value={form.time_spent_minutes} onChange={(e) => setForm({ ...form, time_spent_minutes: e.target.value })} placeholder="e.g. 45" />
            </FormSection>

            <FormSection title="Person Met (PDF)">
              <Select
                label="Met With *"
                value={form.met_with}
                onChange={(e) => handleMetWithChange(e.target.value)}
                required
              >
                {MET_WITH_OPTIONS.map((o) => <option key={o.value} value={o.value}>{o.label}</option>)}
              </Select>
              {prefilling && <p className="text-xs text-gray-400">Loading stakeholder from site...</p>}
              <div className="grid grid-cols-2 gap-4">
                <Input label="Person Name *" value={form.stakeholder_name} onChange={(e) => setForm({ ...form, stakeholder_name: e.target.value })} placeholder="e.g. Ravi Mehta" required />
                <Input label="Contact Number" type="tel" value={form.stakeholder_mobile} onChange={(e) => setForm({ ...form, stakeholder_mobile: e.target.value })} placeholder="9812345678" />
              </div>
              <Input label="Firm Name" value={form.firm_name} onChange={(e) => setForm({ ...form, firm_name: e.target.value })} placeholder="e.g. Mehta Constructions" />
              <Input label="Address" value={form.address} onChange={(e) => setForm({ ...form, address: e.target.value })} />
              <div className="grid grid-cols-2 gap-4">
                <Input label="Area" value={form.area} onChange={(e) => setForm({ ...form, area: e.target.value })} />
                <Input label="City" value={form.city} onChange={(e) => setForm({ ...form, city: e.target.value })} />
              </div>
              <div className="grid grid-cols-2 gap-4">
                <Select label="Category (A–D)" value={form.category} onChange={(e) => setForm({ ...form, category: e.target.value })}>
                  {MEETING_CATEGORIES.map((c) => <option key={c.value} value={c.value}>{c.label}</option>)}
                </Select>
                <Select label="Relationship Stage *" value={form.relationship_stage} onChange={(e) => setForm({ ...form, relationship_stage: e.target.value })} required>
                  {RELATIONSHIP_STAGES.map((s) => <option key={s.value} value={s.value}>{s.label}</option>)}
                </Select>
              </div>
            </FormSection>

            <FormSection title="Relationship Scores (1–10)">
              <div className="grid grid-cols-3 gap-4">
                <Input label="Influence" type="number" min="1" max="10" step="0.1" value={form.influence_score} onChange={(e) => setForm({ ...form, influence_score: e.target.value })} />
                <Input label="Opportunity" type="number" min="1" max="10" step="0.1" value={form.opportunity_score} onChange={(e) => setForm({ ...form, opportunity_score: e.target.value })} />
                <Input label="Loyalty" type="number" min="1" max="10" step="0.1" value={form.loyalty_score} onChange={(e) => setForm({ ...form, loyalty_score: e.target.value })} />
              </div>
            </FormSection>

            <FormSection title="Requirements">
              <TextArea label="Current Requirement" value={form.current_requirement} onChange={(e) => setForm({ ...form, current_requirement: e.target.value })} placeholder="Marble for lobby, bathrooms..." />
              <Input label="Estimated Project Size (sq.ft)" type="number" value={form.estimated_project_size} onChange={(e) => setForm({ ...form, estimated_project_size: e.target.value })} />
            </FormSection>

            <FormSection title="Discussion">
              <TextArea label="Meeting Summary" value={form.summary} onChange={(e) => setForm({ ...form, summary: e.target.value })} placeholder="Requirements discussed, materials shown..." />
              <TextArea label="Meeting Remarks" value={form.remarks} onChange={(e) => setForm({ ...form, remarks: e.target.value })} placeholder="Internal notes" />
            </FormSection>

            <FormSection title="Location & Follow-Up">
              <div className="grid grid-cols-2 gap-4">
                <Input label="Latitude" value={form.latitude} readOnly placeholder="Auto-captured" />
                <Input label="Longitude" value={form.longitude} readOnly placeholder="Auto-captured" />
              </div>
              <Button type="button" variant="secondary" size="sm" onClick={captureGps} disabled={capturingGps}>
                {capturingGps ? 'Capturing GPS...' : '📍 Capture Meeting GPS'}
              </Button>
              <Input label="Next Follow-up Date" type="datetime-local" value={form.follow_up_date} onChange={(e) => setForm({ ...form, follow_up_date: e.target.value })} />
              <label className="flex items-center gap-2 text-sm text-gray-700">
                <input type="checkbox" checked={form.showroom_visit_commitment} onChange={(e) => setForm({ ...form, showroom_visit_commitment: e.target.checked })} className="rounded" />
                Client committed to showroom visit (auto-advances pipeline)
              </label>
            </FormSection>

            <Button type="submit" disabled={submitting}>{submitting ? 'Saving...' : 'Save Meeting'}</Button>
          </form>
        </Card>
      )}

      <Card title="History">
        {loading ? (
          <div className="flex justify-center py-8"><Spinner /></div>
        ) : meetings.length === 0 ? (
          <EmptyState icon="meetings" title="No meetings yet" message="Record site visits, calls, and client interactions to build relationship history." />
        ) : (
          <div className="space-y-3">
            {meetings.map((m) => (
              <div key={m.id} className="py-3 border-b border-gray-100 last:border-0">
                <div className="flex items-start justify-between gap-2">
                  <div>
                    <p className="font-medium">{m.stakeholder_name}</p>
                    {m.firm_name && <p className="text-xs text-gray-500">{m.firm_name}</p>}
                  </div>
                  <div className="flex flex-wrap gap-1 justify-end shrink-0">
                    {m.met_with && <span className="demo-badge bg-indigo-50 text-indigo-700">{metWithLabel(m.met_with)}</span>}
                    {m.category && <span className="demo-badge bg-gray-100 text-gray-600">Cat {m.category}</span>}
                    {m.relationship_stage && (
                      <span className="demo-badge bg-purple-50 text-purple-700">{relationshipStageLabel(m.relationship_stage)}</span>
                    )}
                  </div>
                </div>
                <p className="text-sm text-gray-500">
                  {siteMap[m.site_id] || 'Site'} · {meetingTypeLabel(m.meeting_type)} · {new Date(m.meeting_date).toLocaleString()}
                </p>
                {(m.address || m.area || m.city) && (
                  <p className="text-xs text-gray-400 mt-0.5">
                    {[m.address, m.area, m.city].filter(Boolean).join(', ')}
                  </p>
                )}
                {(m.influence_score || m.opportunity_score) && (
                  <p className="text-xs text-gray-400 mt-1">
                    Scores: Inf {m.influence_score ?? '—'} · Opp {m.opportunity_score ?? '—'} · Loy {m.loyalty_score ?? '—'}
                  </p>
                )}
                {m.showroom_visit_commitment && <span className="demo-badge bg-green-50 text-green-700 mt-1 inline-block">Showroom committed</span>}
                {m.summary && <p className="text-sm text-gray-400 mt-1">{m.summary}</p>}
                {m.follow_up_date && (
                  <p className="text-xs text-[#0071e3] mt-1">Follow-up: {new Date(m.follow_up_date).toLocaleDateString('en-IN')}</p>
                )}
              </div>
            ))}
          </div>
        )}
      </Card>
    </div>
  );
}
