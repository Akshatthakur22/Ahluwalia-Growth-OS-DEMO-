'use client';

import { useEffect, useState } from 'react';
import Link from 'next/link';
import api from '@/lib/api';
import { Card } from '@/components/ui/Card';
import { Button } from '@/components/ui/Button';
import { PageHeader } from '@/components/ui/PageHeader';
import { Alert } from '@/components/ui/Alert';
import { Spinner } from '@/components/ui/Spinner';
import { MetricCard } from '@/components/ui/MetricCard';
import { EmptyState } from '@/components/ui/EmptyState';

interface TeamRecord {
  id: string;
  user_id: string;
  employee_name?: string;
  employee_code?: string;
  role?: string;
  check_in_time: string;
  check_out_time?: string;
  latitude?: string;
  longitude?: string;
  mock_location_detected: boolean;
  route_summary?: string;
}

interface TeamSummary {
  checked_in_today: number;
  total_field_staff: number;
  not_checked_in: number;
  mock_gps_today: number;
  on_route_today: number;
}

export default function TeamAttendancePage() {
  const [records, setRecords] = useState<TeamRecord[]>([]);
  const [summary, setSummary] = useState<TeamSummary | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    api.get('/attendance/team-page-data')
      .then((res) => {
        setSummary(res.data.summary);
        setRecords(res.data.today_records);
      })
      .catch((err) => setError(err.response?.data?.detail || 'Failed to load team attendance'))
      .finally(() => setLoading(false));
  }, []);

  const todayRecords = records;

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-start gap-4">
        <PageHeader
          title="Team Attendance"
          subtitle="Real-time field activity visibility for management"
        />
        <Link href="/attendance">
          <Button variant="secondary" size="sm">My Attendance</Button>
        </Link>
      </div>

      {error && <Alert type="error">{error}</Alert>}

      {loading ? (
        <div className="flex justify-center py-12"><Spinner /></div>
      ) : (
        <>
          {summary && (
            <div className="grid grid-cols-2 lg:grid-cols-4 gap-3">
              <MetricCard
                label="Checked In Today"
                value={summary.checked_in_today}
                subtitle={`of ${summary.total_field_staff} field staff`}
                accent="green"
              />
              <MetricCard
                label="Not Checked In"
                value={summary.not_checked_in}
                subtitle="Missing today"
                accent="orange"
              />
              <MetricCard
                label="Routes Logged"
                value={summary.on_route_today}
                subtitle="Active field days"
                accent="blue"
              />
              <MetricCard
                label="GPS Alerts"
                value={summary.mock_gps_today}
                subtitle="Mock location flags"
                accent={summary.mock_gps_today > 0 ? 'red' : 'gray'}
              />
            </div>
          )}

          <Card title={`Today's Activity (${todayRecords.length})`}>
            {todayRecords.length === 0 ? (
              <EmptyState
                icon="attendance"
                title="No check-ins today yet"
                message="Field team attendance will appear here in real time."
              />
            ) : (
              <div className="space-y-3">
                {todayRecords.map((r) => (
                  <div key={r.id} className="border border-gray-100 rounded-xl p-4">
                    <div className="flex justify-between items-start gap-2">
                      <div>
                        <p className="font-medium text-sm">{r.employee_name || 'Employee'}</p>
                        <p className="text-xs text-gray-500 capitalize">
                          {r.employee_code} · {r.role?.replace(/_/g, ' ')}
                        </p>
                      </div>
                      <div className="flex gap-1">
                        {r.mock_location_detected && (
                          <span className="demo-badge bg-red-100 text-red-700">Mock GPS</span>
                        )}
                        {r.check_out_time ? (
                          <span className="demo-badge bg-green-50 text-green-700">Complete</span>
                        ) : (
                          <span className="demo-badge bg-blue-50 text-blue-700">On field</span>
                        )}
                      </div>
                    </div>
                    <p className="text-xs text-gray-500 mt-2">
                      In: {new Date(r.check_in_time).toLocaleTimeString('en-IN')}
                      {r.check_out_time && ` · Out: ${new Date(r.check_out_time).toLocaleTimeString('en-IN')}`}
                    </p>
                    {r.route_summary && (
                      <p className="text-xs text-gray-600 mt-1">🗺️ {r.route_summary}</p>
                    )}
                  </div>
                ))}
              </div>
            )}
          </Card>

          <Card title="Recent Team History">
            <div className="space-y-2 max-h-96 overflow-y-auto">
              {records.slice(0, 20).map((r) => (
                <div key={r.id} className="py-2 border-b border-gray-50 last:border-0 text-sm">
                  <span className="font-medium">{r.employee_name}</span>
                  <span className="text-gray-500"> · {new Date(r.check_in_time).toLocaleDateString('en-IN')}</span>
                  {r.route_summary && <span className="text-gray-400"> · {r.route_summary}</span>}
                </div>
              ))}
            </div>
          </Card>
        </>
      )}
    </div>
  );
}
