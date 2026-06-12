/** Capture device GPS with Gurgaon demo fallback */
export async function captureGeolocation(): Promise<{ latitude: string; longitude: string }> {
  const fallback = { latitude: '28.4595', longitude: '77.0266' };
  try {
    if (!navigator.geolocation) return fallback;
    const pos = await new Promise<GeolocationPosition>((resolve, reject) =>
      navigator.geolocation.getCurrentPosition(resolve, reject, { timeout: 5000 })
    );
    return {
      latitude: String(pos.coords.latitude),
      longitude: String(pos.coords.longitude),
    };
  } catch {
    return fallback;
  }
}
