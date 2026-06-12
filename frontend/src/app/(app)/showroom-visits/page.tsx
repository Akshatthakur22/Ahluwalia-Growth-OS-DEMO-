'use client';

import { useEffect, useState } from 'react';
import api from '@/lib/api';
import { cleanPayload } from '@/lib/form';
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
import { fetchSitesLookup, siteLookupMap } from '@/lib/query';

interface Visit {
  id: string;
  site_id: string;
  visit_date: string;
  client_name?: string;
  selected_material?: string;
  estimated_quantity?: number;
  lead_temperature?: string;
  quotation_required: boolean;
  expected_purchase_date?: string;
  remarks?: string;
}

interface Site {
  id: string;
  site_name: string;
}

const MATERIALS = [
  'Italian Carrara Marble',
  'Turkish Emperador Dark',
  'Indian Makrana White',
  'Brazilian Quartzite',
  'Spanish Crema Marfil',
  'Engineered Quartz — Calacatta',
  'Black Galaxy Granite',
  'Statuario Marble',
];

const EMPTY_FORM = {
  site_id: '',
  visit_date: '',
  client_name: '',
  client_mobile: '',
  client_address: '',
  client_area: '',
  client_city: 'Ambala',
  project_type: 'residential',
  project_size: '',
  architect_name: '',
  builder_name: '',
  selected_material: 'Italian Carrara Marble',
  estimated_quantity: '',
  lead_temperature: 'warm',
  lead_source: 'site_referral',
  referral_name: '',
  referral_contact: '',
  time_spent_minutes: '',
  presentation_shared: false,
  video_3d_shared: false,
  quotation_required: true,
  expected_purchase_date: '',
  follow_up_date: '',
  remarks: '',
};

export default function ShowroomVisitsPage() {
  const [visits, setVisits] = useState<Visit[]>([]);
  const [sites, setSites] = useState<Site[]>([]);
  const [siteMap, setSiteMap] = useState<Record<string, string>>({});
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [form, setForm] = useState(EMPTY_FORM);

  useEffect(() => {
    Promise.all([api.get('/showroom-visits'), fetchSitesLookup()])
      .then(([v, s]) => {
        setVisits(v.data);
        setSites(s);
        setSiteMap(siteLookupMap(s));
      })
      .catch((err) => setError(err.response?.data?.detail || 'Failed to load'))
      .finally(() => setLoading(false));
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setSubmitting(true);
    setError('');
    setSuccess('');
    try {
      const payload = cleanPayload({
        ...form,
        visit_date: new Date(form.visit_date).toISOString(),
        project_size: form.project_size ? Number(form.project_size) : undefined,
        estimated_quantity: form.estimated_quantity ? Number(form.estimated_quantity) : undefined,
        time_spent_minutes: form.time_spent_minutes ? Number(form.time_spent_minutes) : undefined,
        expected_purchase_date: form.expected_purchase_date ? new Date(form.expected_purchase_date).toISOString() : undefined,
        follow_up_date: form.follow_up_date ? new Date(form.follow_up_date).toISOString() : undefined,
        quotation_required: form.quotation_required,
        presentation_shared: form.presentation_shared,
        video_3d_shared: form.video_3d_shared,
      });
      const { data } = await api.post('/showroom-visits', payload);
      setVisits([data, ...visits]);
      setShowForm(false);
      setForm(EMPTY_FORM);
      setSuccess(
        form.quotation_required
          ? 'Visit logged — pipeline auto-advanced to Selection Done'
          : 'Visit logged — pipeline auto-advanced to Showroom Visit Done'
      );
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to save visit');
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-start gap-4">
        <PageHeader title="Showroom Visits" subtitle="Full CRM visit log — client intel, materials, lead temperature" />
        <Button onClick={() => setShowForm(!showForm)} size="sm">{showForm ? 'Cancel' : '+ Record'}</Button>
      </div>

      {error && <Alert type="error">{error}</Alert>}
      {success && <Alert type="success">{success}</Alert>}

      {showForm && (
        <Card title="New Showroom Visit">
          <form onSubmit={handleSubmit} className="space-y-5">
            <FormSection title="Visit Details">
              <Select label="Linked Site *" value={form.site_id} onChange={(e) => setForm({ ...form, site_id: e.target.value })} required>
                <option value="">Select site</option>
                {sites.map((s) => <option key={s.id} value={s.id}>{s.site_name}</option>)}
              </Select>
              <Input label="Visit Date & Time *" type="datetime-local" value={form.visit_date} onChange={(e) => setForm({ ...form, visit_date: e.target.value })} required />
              <Input label="Time Spent (minutes)" type="number" value={form.time_spent_minutes} onChange={(e) => setForm({ ...form, time_spent_minutes: e.target.value })} />
            </FormSection>

            <FormSection title="Client Profile">
              <div className="grid grid-cols-2 gap-4">
                <Input label="Client Name" value={form.client_name} onChange={(e) => setForm({ ...form, client_name: e.target.value })} />
                <Input label="Client Mobile" type="tel" value={form.client_mobile} onChange={(e) => setForm({ ...form, client_mobile: e.target.value })} />
              </div>
              <Input label="Address" value={form.client_address} onChange={(e) => setForm({ ...form, client_address: e.target.value })} />
              <div className="grid grid-cols-2 gap-4">
                <Input label="Area" value={form.client_area} onChange={(e) => setForm({ ...form, client_area: e.target.value })} />
                <Input label="City" value={form.client_city} onChange={(e) => setForm({ ...form, client_city: e.target.value })} />
              </div>
            </FormSection>

            <FormSection title="Project Context">
              <div className="grid grid-cols-2 gap-4">
                <Select label="Project Type" value={form.project_type} onChange={(e) => setForm({ ...form, project_type: e.target.value })}>
                  <option value="residential">Residential</option>
                  <option value="commercial">Commercial</option>
                  <option value="industrial">Industrial</option>
                </Select>
                <Input label="Project Size (sq.ft)" type="number" value={form.project_size} onChange={(e) => setForm({ ...form, project_size: e.target.value })} />
              </div>
              <div className="grid grid-cols-2 gap-4">
                <Input label="Architect Name" value={form.architect_name} onChange={(e) => setForm({ ...form, architect_name: e.target.value })} />
                <Input label="Builder Name" value={form.builder_name} onChange={(e) => setForm({ ...form, builder_name: e.target.value })} />
              </div>
            </FormSection>

            <FormSection title="Material Selection">
              <Select label="Selected Material" value={form.selected_material} onChange={(e) => setForm({ ...form, selected_material: e.target.value })}>
                {MATERIALS.map((m) => <option key={m} value={m}>{m}</option>)}
              </Select>
              <Input label="Quantity Required (sq.ft)" type="number" value={form.estimated_quantity} onChange={(e) => setForm({ ...form, estimated_quantity: e.target.value })} placeholder="e.g. 500" />
            </FormSection>

            <FormSection title="Lead Intelligence">
              <div className="grid grid-cols-2 gap-4">
                <Select label="Lead Temperature" value={form.lead_temperature} onChange={(e) => setForm({ ...form, lead_temperature: e.target.value })}>
                  <option value="hot">Hot</option>
                  <option value="warm">Warm</option>
                  <option value="cold">Cold</option>
                </Select>
                <Select label="Lead Source" value={form.lead_source} onChange={(e) => setForm({ ...form, lead_source: e.target.value })}>
                  <option value="site_referral">Site Referral</option>
                  <option value="walk_in">Walk-in</option>
                  <option value="architect">Architect</option>
                  <option value="builder">Builder</option>
                  <option value="repeat_client">Repeat Client</option>
                </Select>
              </div>
              <div className="grid grid-cols-2 gap-4">
                <Input label="Referral Name" value={form.referral_name} onChange={(e) => setForm({ ...form, referral_name: e.target.value })} />
                <Input label="Referral Contact" type="tel" value={form.referral_contact} onChange={(e) => setForm({ ...form, referral_contact: e.target.value })} />
              </div>
            </FormSection>

            <FormSection title="Sales Follow-Up">
              <div className="flex flex-wrap gap-4 text-sm text-gray-700">
                <label className="flex items-center gap-2">
                  <input type="checkbox" checked={form.presentation_shared} onChange={(e) => setForm({ ...form, presentation_shared: e.target.checked })} className="rounded" />
                  Presentation shared
                </label>
                <label className="flex items-center gap-2">
                  <input type="checkbox" checked={form.video_3d_shared} onChange={(e) => setForm({ ...form, video_3d_shared: e.target.checked })} className="rounded" />
                  3D video shared
                </label>
                <label className="flex items-center gap-2">
                  <input type="checkbox" checked={form.quotation_required} onChange={(e) => setForm({ ...form, quotation_required: e.target.checked })} className="rounded" />
                  Quotation required
                </label>
              </div>
              <Input label="Expected Purchase Timeline" type="datetime-local" value={form.expected_purchase_date} onChange={(e) => setForm({ ...form, expected_purchase_date: e.target.value })} />
              <Input label="Follow-up Date" type="datetime-local" value={form.follow_up_date} onChange={(e) => setForm({ ...form, follow_up_date: e.target.value })} />
              <TextArea label="Visit Remarks" value={form.remarks} onChange={(e) => setForm({ ...form, remarks: e.target.value })} placeholder="Client feedback, shortlist, pricing..." />
            </FormSection>

            <Button type="submit" disabled={submitting}>{submitting ? 'Saving...' : 'Save Visit'}</Button>
          </form>
        </Card>
      )}

      <Card title="History">
        {loading ? (
          <div className="flex justify-center py-8"><Spinner /></div>
        ) : visits.length === 0 ? (
          <EmptyState icon="showroom" title="No showroom visits yet" message="Log client visits to the Ambala showroom with material selections and quantities." />
        ) : (
          <div className="space-y-3">
            {visits.map((v) => (
              <div key={v.id} className="py-3 border-b border-gray-100 last:border-0">
                <p className="font-medium">{v.client_name || v.selected_material || 'Visit recorded'}</p>
                <p className="text-sm text-gray-500">
                  {siteMap[v.site_id] || 'Site'} · {new Date(v.visit_date).toLocaleString()}
                  {v.estimated_quantity ? ` · ${Number(v.estimated_quantity).toLocaleString('en-IN')} sq.ft` : ''}
                </p>
                <div className="flex flex-wrap gap-2 mt-1">
                  {v.lead_temperature && <span className="demo-badge bg-orange-50 text-orange-700 capitalize">{v.lead_temperature}</span>}
                  {v.quotation_required && <span className="demo-badge bg-amber-100 text-amber-800">Quotation needed</span>}
                  {v.expected_purchase_date && (
                    <span className="demo-badge bg-green-50 text-green-700">
                      Purchase by {new Date(v.expected_purchase_date).toLocaleDateString('en-IN')}
                    </span>
                  )}
                </div>
                {v.remarks && <p className="text-xs text-gray-400 mt-1">{v.remarks}</p>}
              </div>
            ))}
          </div>
        )}
      </Card>
    </div>
  );
}
