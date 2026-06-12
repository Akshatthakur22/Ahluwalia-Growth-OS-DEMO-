'use client';

import { useEffect, useState } from 'react';
import api from '@/lib/api';
import { useAuthStore } from '@/lib/auth';
import { cleanPayload } from '@/lib/form';
import { Card } from '@/components/ui/Card';
import { Button } from '@/components/ui/Button';
import { Input } from '@/components/ui/Input';
import { TextArea } from '@/components/ui/TextArea';
import { Select } from '@/components/ui/Select';
import { FormSection } from '@/components/ui/FormSection';
import { EmptyState } from '@/components/ui/EmptyState';
import { MetricCard } from '@/components/ui/MetricCard';
import { fetchSitesLookup, siteLookupMap } from '@/lib/query';

interface Assignment {
  id: string;
  site_id: string;
  assigned_to: string;
  assignment_type: string;
  assigned_at: string;
  priority?: string;
  target_follow_up_date?: string;
  remarks?: string;
}

interface Site {
  id: string;
  site_name: string;
}

interface AssignableUser {
  id: string;
  full_name: string;
  role: string;
}

const ROLE_LABELS: Record<string, string> = {
  marketing_executive: 'Marketing Associate',
  sales_executive: 'Showroom Sales',
  field_executive: 'Field Executive',
};

export default function AssignmentsPage() {
  const { user } = useAuthStore();
  const canAssign = user?.role === 'manager' || user?.role === 'administrator';

  const [assignments, setAssignments] = useState<Assignment[]>([]);
  const [sites, setSites] = useState<Site[]>([]);
  const [users, setUsers] = useState<AssignableUser[]>([]);
  const [siteMap, setSiteMap] = useState<Record<string, string>>({});
  const [userMap, setUserMap] = useState<Record<string, string>>({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [submitting, setSubmitting] = useState(false);
  const [form, setForm] = useState({
    site_id: '',
    assigned_to: '',
    assignment_type: 'marketing',
    priority: 'medium',
    target_follow_up_date: '',
    remarks: '',
  });

  useEffect(() => {
    const load = async () => {
      setLoading(true);
      setError('');
      try {
        const requests: Promise<unknown>[] = [
          api.get('/assignments'),
          fetchSitesLookup(),
        ];
        if (canAssign) requests.push(api.get('/users/assignable'));

        const results = await Promise.all(requests);
        const assignmentsRes = results[0] as { data: Assignment[] };
        const sites = results[1] as Site[];
        setAssignments(assignmentsRes.data);
        setSites(sites);
        setSiteMap(siteLookupMap(sites));

        if (canAssign && results[2]) {
          const usersRes = results[2] as { data: AssignableUser[] };
          setUsers(usersRes.data);
          setUserMap(Object.fromEntries(usersRes.data.map((u) => [u.id, u.full_name])));
        }
      } catch (err: any) {
        setError(err.response?.data?.detail || 'Failed to load assignments');
      } finally {
        setLoading(false);
      }
    };
    load();
  }, [canAssign]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setSubmitting(true);
    setError('');
    setSuccess('');
    try {
      const payload = cleanPayload({
        ...form,
        target_follow_up_date: form.target_follow_up_date
          ? new Date(form.target_follow_up_date).toISOString()
          : undefined,
      });
      const { data } = await api.post('/assignments', payload);
      setAssignments([data, ...assignments]);
      setForm({ site_id: '', assigned_to: '', assignment_type: 'marketing', priority: 'medium', target_follow_up_date: '', remarks: '' });
      setSuccess('Assignment created successfully');
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to create assignment');
    } finally {
      setSubmitting(false);
    }
  };

  const filteredUsers =
    form.assignment_type === 'marketing'
      ? users.filter((u) => u.role === 'marketing_executive')
      : users.filter((u) => u.role === 'sales_executive');

  if (loading) {
    return (
      <div className="flex justify-center py-16">
        <div className="h-8 w-8 rounded-full border-2 border-gray-300 border-t-blue-600 animate-spin" />
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-semibold text-gray-900 tracking-tight">Assignments</h2>
        <p className="text-sm text-gray-500 mt-1">Allocate sites to marketing or sales executives</p>
      </div>

      {error && (
        <div className="bg-red-50 border border-red-100 text-red-700 px-4 py-3 rounded-xl text-sm">{error}</div>
      )}
      {success && (
        <div className="bg-green-50 border border-green-100 text-green-700 px-4 py-3 rounded-xl text-sm">{success}</div>
      )}

      {assignments.length > 0 && (
        <div className="grid grid-cols-2 gap-3">
          <MetricCard
            label="Total Assignments"
            value={assignments.length}
            subtitle={`${assignments.filter((a) => a.assignment_type === 'marketing').length} marketing · ${assignments.filter((a) => a.assignment_type === 'sales').length} sales`}
            accent="blue"
          />
          <MetricCard
            label="High Priority"
            value={assignments.filter((a) => a.priority === 'high').length}
            subtitle="Needs attention"
            accent="orange"
          />
        </div>
      )}

      {canAssign && (
        <Card title="Assign Opportunity">
          <form onSubmit={handleSubmit} className="space-y-5">
            <FormSection title="Site & Executive">
              <Select label="Site *" value={form.site_id} onChange={(e) => setForm({ ...form, site_id: e.target.value })} required>
                <option value="">Select site</option>
                {sites.map((s) => (
                  <option key={s.id} value={s.id}>{s.site_name}</option>
                ))}
              </Select>
              <div className="grid grid-cols-2 gap-4">
                <Select label="Assignment Type" value={form.assignment_type} onChange={(e) => setForm({ ...form, assigned_to: '', assignment_type: e.target.value })}>
                  <option value="marketing">Marketing</option>
                  <option value="sales">Sales</option>
                </Select>
                <Select label="Priority" value={form.priority} onChange={(e) => setForm({ ...form, priority: e.target.value })}>
                  <option value="low">Low</option>
                  <option value="medium">Medium</option>
                  <option value="high">High</option>
                </Select>
              </div>
              <Select label="Assign To *" value={form.assigned_to} onChange={(e) => setForm({ ...form, assigned_to: e.target.value })} required>
                <option value="">Select team member</option>
                {filteredUsers.map((u) => (
                  <option key={u.id} value={u.id}>
                    {u.full_name} ({ROLE_LABELS[u.role] || u.role})
                  </option>
                ))}
              </Select>
            </FormSection>
            <FormSection title="Follow-Up Plan">
              <Input label="Target Follow-up Date" type="datetime-local" value={form.target_follow_up_date} onChange={(e) => setForm({ ...form, target_follow_up_date: e.target.value })} />
              <TextArea label="Assignment Remarks" value={form.remarks} onChange={(e) => setForm({ ...form, remarks: e.target.value })} placeholder="Context for the assignee — requirement size, urgency, key contacts..." />
            </FormSection>
            <Button type="submit" disabled={submitting}>
              {submitting ? 'Assigning...' : 'Create Assignment'}
            </Button>
          </form>
        </Card>
      )}

      <Card title="Assignment History">
        {assignments.length === 0 ? (
          <EmptyState icon="assignments" title="No assignments yet" message="Assign sites to marketing or sales executives to kick off the pipeline." />
        ) : (
          <div className="space-y-3">
            {assignments.map((a) => (
              <div key={a.id} className="border border-gray-100 rounded-xl p-4">
                <p className="font-medium text-gray-900">
                  {siteMap[a.site_id] || 'Site'} → {userMap[a.assigned_to] || 'Team member'}
                </p>
                <p className="text-sm text-gray-500 mt-1 capitalize">
                  {a.assignment_type} · {new Date(a.assigned_at).toLocaleString()}
                </p>
                <div className="flex flex-wrap gap-2 mt-2">
                  {a.priority && (
                    <span className="text-xs bg-gray-100 text-gray-600 px-2 py-0.5 rounded-full capitalize">
                      {a.priority} priority
                    </span>
                  )}
                  {a.target_follow_up_date && (
                    <span className="text-xs bg-blue-50 text-blue-700 px-2 py-0.5 rounded-full">
                      Follow-up: {new Date(a.target_follow_up_date).toLocaleDateString('en-IN')}
                    </span>
                  )}
                </div>
                {a.remarks && <p className="text-xs text-gray-400 mt-2">{a.remarks}</p>}
              </div>
            ))}
          </div>
        )}
      </Card>
    </div>
  );
}
