'use client';

import { useEffect, useState } from 'react';
import api from '@/lib/api';
import { captureGeolocation } from '@/lib/geolocation';
import { cleanPayload } from '@/lib/form';
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
import { fetchSitesWithPipeline, invalidateCache } from '@/lib/query';

interface Site {
  id: string;
  site_name: string;
  address: string;
  city: string;
  area?: string;
  site_stage?: string;
  project_type?: string;
  project_size?: number;
  estimated_requirement?: string;
  competitor_brand?: string;
  competitor_quantity?: string;
  site_remarks?: string;
  decision_maker?: string;
  expected_purchase_timeline?: string;
  latitude?: string;
  longitude?: string;
  created_at?: string;
  updated_at?: string;
}

interface SiteMedia {
  id: string;
  media_type: string;
  file_url: string;
  created_at: string;
}

interface Contact {
  id: string;
  site_id: string;
  name: string;
  contact_type: string;
  mobile_number: string;
  firm_name?: string;
  designation?: string;
  category?: string;
}

interface Opportunity {
  id: string;
  site_id: string;
  opportunity_name: string;
  current_status: string;
  expected_revenue?: number;
}

type SiteFormData = {
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
  competitor_brand: string;
  competitor_quantity: string;
  site_remarks: string;
  decision_maker: string;
  expected_purchase_timeline: string;
};

const EMPTY_SITE_FORM: SiteFormData = {
  site_name: '',
  address: '',
  area: '',
  city: 'Gurgaon',
  latitude: '',
  longitude: '',
  site_stage: 'structure',
  project_type: 'residential',
  project_size: '',
  estimated_requirement: '',
  competitor_brand: '',
  competitor_quantity: '',
  site_remarks: '',
  decision_maker: '',
  expected_purchase_timeline: '',
};

const EMPTY_CONTACT_FORM = {
  site_id: '',
  name: '',
  contact_type: 'builder',
  mobile_number: '',
  alternate_number: '',
  firm_name: '',
  designation: '',
  category: 'B',
  address: '',
  remarks: '',
};

function siteToForm(site: Site): SiteFormData {
  return {
    site_name: site.site_name || '',
    address: site.address || '',
    area: site.area || '',
    city: site.city || 'Gurgaon',
    latitude: site.latitude || '',
    longitude: site.longitude || '',
    site_stage: site.site_stage || 'structure',
    project_type: site.project_type || 'residential',
    project_size: site.project_size ? String(site.project_size) : '',
    estimated_requirement: site.estimated_requirement || '',
    competitor_brand: site.competitor_brand || '',
    competitor_quantity: site.competitor_quantity || '',
    site_remarks: site.site_remarks || '',
    decision_maker: site.decision_maker || '',
    expected_purchase_timeline: site.expected_purchase_timeline || '',
  };
}

function SiteFormFields({
  form,
  setForm,
  onCaptureGps,
  capturingGps,
}: {
  form: SiteFormData;
  setForm: (f: SiteFormData) => void;
  onCaptureGps: () => void;
  capturingGps: boolean;
}) {
  return (
    <>
      <FormSection title="Site Location">
        <Input label="Site Name *" value={form.site_name} onChange={(e) => setForm({ ...form, site_name: e.target.value })} placeholder="e.g. Sunrise Towers" required />
        <Input label="Address *" value={form.address} onChange={(e) => setForm({ ...form, address: e.target.value })} placeholder="Full street address" required />
        <div className="grid grid-cols-2 gap-4">
          <Input label="Area / Locality" value={form.area} onChange={(e) => setForm({ ...form, area: e.target.value })} placeholder="Sector 45" />
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

      <FormSection title="Project Details">
        <div className="grid grid-cols-2 gap-4">
          <Select label="Project Stage" value={form.site_stage} onChange={(e) => setForm({ ...form, site_stage: e.target.value })}>
            <option value="planning">Planning</option>
            <option value="foundation">Foundation</option>
            <option value="structure">Structure</option>
            <option value="finishing">Finishing</option>
            <option value="completed">Completed</option>
          </Select>
          <Select label="Project Type" value={form.project_type} onChange={(e) => setForm({ ...form, project_type: e.target.value })}>
            <option value="residential">Residential</option>
            <option value="commercial">Commercial</option>
            <option value="industrial">Industrial</option>
            <option value="mixed_use">Mixed Use</option>
          </Select>
        </div>
        <Input label="Project Size (sq.ft)" type="number" value={form.project_size} onChange={(e) => setForm({ ...form, project_size: e.target.value })} placeholder="e.g. 50000" />
        <TextArea label="Estimated Marble Requirement" value={form.estimated_requirement} onChange={(e) => setForm({ ...form, estimated_requirement: e.target.value })} placeholder="Lobby, bathrooms, common areas..." />
      </FormSection>

      <FormSection title="Competitor Intelligence">
        <div className="grid grid-cols-2 gap-4">
          <Input label="Current Vendor / Competitor" value={form.competitor_brand} onChange={(e) => setForm({ ...form, competitor_brand: e.target.value })} placeholder="e.g. Kajaria" />
          <Input label="Competitor Material / Qty" value={form.competitor_quantity} onChange={(e) => setForm({ ...form, competitor_quantity: e.target.value })} placeholder="e.g. 2000 sq.ft" />
        </div>
      </FormSection>

      <FormSection title="Decision Intelligence">
        <div className="grid grid-cols-2 gap-4">
          <Input label="Decision Maker" value={form.decision_maker} onChange={(e) => setForm({ ...form, decision_maker: e.target.value })} placeholder="e.g. Ravi Mehta, MD" />
          <Input label="Expected Purchase Timeline" value={form.expected_purchase_timeline} onChange={(e) => setForm({ ...form, expected_purchase_timeline: e.target.value })} placeholder="e.g. Q3 2026" />
        </div>
        <TextArea label="Site Remarks" value={form.site_remarks} onChange={(e) => setForm({ ...form, site_remarks: e.target.value })} placeholder="Access notes, competitor intel..." />
      </FormSection>
    </>
  );
}

export default function SitesPage() {
  const [sites, setSites] = useState<Site[]>([]);
  const [opportunities, setOpportunities] = useState<Opportunity[]>([]);
  const [selected, setSelected] = useState<Site | null>(null);
  const [contacts, setContacts] = useState<Contact[]>([]);
  const [loading, setLoading] = useState(true);
  const [loadingDetail, setLoadingDetail] = useState(false);
  const [showForm, setShowForm] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [saving, setSaving] = useState(false);
  const [capturingGps, setCapturingGps] = useState(false);
  const [createForm, setCreateForm] = useState(EMPTY_SITE_FORM);
  const [editForm, setEditForm] = useState(EMPTY_SITE_FORM);
  const [contactForm, setContactForm] = useState(EMPTY_CONTACT_FORM);
  const [media, setMedia] = useState<SiteMedia[]>([]);
  const [photoUrl, setPhotoUrl] = useState('');
  const [uploadingPhoto, setUploadingPhoto] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  const loadSites = async () => {
    try {
      const data = await fetchSitesWithPipeline();
      setSites(data.sites as Site[]);
      const opps = Object.entries(data.opportunities_by_site).map(([siteId, o]) => ({
        id: o.id,
        site_id: siteId,
        opportunity_name: o.opportunity_name,
        current_status: o.current_status,
        expected_revenue: o.expected_revenue,
      }));
      setOpportunities(opps);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to load sites');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { loadSites(); }, []);

  const captureGpsFor = (setter: (f: SiteFormData) => void, current: SiteFormData) => {
    setCapturingGps(true);
    captureGeolocation().then((coords) => {
      setter({ ...current, ...coords });
      setCapturingGps(false);
    });
  };

  const selectSite = async (site: Site) => {
    setSelected(site);
    setShowForm(false);
    setEditForm(siteToForm(site));
    setContactForm((c) => ({ ...c, site_id: site.id }));
    setLoadingDetail(true);
    setError('');
    try {
      const [contactsRes, mediaRes] = await Promise.all([
        api.get('/contacts', { params: { site_id: site.id } }),
        api.get(`/sites/${site.id}/media`),
      ]);
      setSelected(site);
      setEditForm(siteToForm(site));
      setContacts(contactsRes.data);
      setMedia(mediaRes.data);
    } catch {
      setContacts([]);
      setMedia([]);
    } finally {
      setLoadingDetail(false);
    }
  };

  const handleCreateSite = async (e: React.FormEvent) => {
    e.preventDefault();
    setSubmitting(true);
    setError('');
    setSuccess('');
    try {
      const payload = cleanPayload({
        ...createForm,
        project_size: createForm.project_size ? Number(createForm.project_size) : undefined,
      });
      const { data } = await api.post('/sites', payload);
      setSites([data, ...sites]);
      setShowForm(false);
      setCreateForm(EMPTY_SITE_FORM);
      setSuccess(`Site "${data.site_name}" created — opportunity auto-generated`);
      invalidateCache('sites:');
      await loadSites();
      selectSite(data);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to create site');
    } finally {
      setSubmitting(false);
    }
  };

  const handleUpdateSite = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!selected) return;
    setSaving(true);
    setError('');
    setSuccess('');
    try {
      const payload = cleanPayload({
        ...editForm,
        project_size: editForm.project_size ? Number(editForm.project_size) : undefined,
      });
      const { data } = await api.patch(`/sites/${selected.id}`, payload);
      setSelected(data);
      setSites(sites.map((s) => (s.id === data.id ? data : s)));
      setSuccess(`Site "${data.site_name}" updated`);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to update site');
    } finally {
      setSaving(false);
    }
  };

  const handleUploadPhoto = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!selected || !photoUrl.trim()) return;
    setUploadingPhoto(true);
    setError('');
    try {
      const { data } = await api.post(`/sites/${selected.id}/media`, {
        media_type: 'site_photo',
        file_url: photoUrl.trim(),
      });
      setMedia([data, ...media]);
      setPhotoUrl('');
      setSuccess('Site photo attached');
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to upload photo');
    } finally {
      setUploadingPhoto(false);
    }
  };

  const handleAddContact = async (e: React.FormEvent) => {
    e.preventDefault();
    const siteId = contactForm.site_id || selected?.id;
    if (!siteId) return;
    setError('');
    setSuccess('');
    try {
      await api.post('/contacts', cleanPayload({ ...contactForm, site_id: siteId }));
      setContactForm({ ...EMPTY_CONTACT_FORM, site_id: siteId });
      setSuccess('Stakeholder added successfully');
      if (selected) {
        const { data } = await api.get('/contacts', { params: { site_id: selected.id } });
        setContacts(data);
      }
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to add contact');
    }
  };

  const linkedOpp = selected ? opportunities.find((o) => o.site_id === selected.id) : null;

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-start gap-4">
        <PageHeader title="Site Discovery" subtitle="Capture, track, and update site intelligence" />
        <Button
          onClick={() => { setShowForm(!showForm); if (!showForm) setSelected(null); }}
          size="sm"
        >
          {showForm ? 'Cancel' : '+ New Site'}
        </Button>
      </div>

      {error && <Alert type="error">{error}</Alert>}
      {success && <Alert type="success">{success}</Alert>}

      {!loading && sites.length > 0 && (
        <div className="grid grid-cols-3 gap-3">
          <MetricCard label="Total Sites" value={sites.length} subtitle="In portfolio" accent="blue" />
          <MetricCard
            label="Residential"
            value={sites.filter((s) => s.project_type === 'residential').length}
            subtitle="Projects"
            accent="green"
          />
          <MetricCard
            label="Commercial"
            value={sites.filter((s) => s.project_type === 'commercial' || s.project_type === 'mixed_use').length}
            subtitle="Projects"
            accent="orange"
          />
        </div>
      )}

      {showForm && (
        <Card title="New Site — Field Capture">
          <form onSubmit={handleCreateSite} className="space-y-5">
            <SiteFormFields
              form={createForm}
              setForm={setCreateForm}
              onCaptureGps={() => captureGpsFor(setCreateForm, createForm)}
              capturingGps={capturingGps}
            />
            <Button type="submit" disabled={submitting}>{submitting ? 'Saving...' : 'Save Site & Create Opportunity'}</Button>
          </form>
        </Card>
      )}

      {loading ? (
        <div className="flex justify-center py-12"><Spinner /></div>
      ) : sites.length === 0 ? (
        <EmptyState icon="sites" title="No sites discovered" message="Capture your first construction site from the field to start the pipeline." action={<Button size="sm" onClick={() => setShowForm(true)}>+ New Site</Button>} />
      ) : (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
          <Card title="Sites">
            <div className="space-y-2 max-h-[70vh] overflow-y-auto">
              {sites.map((site) => {
                const opp = opportunities.find((o) => o.site_id === site.id);
                return (
                  <button
                    key={site.id}
                    type="button"
                    onClick={() => selectSite(site)}
                    className={`w-full text-left rounded-xl p-4 border transition-colors ${
                      selected?.id === site.id ? 'border-[#0071e3] bg-blue-50/50' : 'border-gray-100 hover:bg-gray-50'
                    }`}
                  >
                    <h3 className="font-medium text-sm text-gray-900">{site.site_name}</h3>
                    <p className="text-xs text-gray-500 mt-0.5">
                      {site.address}{site.area ? `, ${site.area}` : ''}, {site.city}
                    </p>
                    <div className="flex flex-wrap gap-1.5 mt-2">
                      {site.site_stage && <span className="demo-badge bg-blue-100 text-blue-700 capitalize">{site.site_stage}</span>}
                      {site.project_type && <span className="demo-badge bg-gray-100 text-gray-600 capitalize">{site.project_type.replace('_', ' ')}</span>}
                      {opp && <span className="demo-badge bg-indigo-100 text-indigo-700">{formatStatus(opp.current_status)}</span>}
                    </div>
                  </button>
                );
              })}
            </div>
          </Card>

          {selected ? (
            <div className="space-y-4">
              <Card title="Site Detail & Update">
                {loadingDetail ? (
                  <div className="flex justify-center py-8"><Spinner /></div>
                ) : (
                  <>
                    <div className="flex flex-wrap gap-3 mb-4 p-3 bg-gray-50 rounded-xl text-xs text-gray-500">
                      {selected.created_at && (
                        <span>Discovered: {new Date(selected.created_at).toLocaleDateString('en-IN')}</span>
                      )}
                      {selected.updated_at && (
                        <span>Last updated: {new Date(selected.updated_at).toLocaleDateString('en-IN')}</span>
                      )}
                      {selected.latitude && selected.longitude && (
                        <span>GPS: {Number(selected.latitude).toFixed(4)}, {Number(selected.longitude).toFixed(4)}</span>
                      )}
                    </div>

                    {linkedOpp && (
                      <div className="mb-4 p-3 border border-indigo-100 bg-indigo-50/50 rounded-xl">
                        <p className="text-xs text-gray-500">Linked Opportunity</p>
                        <p className="text-sm font-medium text-gray-900">{linkedOpp.opportunity_name}</p>
                        <span className="demo-badge bg-indigo-100 text-indigo-700 mt-1 inline-block">{formatStatus(linkedOpp.current_status)}</span>
                        {linkedOpp.expected_revenue && (
                          <p className="text-xs text-gray-500 mt-1">₹{Number(linkedOpp.expected_revenue).toLocaleString('en-IN')}</p>
                        )}
                      </div>
                    )}

                    <form onSubmit={handleUpdateSite} className="space-y-5">
                      <SiteFormFields
                        form={editForm}
                        setForm={setEditForm}
                        onCaptureGps={() => captureGpsFor(setEditForm, editForm)}
                        capturingGps={capturingGps}
                      />
                      <Button type="submit" disabled={saving}>{saving ? 'Saving...' : 'Save Changes'}</Button>
                    </form>
                  </>
                )}
              </Card>

              <Card title={`Stakeholders (${contacts.length})`}>
                {contacts.length === 0 ? (
                  <p className="text-sm text-gray-400 mb-4">No stakeholders linked yet.</p>
                ) : (
                  <div className="space-y-2 mb-4">
                    {contacts.map((c) => (
                      <div key={c.id} className="py-2 border-b border-gray-50 last:border-0">
                        <p className="text-sm font-medium">{c.name}</p>
                        <p className="text-xs text-gray-500 capitalize">{c.contact_type} · {c.firm_name || '—'} · {c.mobile_number}{c.category ? ` · Cat ${c.category}` : ''}</p>
                      </div>
                    ))}
                  </div>
                )}
                <form onSubmit={handleAddContact} className="space-y-3 pt-2 border-t border-gray-100">
                  <p className="text-xs font-medium text-gray-500">Add stakeholder to this site</p>
                  <div className="grid grid-cols-2 gap-3">
                    <Input label="Name" value={contactForm.name} onChange={(e) => setContactForm({ ...contactForm, name: e.target.value })} required />
                    <Select label="Type" value={contactForm.contact_type} onChange={(e) => setContactForm({ ...contactForm, contact_type: e.target.value })}>
                      <option value="builder">Builder</option>
                      <option value="architect">Architect</option>
                      <option value="owner">Owner</option>
                      <option value="referral">Referral</option>
                    </Select>
                  </div>
                  <Input label="Mobile" type="tel" value={contactForm.mobile_number} onChange={(e) => setContactForm({ ...contactForm, mobile_number: e.target.value })} required />
                  <Select label="Category (A–D)" value={contactForm.category} onChange={(e) => setContactForm({ ...contactForm, category: e.target.value })}>
                    <option value="A">A — Key Decision Maker</option>
                    <option value="B">B — Influencer</option>
                    <option value="C">C — User / Site Contact</option>
                    <option value="D">D — Referral / Peripheral</option>
                  </Select>
                  <Button type="submit" variant="secondary" size="sm">Add Stakeholder</Button>
                </form>
              </Card>

              <Card title={`Site Photos (${media.length})`}>
                {media.length > 0 && (
                  <div className="grid grid-cols-2 gap-2 mb-4">
                    {media.map((m) => (
                      <a key={m.id} href={m.file_url} target="_blank" rel="noreferrer" className="block rounded-lg overflow-hidden border border-gray-100">
                        <img src={m.file_url} alt="Site" className="w-full h-24 object-cover" />
                        <p className="text-[10px] text-gray-400 p-1 capitalize">{m.media_type.replace('_', ' ')}</p>
                      </a>
                    ))}
                  </div>
                )}
                <form onSubmit={handleUploadPhoto} className="flex gap-2">
                  <Input
                    label="Photo URL"
                    value={photoUrl}
                    onChange={(e) => setPhotoUrl(e.target.value)}
                    placeholder="https://... site photo"
                    className="flex-1"
                  />
                  <Button type="submit" variant="secondary" size="sm" disabled={uploadingPhoto} className="self-end">
                    {uploadingPhoto ? 'Adding...' : 'Attach'}
                  </Button>
                </form>
              </Card>
            </div>
          ) : (
            <Card title="Select a Site">
              <p className="text-sm text-gray-500 py-8 text-center">
                Click a site on the left to view details, update field data, and manage stakeholders.
              </p>
            </Card>
          )}
        </div>
      )}
    </div>
  );
}
