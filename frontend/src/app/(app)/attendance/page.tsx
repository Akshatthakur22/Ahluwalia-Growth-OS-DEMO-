'use client';

import { useEffect, useState, useCallback } from 'react';
import Link from 'next/link';
import api from '@/lib/api';
import { captureGeolocation } from '@/lib/geolocation';
import { useAuthStore } from '@/lib/auth';
import { Card } from '@/components/ui/Card';
import { Button } from '@/components/ui/Button';
import { TextArea } from '@/components/ui/TextArea';
import { PageHeader } from '@/components/ui/PageHeader';
import { Alert } from '@/components/ui/Alert';
import { Spinner } from '@/components/ui/Spinner';
import { EmptyState } from '@/components/ui/EmptyState';
import { MetricCard } from '@/components/ui/MetricCard';
import { FormSection } from '@/components/ui/FormSection';

interface AttendanceRecord {
  id: string;
  check_in_time: string;
  check_out_time?: string;
  latitude?: string;
  longitude?: string;
  mock_location_detected: boolean;
  route_summary?: string;
}

interface TodayStatus {
  checked_in: boolean;
  checked_out: boolean;
  record: AttendanceRecord | null;
}

interface Summary {
  checked_in_today: boolean;
  checked_out_today: boolean;
  month_check_ins: number;
  month_on_time: number;
  month_route_logs: number;
  avg_hours_in_field: number;
  total_records: number;
}

function formatDuration(checkIn: string, checkOut?: string) {
  if (!checkOut) return null;
  const hrs = (new Date(checkOut).getTime() - new Date(checkIn).getTime()) / 3600000;
  return `${hrs.toFixed(1)}h in field`;
}

function mapsLink(lat?: string, lon?: string) {
  if (!lat || !lon) return null;
  return `https://www.google.com/maps?q=${lat},${lon}`;
}

export default function AttendancePage() {
  const { user } = useAuthStore();
  const isManager = user?.role === 'manager' || user?.role === 'ceo' || user?.role === 'administrator';

  const [records, setRecords] = useState<AttendanceRecord[]>([]);
  const [today, setToday] = useState<TodayStatus | null>(null);
  const [summary, setSummary] = useState<Summary | null>(null);
  const [loading, setLoading] = useState(true);
  const [checkingIn, setCheckingIn] = useState(false);
  const [checkingOut, setCheckingOut] = useState(false);
  const [routeSummary, setRouteSummary] = useState('');
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');

  const load = useCallback(async () => {
    try {
      const { fetchAttendancePageData } = await import('@/lib/query');
      const data = await fetchAttendancePageData();
      setRecords(data.records);
      setToday(data.today);
      setSummary(data.summary);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to load attendance');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => { load(); }, [load]);

  const handleCheckIn = async () => {
    setCheckingIn(true);
    setError('');
    setMessage('');
    try {
      const { latitude, longitude } = await captureGeolocation();
      const { data } = await api.post('/attendance/check-in', {
        latitude,
        longitude,
        device_information: navigator.userAgent,
      });
      setMessage(`Checked in at ${new Date(data.check_in_time).toLocaleString()}`);
      const { invalidateCache } = await import('@/lib/query');
      invalidateCache('attendance:');
      await load();
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Check-in failed');
    } finally {
      setCheckingIn(false);
    }
  };

  const handleCheckOut = async () => {
    setCheckingOut(true);
    setError('');
    setMessage('');
    try {
      const { latitude, longitude } = await captureGeolocation();
      await api.post('/attendance/check-out', {
        latitude,
        longitude,
        route_summary: routeSummary || undefined,
        device_information: navigator.userAgent,
      });
      setMessage('Checked out — route logged for management review');
      setRouteSummary('');
      const { invalidateCache } = await import('@/lib/query');
      invalidateCache('attendance:');
      await load();
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Check-out failed');
    } finally {
      setCheckingOut(false);
    }
  };

  const todayRecord = today?.record;
  const canCheckIn = !today?.checked_in;
  const canCheckOut = today?.checked_in && !today?.checked_out;

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-start gap-4">
        <PageHeader
          title="Attendance & Field Tracking"
          subtitle="GPS-validated check-in, route logging, and productivity"
        />
        {isManager && (
          <Link href="/attendance/team">
            <Button variant="secondary" size="sm">Team View</Button>
          </Link>
        )}
      </div>

      {error && <Alert type="error">{error}</Alert>}
      {message && <Alert type="success">{message}</Alert>}

      {loading ? (
        <div className="flex justify-center py-12"><Spinner /></div>
      ) : (
        <>
          {summary && (
            <div className="grid grid-cols-2 lg:grid-cols-4 gap-3">
              <MetricCard
                label="Today"
                value={summary.checked_out_today ? 'Done' : summary.checked_in_today ? 'On Field' : 'Not Started'}
                subtitle={summary.checked_in_today ? 'Checked in' : 'Tap check-in below'}
                accent={summary.checked_out_today ? 'green' : summary.checked_in_today ? 'blue' : 'gray'}
              />
              <MetricCard label="This Month" value={summary.month_check_ins} subtitle={`${summary.month_on_time} on-time`} accent="purple" />
              <MetricCard label="Route Logs" value={summary.month_route_logs} subtitle="Days with route data" accent="orange" />
              <MetricCard label="Avg Field Hours" value={`${summary.avg_hours_in_field}h`} subtitle={`${summary.total_records} total days`} accent="blue" />
            </div>
          )}

          <Card title="Today's Attendance">
            {todayRecord ? (
              <div className="space-y-4">
                <div className="p-4 bg-green-50 border border-green-100 rounded-xl">
                  <p className="text-sm font-medium text-green-800">
                    {today?.checked_out ? '✓ Day completed' : '● Active on field'}
                  </p>
                  <p className="text-xs text-green-700 mt-1">
                    Check-in: {new Date(todayRecord.check_in_time).toLocaleString()}
                  </p>
                  {todayRecord.check_out_time && (
                    <p className="text-xs text-green-700">
                      Check-out: {new Date(todayRecord.check_out_time).toLocaleString()}
                      {' · '}{formatDuration(todayRecord.check_in_time, todayRecord.check_out_time)}
                    </p>
                  )}
                  {todayRecord.latitude && todayRecord.longitude && (
                    <a
                      href={mapsLink(todayRecord.latitude, todayRecord.longitude)!}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-xs text-[#0071e3] mt-2 inline-block hover:underline"
                    >
                      View GPS on map ({Number(todayRecord.latitude).toFixed(4)}, {Number(todayRecord.longitude).toFixed(4)})
                    </a>
                  )}
                </div>

                {canCheckOut && (
                  <FormSection title="End of Day — Route Summary">
                    <TextArea
                      label="Sites visited / route summary"
                      value={routeSummary}
                      onChange={(e) => setRouteSummary(e.target.value)}
                      placeholder="e.g. 3 sites: Green Valley Residency, Skyline Commercial Hub, Prestige Lakeside Towers"
                    />
                    <Button onClick={handleCheckOut} disabled={checkingOut} className="w-full" variant="secondary">
                      {checkingOut ? 'Checking out...' : 'Check Out & Log Route'}
                    </Button>
                  </FormSection>
                )}

                {todayRecord.route_summary && (
                  <div className="p-3 bg-gray-50 rounded-xl">
                    <p className="text-xs text-gray-500">Route logged</p>
                    <p className="text-sm text-gray-800 mt-0.5">{todayRecord.route_summary}</p>
                  </div>
                )}
              </div>
            ) : (
              <div className="space-y-4">
                <p className="text-sm text-gray-500">
                  GPS location is validated before recording. Mock or spoofed locations are blocked per company policy.
                </p>
                <Button onClick={handleCheckIn} disabled={checkingIn || !canCheckIn} className="w-full" size="lg">
                  {checkingIn ? 'Validating GPS...' : '📍 Check In Now'}
                </Button>
              </div>
            )}
          </Card>

          <Card title="Attendance History">
            {records.length === 0 ? (
              <EmptyState
                icon="attendance"
                title="No check-ins yet"
                message="Start your field day with a GPS-validated check-in."
              />
            ) : (
              <div className="space-y-3">
                {records.map((r) => (
                  <div key={r.id} className="py-3 border-b border-gray-100 last:border-0">
                    <div className="flex justify-between items-start gap-2">
                      <div>
                        <p className="font-medium text-sm">{new Date(r.check_in_time).toLocaleString()}</p>
                        {r.check_out_time && (
                          <p className="text-xs text-gray-500">
                            Out: {new Date(r.check_out_time).toLocaleString()}
                            {' · '}{formatDuration(r.check_in_time, r.check_out_time)}
                          </p>
                        )}
                        {r.route_summary && (
                          <p className="text-xs text-gray-600 mt-1">🗺️ {r.route_summary}</p>
                        )}
                        {r.latitude && r.longitude && (
                          <p className="text-xs text-gray-400 mt-0.5">
                            {Number(r.latitude).toFixed(4)}, {Number(r.longitude).toFixed(4)}
                          </p>
                        )}
                      </div>
                      <div className="flex flex-col gap-1 items-end shrink-0">
                        {r.mock_location_detected && (
                          <span className="demo-badge bg-red-100 text-red-700">Mock GPS</span>
                        )}
                        {!r.check_out_time && !r.mock_location_detected && (
                          <span className="demo-badge bg-amber-50 text-amber-700">No checkout</span>
                        )}
                        {r.check_out_time && (
                          <span className="demo-badge bg-green-50 text-green-700">Complete</span>
                        )}
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </Card>
        </>
      )}
    </div>
  );
}
