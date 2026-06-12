'use client';

import Link from 'next/link';
import { usePathname, useRouter } from 'next/navigation';
import { useAuthStore } from '@/lib/auth';
import { Button } from '@/components/ui/Button';

const ROLE_NAV: Record<string, { href: string; label: string }[]> = {
  field_executive: [
    { href: '/dashboard', label: 'Home' },
    { href: '/attendance', label: 'Check In' },
    { href: '/sites', label: 'Sites' },
    { href: '/search', label: 'Search' },
  ],
  marketing_executive: [
    { href: '/dashboard', label: 'Home' },
    { href: '/attendance', label: 'Attendance' },
    { href: '/meetings', label: 'Meetings' },
    { href: '/opportunities', label: 'Pipeline' },
    { href: '/search', label: 'Search' },
  ],
  sales_executive: [
    { href: '/dashboard', label: 'Home' },
    { href: '/attendance', label: 'Attendance' },
    { href: '/showroom-visits', label: 'Showroom' },
    { href: '/opportunities', label: 'Pipeline' },
    { href: '/search', label: 'Search' },
  ],
  manager: [
    { href: '/dashboard', label: 'Dashboard' },
    { href: '/attendance/team', label: 'Attendance' },
    { href: '/assignments', label: 'Assign' },
    { href: '/opportunities', label: 'Pipeline' },
    { href: '/search', label: 'Search' },
  ],
  ceo: [
    { href: '/dashboard', label: 'Command Center' },
    { href: '/opportunities', label: 'Pipeline' },
    { href: '/search', label: 'Search' },
    { href: '/attendance/team', label: 'Team Pulse' },
  ],
  administrator: [
    { href: '/dashboard', label: 'Dashboard' },
    { href: '/attendance/team', label: 'Attendance' },
    { href: '/assignments', label: 'Assign' },
    { href: '/opportunities', label: 'Pipeline' },
    { href: '/search', label: 'Search' },
  ],
};

export function AppShell({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();
  const router = useRouter();
  const { user, logout } = useAuthStore();

  if (!user) return <>{children}</>;

  const visibleNav = ROLE_NAV[user.role] || ROLE_NAV.field_executive;

  const handleLogout = () => {
    logout();
    router.push('/login');
  };

  return (
    <div className="min-h-screen bg-[#f5f5f7]">
      <header className="bg-white/80 backdrop-blur-md border-b border-gray-200/80 sticky top-0 z-10">
        <div className="max-w-6xl mx-auto px-4 py-3 flex justify-between items-center">
          <div>
            <h1 className="text-base font-semibold text-gray-900 tracking-tight">Growth OS</h1>
            <p className="text-xs text-gray-500 hidden sm:block">Ahluwalia Marbles</p>
          </div>
          <div className="flex items-center gap-3">
            <span className="text-sm text-gray-600 hidden sm:inline">{user.full_name}</span>
            <Button variant="secondary" size="sm" onClick={handleLogout}>Logout</Button>
          </div>
        </div>
      </header>

      <nav className="bg-white border-b border-gray-100">
        <div className="max-w-6xl mx-auto px-2 flex gap-0.5 overflow-x-auto">
          {visibleNav.map((item) => (
            <Link
              key={item.href}
              href={item.href}
              className={`px-4 py-3 text-sm whitespace-nowrap border-b-2 transition-colors min-h-[44px] flex items-center ${
                pathname.startsWith(item.href)
                  ? 'border-[#0071e3] text-[#0071e3] font-medium'
                  : 'border-transparent text-gray-600 hover:text-gray-900'
              }`}
            >
              {item.label}
            </Link>
          ))}
        </div>
      </nav>

      <main className="max-w-6xl mx-auto px-4 py-6 pb-24">{children}</main>
    </div>
  );
}
