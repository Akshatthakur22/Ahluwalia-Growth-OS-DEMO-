'use client';

import { useEffect, useState, useRef } from 'react';
import api from '@/lib/api';
import { captureGeolocation } from '@/lib/geolocation';
import { cleanPayload } from '@/lib/form';
import { resolveMediaUrl } from '@/lib/media';
import { formatStatus } from '@/lib/lifecycle';
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
import { MetricCard } from '@/components/ui/MetricCard';
import { fetchSitesWithPipeline, fetchSiteDetail, invalidateCache } from '@/lib/query';

const SITE_STAGES = [
  { value: '10', label: '10 Days — Early planning' },
  { value: '30', label: '30 Days — Foundation' },
  { value: '50', label: '50 Days — Structure' },
  { value: '70', label: '70 Days — Finishing' },
  { value: '100', label: '100 Days — Near completion' },
];

const CATEGORIES = [
  { value: 'A', label: 'A — Key Decision Maker' },
  { value: 'B', label: 'B — Influencer' },
  { value: 'C', label: 'C — Site Contact' },
  { value: 'D', label: 'D — Peripheral' },
];

export type SiteCaptureForm = {
  site_name: string;
  address: string;
  area: string;
  city: string;
  latitude: string;
  longitude: string;
  site_stage: string;
  project_type: string;
  project_size: string;
  estimated_requirement: string;
  decision_maker: string;
  expected_purchase_timeline: string;
  current_vendor: string;
  material_used: string;
  purchase_rate: string;
  competitor_brand: string;
  competitor_quantity: string;
  site_remarks: string;
  owner_name: string;
  owner_mobile: string;
  owner_address: string;
  builder_name: string;
  builder_firm_name: string;
  builder_mobile: string;
  builder_category: string;
  architect_name: string;
  architect_firm_name: string;
  architect_mobile: string;
  architect_category: string;
};

const EMPTY_FORM: SiteCaptureForm = {
  site_name: '',
  address: '',
  area: '',
  city: 'Gurgaon',
  latitude: '',
  longitude: '',
  site_stage: '50',
  project_type: 'residential',
  project_size: '',
  estimated_requirement: '',
  decision_maker: '',
  expected_purchase_timeline: '',
  current_vendor: '',
  material_used: '',
  purchase_rate: '',
  competitor_brand: '',
  competitor_quantity: '',
  site_remarks: '',
  owner_name: '',
  owner_mobile: '',
  owner_address: '',
  builder_name: '',
  builder_firm_name: '',
  builder_mobile: '',
  builder_category: 'A',
  architect_name: '',
  architect_firm_name: '',
  architect_mobile: '',
  architect_category: 'B',
};

function stageLabel(value?: string) {
  return SITE_STAGES.find((s) => s.value === value)?.label?.split(' — ')[0] || value || '—';
}

function detailToForm(detail: any): SiteCaptureForm {
  const s = detail;
  const sh = detail.stakeholders || {};
  return {
    site_name: s.site_name || '',
    address: s.address || '',
    area: s.area || '',
    city: s.city || 'Gurgaon',
    latitude: s.latitude || '',
    longitude: s.longitude || '',
    site_stage: s.site_stage || '50',
    project_type: s.project_type || 'residential',
    project_size: s.project_size ? String(s.project_size) : '',
    estimated_requirement: s.estimated_requirement || '',
    decision_maker: s.decision_maker || '',
    expected_purchase_timeline: s.expected_purchase_timeline || '',
    current_vendor: s.current_vendor || '',
    material_used: s.material_used || '',
    purchase_rate: s.purchase_rate ? String(s.purchase_rate) : '',
    competitor_brand: s.competitor_brand || '',
    competitor_quantity: s.competitor_quantity || '',
    site_remarks: s.site_remarks || '',
    owner_name: sh.owner_name || '',
    owner_mobile: sh.owner_mobile || '',
    owner_address: sh.owner_address || '',
    builder_name: sh.builder_name || '',
    builder_firm_name: sh.builder_firm_name || '',
    builder_mobile: sh.builder_mobile || '',
    builder_category: sh.builder_category || 'A',
    architect_name: sh.architect_name || '',
    architect_firm_name: sh.architect_firm_name || '',
    architect_mobile: sh.architect_mobile || '',
    architect_category: sh.architect_category || 'B',
  };
}

function SiteCaptureFields({
  form,
  setForm,
  onCaptureGps,
  capturingGps,
}: {
  form: SiteCaptureForm;
  setForm: (f: SiteCaptureForm) => void;
  onCaptureGps: () => void;
  capturingGps: boolean;
}) {
  return (
    <>
      <FormSection title="Site Location">
        <Input label="Site Name *" value={form.site_name} onChange={(e) => setForm({ ...form, site_name: e.target.value })} required />
        <Input label="Site Address *" value={form.address} onChange={(e) => setForm({ ...form, address: e.target.value })} required />
        <div className="grid grid-cols-2 gap-4">
          <Input label="Area / Locality" value={form.area} onChange={(e) => setForm({ ...form, area: e.target.value })} />
          <Input label="City *" value={form.city} onChange={(e) => setForm({ ...form, city: e.target.value })} required />
        </div>
        <div className="grid grid-cols-2 gap-4">
          <Input label="Latitude" value={form.latitude} readOnly placeholder="Auto-captured" />
          <Input label="Longitude" value={form.longitude} readOnly placeholder="Auto-captured" />
        </div>
        <Button type="button" variant="secondary" size="sm" onClick={onCaptureGps} disabled={capturingGps}>
          {capturingGps ? 'Capturing GPS...' : '📍 Capture GPS Location'}
        </Button>
      </FormSection>

      <FormSection title="Owner">
        <Input label="Owner Name" value={form.owner_name} onChange={(e) => setForm({ ...form, owner_name: e.target.value })} />
        <div className="grid grid-cols-2 gap-4">
          <Input label="Owner Contact" type="tel" value={form.owner_mobile} onChange={(e) => setForm({ ...form, owner_mobile: e.target.value })} />
          <Input label="Owner Address" value={form.owner_address} onChange={(e) => setForm({ ...form, owner_address: e.target.value })} />
        </div>
      </FormSection>

      <FormSection title="Builder">
        <div className="grid grid-cols-2 gap-4">
          <Input label="Builder Name" value={form.builder_name} onChange={(e) => setForm({ ...form, builder_name: e.target.value })} />
          <Input label="Builder Firm Name" value={form.builder_firm_name} onChange={(e) => setForm({ ...form, builder_firm_name: e.target.value })} />
        </div>
        <div className="grid grid-cols-2 gap-4">
          <Input label="Builder Contact" type="tel" value={form.builder_mobile} onChange={(e) => setForm({ ...form, builder_mobile: e.target.value })} />
          <Select label="Builder Category (A–D)" value={form.builder_category} onChange={(e) => setForm({ ...form, builder_category: e.target.value })}>
            {CATEGORIES.map((c) => <option key={c.value} value={c.value}>{c.label}</option>)}
          </Select>
        </div>
      </FormSection>

      <FormSection title="Architect">
        <div className="grid grid-cols-2 gap-4">
          <Input label="Architect Name" value={form.architect_name} onChange={(e) => setForm({ ...form, architect_name: e.target.value })} />
          <Input label="Architect Firm Name" value={form.architect_firm_name} onChange={(e) => setForm({ ...form, architect_firm_name: e.target.value })} />
        </div>
        <div className="grid grid-cols-2 gap-4">
          <Input label="Architect Contact" type="tel" value={form.architect_mobile} onChange={(e) => setForm({ ...form, architect_mobile: e.target.value })} />
          <Select label="Architect Category (A–D)" value={form.architect_category} onChange={(e) => setForm({ ...form, architect_category: e.target.value })}>
            {CATEGORIES.map((c) => <option key={c.value} value={c.value}>{c.label}</option>)}
          </Select>
        </div>
      </FormSection>

      <FormSection title="Project Details">
        <div className="grid grid-cols-2 gap-4">
          <Select label="Project Stage (Days)" value={form.site_stage} onChange={(e) => setForm({ ...form, site_stage: e.target.value })}>
            {SITE_STAGES.map((s) => <option key={s.value} value={s.value}>{s.label}</option>)}
          </Select>
          <Select label="Project Type" value={form.project_type} onChange={(e) => setForm({ ...form, project_type: e.target.value })}>
            <option value="residential">Residential</option>
            <option value="commercial">Commercial</option>
            <option value="industrial">Industrial</option>
            <option value="mixed_use">Mixed Use</option>
          </Select>
        </div>
        <Input label="Project Size (sq.ft)" type="number" value={form.project_size} onChange={(e) => setForm({ ...form, project_size: e.target.value })} />
        <TextArea label="Estimated Marble Requirement" value={form.estimated_requirement} onChange={(e) => setForm({ ...form, estimated_requirement: e.target.value })} />
        <div className="grid grid-cols-2 gap-4">
          <Input label="Decision Maker" value={form.decision_maker} onChange={(e) => setForm({ ...form, decision_maker: e.target.value })} />
          <Input label="Expected Purchase Timeline" value={form.expected_purchase_timeline} onChange={(e) => setForm({ ...form, expected_purchase_timeline: e.target.value })} placeholder="e.g. Q3 2026" />
        </div>
      </FormSection>

      <FormSection title="Vendor & Competitor Intelligence">
        <div className="grid grid-cols-2 gap-4">
          <Input label="Current Vendor" value={form.current_vendor} onChange={(e) => setForm({ ...form, current_vendor: e.target.value })} />
          <Input label="Material Used" value={form.material_used} onChange={(e) => setForm({ ...form, material_used: e.target.value })} placeholder="e.g. Italian Carrara" />
        </div>
        <div className="grid grid-cols-3 gap-4">
          <Input label="Purchase Rate (₹/sq.ft)" type="number" value={form.purchase_rate} onChange={(e) => setForm({ ...form, purchase_rate: e.target.value })} />
          <Input label="Competitor Name" value={form.competitor_brand} onChange={(e) => setForm({ ...form, competitor_brand: e.target.value })} />
          <Input label="Competitor Qty" value={form.competitor_quantity} onChange={(e) => setForm({ ...form, competitor_quantity: e.target.value })} />
        </div>
      </FormSection>

      <FormSection title="Field Notes">
        <TextArea label="Remarks" value={form.site_remarks} onChange={(e) => setForm({ ...form, site_remarks: e.target.value })} />
      </FormSection>
    </>
  );
}

export default function SitesPage() {
  const [sites, setSites] = useState<any[]>([]);
  const [opportunities, setOpportunities] = useState<any[]>([]);
  const [selectedId, setSelectedId] = useState<string | null>(null);
  const [selectedDetail, setSelectedDetail] = useState<any>(null);
  const [media, setMedia] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [loadingDetail, setLoadingDetail] = useState(false);
  const [showForm, setShowForm] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [saving, setSaving] = useState(false);
  const [capturingGps, setCapturingGps] = useState(false);
  const [uploadingPhoto, setUploadingPhoto] = useState(false);
  const [createForm, setCreateForm] = useState<SiteCaptureForm>(EMPTY_FORM);
  const [editForm, setEditForm] = useState<SiteCaptureForm>(EMPTY_FORM);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const photoInputRef = useRef<HTMLInputElement>(null);

  const loadSites = async () => {
    try {
      const data = await fetchSitesWithPipeline();
      setSites(data.sites);
      setOpportunities(
        Object.entries(data.opportunities_by_site).map(([siteId, o]: [string, any]) => ({
          id: o.id,
          site_id: siteId,
          opportunity_name: o.opportunity_name,
          current_status: o.current_status,
          expected_revenue: o.expected_revenue,
        }))
      );
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to load sites');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { loadSites(); }, []);

  const buildPayload = (form: SiteCaptureForm) => cleanPayload({
    ...form,
    project_size: form.project_size ? Number(form.project_size) : undefined,
    purchase_rate: form.purchase_rate ? Number(form.purchase_rate) : undefined,
  });

  const captureGpsFor = (setter: (f: SiteCaptureForm) => void, current: SiteCaptureForm) => {
    setCapturingGps(true);
    captureGeolocation()
      .then((coords) => setter({ ...current, ...coords }))
      .finally(() => setCapturingGps(false));
  };

  const selectSite = async (site: any) => {
    setSelectedId(site.id);
    setShowForm(false);
    setLoadingDetail(true);
    setError('');
    try {
      const data = await fetchSiteDetail(site.id);
      setSelectedDetail(data);
      setEditForm(detailToForm(data));
      setMedia(data.media || []);
    } catch {
      setSelectedDetail(site);
      setEditForm(detailToForm(site));
      setMedia([]);
    } finally {
      setLoadingDetail(false);
    }
  };

  const handleCreate = async (e: React.FormEvent) => {
    e.preventDefault();
    setSubmitting(true);
    setError('');
    setSuccess('');
    try {
      const { data } = await api.post('/sites/capture', buildPayload(createForm));
      setShowForm(false);
      setCreateForm(EMPTY_FORM);
      setSuccess(`Site "${data.site_name}" captured with stakeholders`);
      invalidateCache('sites:');
      await loadSites();
      selectSite(data);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to create site');
    } finally {
      setSubmitting(false);
    }
  };

  const handleUpdate = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!selectedId) return;
    setSaving(true);
    setError('');
    setSuccess('');
    try {
      const { data } = await api.patch(`/sites/${selectedId}/capture`, buildPayload(editForm));
      setSelectedDetail(data);
      setSuccess(`Site "${data.site_name}" updated`);
      invalidateCache('sites:');
      await loadSites();
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to update site');
    } finally {
      setSaving(false);
    }
  };

  const handlePhotoSelect = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file || !selectedId) return;
    setUploadingPhoto(true);
    setError('');
    try {
      const coords = await captureGeolocation();
      const formData = new FormData();
      formData.append('file', file);
      formData.append('latitude', coords.latitude);
      formData.append('longitude', coords.longitude);
      const { data } = await api.post(`/sites/${selectedId}/media/upload`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      setMedia([data, ...media]);
      invalidateCache(`sites:detail:${selectedId}`);
      setSuccess('Geo-tagged site photo uploaded');
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to upload photo');
    } finally {
      setUploadingPhoto(false);
      if (photoInputRef.current) photoInputRef.current.value = '';
    }
  };

  const linkedOpp = selectedId ? opportunities.find((o) => o.site_id === selectedId) : null;

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-start gap-4">
        <PageHeader title="Field Intelligence" subtitle="PDF-complete site capture — owner, builder, architect, vendor intel & geo photos" />
        <Button onClick={() => { setShowForm(!showForm); if (!showForm) { setSelectedId(null); setSelectedDetail(null); } }} size="sm">
          {showForm ? 'Cancel' : '+ New Site'}
        </Button>
      </div>

      {error && <Alert type="error">{error}</Alert>}
      {success && <Alert type="success">{success}</Alert>}

      {!loading && sites.length > 0 && (
        <div className="grid grid-cols-3 gap-3">
          <MetricCard label="Sites in DB" value={sites.length} subtitle="Market intelligence" accent="blue" />
          <MetricCard label="Active Pipeline" value={opportunities.filter((o) => o.current_status !== 'lost').length} subtitle="Linked opportunities" accent="green" />
          <MetricCard label="Early Stage (10–30d)" value={sites.filter((s) => s.site_stage === '10' || s.site_stage === '30').length} subtitle="New discoveries" accent="orange" />
        </div>
      )}

      {showForm && (
        <Card title="New Site — Field Capture">
          <form onSubmit={handleCreate} className="space-y-5">
            <SiteCaptureFields form={createForm} setForm={setCreateForm} onCaptureGps={() => captureGpsFor(setCreateForm, createForm)} capturingGps={capturingGps} />
            <Button type="submit" disabled={submitting}>{submitting ? 'Saving...' : 'Save Site, Stakeholders & Opportunity'}</Button>
          </form>
        </Card>
      )}

      {loading ? (
        <div className="flex justify-center py-12"><Spinner /></div>
      ) : sites.length === 0 ? (
        <EmptyState icon="sites" title="No sites discovered" message="Capture your first site with full PDF field intelligence." action={<Button size="sm" onClick={() => setShowForm(true)}>+ New Site</Button>} />
      ) : (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
          <Card title="Site Portfolio">
            <div className="space-y-2 max-h-[75vh] overflow-y-auto">
              {sites.map((site) => {
                const opp = opportunities.find((o) => o.site_id === site.id);
                return (
                  <button
                    key={site.id}
                    type="button"
                    onClick={() => selectSite(site)}
                    className={`w-full text-left rounded-xl p-4 border transition-colors ${selectedId === site.id ? 'border-[#0071e3] bg-blue-50/50' : 'border-gray-100 hover:bg-gray-50'}`}
                  >
                    <h3 className="font-medium text-sm">{site.site_name}</h3>
                    <p className="text-xs text-gray-500 mt-0.5">{site.address}, {site.city}</p>
                    <div className="flex flex-wrap gap-1.5 mt-2">
                      <span className="demo-badge bg-blue-100 text-blue-700">{stageLabel(site.site_stage)}</span>
                      {site.current_vendor && <span className="demo-badge bg-gray-100 text-gray-600">Vendor: {site.current_vendor}</span>}
                      {opp && <span className="demo-badge bg-indigo-100 text-indigo-700">{formatStatus(opp.current_status)}</span>}
                    </div>
                  </button>
                );
              })}
            </div>
          </Card>

          {selectedId && selectedDetail ? (
            <div className="space-y-4">
              <Card title="Site Detail & Update">
                {loadingDetail ? (
                  <div className="flex justify-center py-8"><Spinner /></div>
                ) : (
                  <>
                    <div className="flex flex-wrap gap-3 mb-4 p-3 bg-gray-50 rounded-xl text-xs text-gray-500">
                      {selectedDetail.created_at && <span>Discovered: {new Date(selectedDetail.created_at).toLocaleDateString('en-IN')}</span>}
                      {selectedDetail.latitude && selectedDetail.longitude && (
                        <span>Site GPS: {Number(selectedDetail.latitude).toFixed(4)}, {Number(selectedDetail.longitude).toFixed(4)}</span>
                      )}
                    </div>
                    {linkedOpp && (
                      <div className="mb-4 p-3 border border-indigo-100 bg-indigo-50/50 rounded-xl">
                        <p className="text-xs text-gray-500">Linked Opportunity</p>
                        <p className="text-sm font-medium">{linkedOpp.opportunity_name}</p>
                        <span className="demo-badge bg-indigo-100 text-indigo-700 mt-1 inline-block">{formatStatus(linkedOpp.current_status)}</span>
                      </div>
                    )}
                    <form onSubmit={handleUpdate} className="space-y-5">
                      <SiteCaptureFields form={editForm} setForm={setEditForm} onCaptureGps={() => captureGpsFor(setEditForm, editForm)} capturingGps={capturingGps} />
                      <Button type="submit" disabled={saving}>{saving ? 'Saving...' : 'Save Changes'}</Button>
                    </form>
                  </>
                )}
              </Card>

              <Card title={`Geo-Tagged Photos (${media.length})`}>
                {media.length > 0 && (
                  <div className="grid grid-cols-2 gap-2 mb-4">
                    {media.map((m) => (
                      <a key={m.id} href={resolveMediaUrl(m.file_url)} target="_blank" rel="noreferrer" className="block rounded-lg overflow-hidden border border-gray-100">
                        <img src={resolveMediaUrl(m.file_url)} alt="Site" className="w-full h-28 object-cover" />
                        <div className="p-2 text-[10px] text-gray-500">
                          {m.latitude && m.longitude ? (
                            <span>📍 {Number(m.latitude).toFixed(4)}, {Number(m.longitude).toFixed(4)}</span>
                          ) : (
                            <span>No GPS on photo</span>
                          )}
                          {m.captured_at && <span className="block">{new Date(m.captured_at).toLocaleString('en-IN')}</span>}
                        </div>
                      </a>
                    ))}
                  </div>
                )}
                <input ref={photoInputRef} type="file" accept="image/*" capture="environment" className="hidden" onChange={handlePhotoSelect} />
                <Button type="button" variant="secondary" size="sm" disabled={uploadingPhoto} onClick={() => photoInputRef.current?.click()}>
                  {uploadingPhoto ? 'Uploading...' : '📷 Capture / Upload Geo-Tagged Photo'}
                </Button>
                <p className="text-[11px] text-gray-400 mt-2">GPS is captured automatically when the photo is taken.</p>
              </Card>
            </div>
          ) : (
            <Card title="Select a Site">
              <p className="text-sm text-gray-500 py-8 text-center">Select a site to view and update full field intelligence.</p>
            </Card>
          )}
        </div>
      )}
    </div>
  );
}
