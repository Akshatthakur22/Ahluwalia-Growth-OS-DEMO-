import Link from 'next/link';

const FEATURES = [
  { icon: '📍', label: 'Field Attendance', desc: 'GPS check-ins & site visits' },
  { icon: '🤝', label: 'Sales Pipeline', desc: 'Opportunity lifecycle tracking' },
  { icon: '🔍', label: 'Master Search', desc: 'One number, full history' },
  { icon: '📊', label: 'Executive Dashboard', desc: 'Revenue & pipeline insights' },
];

export default function HomePage() {
  return (
    <div className="min-h-screen bg-[#f5f5f7] flex flex-col">
      <header className="px-6 py-5 flex items-center justify-between max-w-5xl mx-auto w-full">
        <span className="text-sm font-semibold text-gray-900 tracking-tight">Ahluwalia Marbles</span>
        <Link
          href="/login"
          className="text-sm font-medium text-[#0071e3] hover:underline"
        >
          Sign In
        </Link>
      </header>

      <main className="flex-1 flex items-center justify-center px-4 py-12">
        <div className="max-w-lg w-full text-center">
          <div className="mb-8">
            <div className="inline-flex items-center justify-center w-16 h-16 rounded-2xl bg-gradient-to-br from-[#0071e3] to-indigo-600 text-white text-2xl font-bold shadow-lg shadow-blue-500/20 mb-6">
              G
            </div>
            <h1 className="text-4xl sm:text-5xl font-semibold text-gray-900 tracking-tight">
              Growth OS
            </h1>
            <p className="mt-3 text-gray-500 text-base sm:text-lg leading-relaxed max-w-md mx-auto">
              The business operating system for Ahluwalia Marbles — from field discovery to confirmed orders.
            </p>
          </div>

          <div className="demo-card text-left mb-8">
            <div className="grid grid-cols-2 gap-4">
              {FEATURES.map((f) => (
                <div key={f.label} className="flex gap-3 items-start">
                  <span className="text-xl shrink-0">{f.icon}</span>
                  <div>
                    <p className="text-sm font-medium text-gray-900">{f.label}</p>
                    <p className="text-xs text-gray-500 mt-0.5">{f.desc}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>

          <Link
            href="/login"
            className="inline-flex items-center justify-center w-full sm:w-auto min-w-[200px] bg-[#0071e3] text-white px-8 py-3.5 rounded-xl font-medium text-sm hover:bg-[#0077ed] transition-colors shadow-sm active:scale-[0.98]"
          >
            Get Started
          </Link>
          <p className="mt-4 text-xs text-gray-400">
            Demo accounts available on the sign-in page
          </p>
        </div>
      </main>

      <footer className="px-6 py-4 text-center text-xs text-gray-400">
        Ahluwalia Growth OS · MVP Demo
      </footer>
    </div>
  );
}
