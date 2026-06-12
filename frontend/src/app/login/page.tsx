'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { useAuthStore } from '@/lib/auth';
import { Button } from '@/components/ui/Button';
import { Input } from '@/components/ui/Input';
import { Alert } from '@/components/ui/Alert';

const DEMO_ACCOUNTS = [
  { role: 'Field Executive', mobile: '9876543210', password: 'password123' },
  { role: 'Marketing', mobile: '9876543211', password: 'password123' },
  { role: 'Sales', mobile: '9876543212', password: 'password123' },
  { role: 'Manager', mobile: '9876543213', password: 'password123' },
  { role: 'CEO', mobile: '9876543214', password: 'password123' },
];

export default function LoginPage() {
  const router = useRouter();
  const { login } = useAuthStore();
  const [mobileNumber, setMobileNumber] = useState('');
  const [password, setPassword] = useState('password123');
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const fillDemo = (mobile: string) => {
    setMobileNumber(mobile);
    setPassword('password123');
    setError('');
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setIsLoading(true);
    try {
      await login(mobileNumber, password);
      router.push('/dashboard');
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Login failed. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-[#f5f5f7] px-4 py-8">
      <div className="max-w-md w-full space-y-6">
        <div className="text-center">
          <h1 className="text-3xl font-semibold text-gray-900 tracking-tight">Growth OS</h1>
          <p className="mt-2 text-gray-500 text-sm">Ahluwalia Marbles — Business Operating System</p>
        </div>

        <div className="demo-card">
          <form className="space-y-4" onSubmit={handleSubmit}>
            <Input label="Mobile Number" type="tel" value={mobileNumber} onChange={(e) => setMobileNumber(e.target.value)} placeholder="10-digit mobile" required />
            <Input label="Password" type="password" value={password} onChange={(e) => setPassword(e.target.value)} required />
            {error && <Alert type="error">{error}</Alert>}
            <Button type="submit" className="w-full" disabled={isLoading}>
              {isLoading ? 'Signing in...' : 'Sign In'}
            </Button>
          </form>
        </div>

        <div className="demo-card">
          <p className="text-xs font-medium text-gray-500 uppercase tracking-wide mb-3">Demo Accounts — tap to fill</p>
          <div className="space-y-2">
            {DEMO_ACCOUNTS.map((a) => (
              <button
                key={a.mobile}
                type="button"
                onClick={() => fillDemo(a.mobile)}
                className="w-full text-left px-4 py-3 rounded-xl bg-gray-50 hover:bg-gray-100 transition-colors border border-gray-100"
              >
                <span className="font-medium text-gray-900 text-sm">{a.role}</span>
                <span className="text-gray-500 text-xs block mt-0.5">{a.mobile} · password123</span>
              </button>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
