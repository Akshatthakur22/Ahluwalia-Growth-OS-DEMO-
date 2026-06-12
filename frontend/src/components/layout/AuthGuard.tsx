'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { useAuthStore } from '@/lib/auth';
import { AppShell } from './AppShell';

export function AuthGuard({ children }: { children: React.ReactNode }) {
  const router = useRouter();
  const { user, fetchUser, isLoading } = useAuthStore();
  const [initialized, setInitialized] = useState(false);

  useEffect(() => {
    const token = localStorage.getItem('access_token');
    if (!token) {
      router.replace('/login');
      return;
    }
    // Skip blocking re-fetch when user already loaded (e.g. right after login)
    if (user) {
      setInitialized(true);
      return;
    }
    fetchUser().finally(() => setInitialized(true));
  }, [fetchUser, router, user]);

  useEffect(() => {
    if (initialized && !isLoading && !user) {
      localStorage.removeItem('access_token');
      router.replace('/login');
    }
  }, [initialized, isLoading, user, router]);

  if (!initialized || isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-[#f5f5f7]">
        <div className="flex flex-col items-center gap-3">
          <div className="h-8 w-8 rounded-full border-2 border-gray-300 border-t-blue-600 animate-spin" />
          <p className="text-sm text-gray-500">Loading...</p>
        </div>
      </div>
    );
  }

  if (!user) return null;

  return <AppShell>{children}</AppShell>;
}
