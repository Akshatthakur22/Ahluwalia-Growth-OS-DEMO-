import api from './api';

type CacheEntry<T> = { data: T; expires: number };

const cache = new Map<string, CacheEntry<unknown>>();
const inflight = new Map<string, Promise<unknown>>();

const DEFAULT_TTL = 60_000; // 1 minute

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
  }, 120_000);
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

export function fetchExecutiveDashboard() {
  return cachedGet('dash:executive', async () => {
    const { data } = await api.get('/dashboard/executive');
    return data;
  }, 45_000);
}

export function fetchManagerDashboard() {
  return cachedGet('dash:manager', async () => {
    const { data } = await api.get('/dashboard/manager');
    return data;
  }, 45_000);
}

export function fetchSitesWithPipeline(): Promise<SitePipelineBundle> {
  return cachedGet('sites:with-pipeline', async () => {
    const { data } = await api.get<SitePipelineBundle>('/sites/with-pipeline');
    return data;
  }, 60_000);
}
