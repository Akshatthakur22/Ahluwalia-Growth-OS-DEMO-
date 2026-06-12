'use client';

import { useEffect, useState } from 'react';
import Link from 'next/link';
import { useAuthStore } from '@/lib/auth';
import { Card } from '@/components/ui/Card';
import { PageHeader } from '@/components/ui/PageHeader';
import { Alert } from '@/components/ui/Alert';
import { MetricCard } from '@/components/ui/MetricCard';
import { PipelineBar } from '@/components/ui/PipelineBar';
import { ExecutiveDashboard } from '@/components/dashboard/ExecutiveDashboard';
import { fetchExecutiveDashboard, fetchManagerDashboard, fetchRoleDashboard } from '@/lib/query';

function SkeletonCards({ count = 4 }: { count?: number }) {
  return (
    <div className="grid grid-cols-2 lg:grid-cols-4 gap-3">
      {Array.from({ length: count }).map((_, i) => (
        <div key={i} className="demo-card !p-4 animate-pulse">
          <div className="h-3 w-20 bg-gray-200 rounded" />
          <div className="h-8 w-28 bg-gray-200 rounded mt-3" />
          <div className="h-2 w-32 bg-gray-100 rounded mt-2" />
        </div>
      ))}
    </div>
  );
}

function ManagerDashboard({ data }: { data: any }) {
  const overdue = data.operations.overdue_opportunity_followups + data.operations.overdue_meeting_followups;

  return (
    <>
      <Card title="Team Attendance Today">
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-3">
          <MetricCard label="Checked In" value={data.team.checked_in_today} subtitle={`${data.team.attendance_percentage}% of team`} accent="green" />
          <MetricCard label="Not Checked In" value={data.team.not_checked_in} subtitle="Follow up required" accent="orange" />
          <MetricCard label="GPS Alerts" value={data.team.mock_gps_incidents} subtitle="Mock location blocked" accent="gray" />
          <MetricCard label="Active Staff" value={data.team.total_active_employees} subtitle="On payroll" accent="blue" />
        </div>
      </Card>

      <Card title="Operations & Alerts">
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-3">
          <MetricCard label="Overdue Follow-ups" value={overdue} subtitle={`${data.operations.overdue_opportunity_followups} deals · ${data.operations.overdue_meeting_followups} meetings`} accent="orange" />
          <MetricCard label="Active Assignments" value={data.operations.active_assignments} subtitle="Sites assigned to team" accent="purple" />
          <MetricCard label="Showroom (Month)" value={data.operations.showroom_visits_this_month} subtitle={`${data.operations.showroom_visits_scheduled} scheduled`} accent="blue" />
          <MetricCard label="New Sites" value={data.field_operations.sites_this_month} subtitle={`${data.field_operations.total_sites} total`} accent="green" />
        </div>
      </Card>

      <div className="grid grid-cols-2 gap-3">
        <MetricCard label="Meetings Held" value={data.field_operations.total_meetings} subtitle="Relationship activity" accent="purple" />
        <MetricCard label="Sites in Portfolio" value={data.field_operations.total_sites} subtitle="Field intelligence" accent="gray" />
      </div>

      <Card title="Pipeline Snapshot — Action Stages">
        <PipelineBar pipeline={data.pipeline_snapshot} />
      </Card>

      <Card title="Manager Actions">
        <div className="grid grid-cols-2 gap-3">
          <Link href="/assignments" className="bg-purple-50 text-purple-700 rounded-xl p-4 text-center font-medium hover:bg-purple-100 transition-colors min-h-[56px] flex items-center justify-center">Assign Sites</Link>
          <Link href="/attendance/team" className="bg-blue-50 text-blue-700 rounded-xl p-4 text-center font-medium hover:bg-blue-100 transition-colors min-h-[56px] flex items-center justify-center">Team Attendance</Link>
          <Link href="/opportunities" className="bg-indigo-50 text-indigo-700 rounded-xl p-4 text-center font-medium hover:bg-indigo-100 transition-colors min-h-[56px] flex items-center justify-center">Move Pipeline</Link>
          <Link href="/search" className="bg-gray-50 text-gray-700 rounded-xl p-4 text-center font-medium hover:bg-gray-100 transition-colors min-h-[56px] flex items-center justify-center">Search Contacts</Link>
        </div>
      </Card>
    </>
  );
}

interface RoleDashboard {
  role: string;
  cards: { label: string; value: string; subtitle: string; accent: string }[];
  pipeline_summary?: Record<string, number>;
}

export default function DashboardPage() {
  const { user } = useAuthStore();
  const [ceoData, setCeoData] = useState<any>(null);
  const [managerData, setManagerData] = useState<any>(null);
  const [roleDash, setRoleDash] = useState<RoleDashboard | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  const isCeo = user?.role === 'ceo';
  const isManager = user?.role === 'manager' || user?.role === 'administrator';

  useEffect(() => {
    if (!user) return;
    setLoading(true);
    setError('');

    const load = async () => {
      try {
        if (isCeo) {
          setCeoData(await fetchExecutiveDashboard());
        } else if (isManager) {
          setManagerData(await fetchManagerDashboard());
        } else {
          setRoleDash(await fetchRoleDashboard(user.role));
        }
      } catch (err: any) {
        setError(err.response?.data?.detail || 'Failed to load dashboard');
      } finally {
        setLoading(false);
      }
    };
    load();
  }, [user, isCeo, isManager]);

  const roleLabel = user?.role?.replace(/_/g, ' ').replace(/\b\w/g, (c) => c.toUpperCase());
  const title = isCeo
    ? 'Executive Command Center'
    : isManager
      ? 'Operations Dashboard'
      : `Welcome, ${user?.full_name?.split(' ')[0]}`;

  const subtitle = isCeo
    ? 'Analytics & KPI command center — revenue, funnel, and growth intelligence'
    : isManager
      ? 'Team attendance, assignments & daily execution control'
      : `${roleLabel} · ${user?.employee_code} · Ahluwalia Marbles`;

  return (
    <div className="space-y-6">
      <PageHeader title={title} subtitle={subtitle} />

      {error && <Alert type="error">{error}</Alert>}

      {loading && <SkeletonCards count={isCeo || isManager ? 8 : 4} />}

      {!loading && isCeo && ceoData && <ExecutiveDashboard data={ceoData} />}

      {!loading && isManager && managerData && <ManagerDashboard data={managerData} />}

      {!loading && !isCeo && !isManager && roleDash && (
        <>
          <div className="grid grid-cols-2 gap-3">
            {roleDash.cards.map((card) => (
              <MetricCard key={card.label} label={card.label} value={card.value} subtitle={card.subtitle} accent={card.accent} />
            ))}
          </div>

          {roleDash.pipeline_summary && user?.role === 'sales_executive' && (
            <Card title="Team Pipeline Snapshot">
              <PipelineBar pipeline={roleDash.pipeline_summary} />
            </Card>
          )}

          <Card title="Quick Actions">
            <div className="grid grid-cols-2 gap-3">
              {user?.role === 'field_executive' && (
                <>
                  <Link href="/attendance" className="bg-blue-50 text-blue-700 rounded-xl p-4 text-center font-medium hover:bg-blue-100 transition-colors min-h-[56px] flex items-center justify-center">Check In</Link>
                  <Link href="/sites" className="bg-green-50 text-green-700 rounded-xl p-4 text-center font-medium hover:bg-green-100 transition-colors min-h-[56px] flex items-center justify-center">Sites</Link>
                </>
              )}
              {user?.role === 'marketing_executive' && (
                <Link href="/meetings" className="bg-purple-50 text-purple-700 rounded-xl p-4 text-center font-medium hover:bg-purple-100 transition-colors min-h-[56px] flex items-center justify-center col-span-2">Record Meeting</Link>
              )}
              {user?.role === 'sales_executive' && (
                <Link href="/showroom-visits" className="bg-orange-50 text-orange-700 rounded-xl p-4 text-center font-medium hover:bg-orange-100 transition-colors min-h-[56px] flex items-center justify-center col-span-2">Showroom Visit</Link>
              )}
              <Link href="/search" className="bg-gray-50 text-gray-700 rounded-xl p-4 text-center font-medium hover:bg-gray-100 transition-colors min-h-[56px] flex items-center justify-center">Search</Link>
              <Link href="/opportunities" className="bg-indigo-50 text-indigo-700 rounded-xl p-4 text-center font-medium hover:bg-indigo-100 transition-colors min-h-[56px] flex items-center justify-center">Pipeline</Link>
            </div>
          </Card>
        </>
      )}
    </div>
  );
}
