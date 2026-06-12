import api from './api';

type CacheEntry<T> = { data: T; expires: number };

const cache = new Map<string, CacheEntry<unknown>>();
const inflight = new Map<string, Promise<unknown>>();

const DEFAULT_TTL = 90_000; // 90 seconds

export function invalidateCache(prefix?: string) {
  if (!prefix) {
    cache.clear();
    return;
  }
  for (const key of cache.keys()) {
    if (key.startsWith(prefix)) cache.delete(key);
  }
}

export async function cachedGet<T>(
  key: string,
  fetcher: () => Promise<T>,
  ttlMs = DEFAULT_TTL,
): Promise<T> {
  const hit = cache.get(key);
  if (hit && Date.now() < hit.expires) {
    return hit.data as T;
  }

  const pending = inflight.get(key);
  if (pending) return pending as Promise<T>;

  const promise = fetcher()
    .then((data) => {
      cache.set(key, { data, expires: Date.now() + ttlMs });
      inflight.delete(key);
      return data;
    })
    .catch((err) => {
      inflight.delete(key);
      throw err;
    });

  inflight.set(key, promise);
  return promise as Promise<T>;
}

export interface SiteLookup {
  id: string;
  site_name: string;
}

export function fetchSitesLookup(): Promise<SiteLookup[]> {
  return cachedGet('sites:lookup', async () => {
    const { data } = await api.get<SiteLookup[]>('/sites/lookup');
    return data;
  }, 180_000);
}

export function siteLookupMap(sites: SiteLookup[]): Record<string, string> {
  return Object.fromEntries(sites.map((s) => [s.id, s.site_name]));
}

export interface SitePipelineBundle {
  sites: unknown[];
  opportunities_by_site: Record<string, {
    id: string;
    opportunity_name: string;
    current_status: string;
    expected_revenue?: number;
  }>;
}

export function fetchSitesWithPipeline(): Promise<SitePipelineBundle> {
  return cachedGet('sites:with-pipeline', async () => {
    const { data } = await api.get<SitePipelineBundle>('/sites/with-pipeline');
    return data;
  }, 120_000);
}

export function fetchSiteDetail(siteId: string) {
  return cachedGet(`sites:detail:${siteId}`, async () => {
    const { data } = await api.get(`/sites/${siteId}/detail`);
    return data;
  }, 60_000);
}

export function fetchExecutiveDashboard() {
  return cachedGet('dash:executive', async () => {
    const { data } = await api.get('/dashboard/executive');
    return data;
  }, 90_000);
}

export function fetchManagerDashboard() {
  return cachedGet('dash:manager', async () => {
    const { data } = await api.get('/dashboard/manager');
    return data;
  }, 90_000);
}

export function fetchRoleDashboard(role: string) {
  return cachedGet(`dash:role:${role}`, async () => {
    const { data } = await api.get('/dashboard/role');
    return data;
  }, 90_000);
}

export function fetchOpportunities() {
  return cachedGet('opportunities:list', async () => {
    const { data } = await api.get('/opportunities');
    return data;
  }, 90_000);
}

export function fetchOpportunityDetail(opportunityId: string) {
  return cachedGet(`opportunities:detail:${opportunityId}`, async () => {
    const { data } = await api.get(`/opportunities/${opportunityId}/detail`);
    return data;
  }, 60_000);
}

export function fetchMeetings() {
  return cachedGet('meetings:list', async () => {
    const { data } = await api.get('/meetings');
    return data;
  }, 90_000);
}

export function fetchAttendancePageData() {
  return cachedGet('attendance:page', async () => {
    const { data } = await api.get('/attendance/page-data');
    return data;
  }, 30_000);
}

export function fetchTeamAttendancePageData() {
  return cachedGet('attendance:team', async () => {
    const { data } = await api.get('/attendance/team-page-data');
    return data;
  }, 30_000);
}
