const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export function resolveMediaUrl(fileUrl: string): string {
  if (fileUrl.startsWith('http://') || fileUrl.startsWith('https://') || fileUrl.startsWith('data:')) {
    return fileUrl;
  }
  return `${API_BASE}${fileUrl}`;
}
