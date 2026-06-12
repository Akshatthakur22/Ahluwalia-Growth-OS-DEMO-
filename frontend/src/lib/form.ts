/** Remove empty strings before API submit */
export function cleanPayload<T extends Record<string, unknown>>(obj: T): Partial<T> {
  const out: Record<string, unknown> = {};
  for (const [k, v] of Object.entries(obj)) {
    if (v !== '' && v !== null && v !== undefined) out[k] = v;
  }
  return out as Partial<T>;
}
