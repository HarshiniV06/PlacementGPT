import Link from 'next/link';
import { useRouter } from 'next/router';
import { ReactNode } from 'react';

const navItems = [
  { href: '/', label: 'Dashboard' },
  { href: '/resume', label: 'Resume' },
  { href: '/career-plan', label: 'Career Plan' },
  { href: '/dsa', label: 'DSA Tracker' },
  { href: '/interview', label: 'Interview' },
  { href: '/company', label: 'Company Prep' },
  { href: '/voice', label: 'Voice Practice' },
];

export default function Layout({ children }: { children: ReactNode }) {
  const router = useRouter();

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white border-b border-gray-200 sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 py-3 flex items-center justify-between">
          <Link href="/" className="text-xl font-bold text-primary">
            PlacementGPT
          </Link>
          <nav className="hidden md:flex gap-1">
            {navItems.map((item) => (
              <Link
                key={item.href}
                href={item.href}
                className={`px-3 py-2 rounded-lg text-sm font-medium transition-colors ${
                  router.pathname === item.href
                    ? 'bg-primary text-white'
                    : 'text-gray-600 hover:bg-gray-100'
                }`}
              >
                {item.label}
              </Link>
            ))}
          </nav>
        </div>
        <div className="md:hidden overflow-x-auto px-4 pb-2 flex gap-2">
          {navItems.map((item) => (
            <Link
              key={item.href}
              href={item.href}
              className={`px-3 py-1.5 rounded-full text-xs font-medium whitespace-nowrap ${
                router.pathname === item.href
                  ? 'bg-primary text-white'
                  : 'bg-gray-100 text-gray-600'
              }`}
            >
              {item.label}
            </Link>
          ))}
        </div>
      </header>
      <main className="max-w-7xl mx-auto px-4 py-6">{children}</main>
    </div>
  );
}

export function Card({ title, children, className = '' }: { title?: string; children: ReactNode; className?: string }) {
  return (
    <div className={`bg-white rounded-xl shadow-sm border border-gray-200 p-6 ${className}`}>
      {title && <h2 className="text-lg font-semibold text-gray-900 mb-4">{title}</h2>}
      {children}
    </div>
  );
}

export function ScoreRing({ score, label }: { score: number; label: string }) {
  const color = score >= 80 ? 'text-secondary' : score >= 60 ? 'text-accent' : score >= 40 ? 'text-primary' : 'text-danger';
  return (
    <div className="text-center">
      <div className={`text-4xl font-bold ${color}`}>{Math.round(score)}</div>
      <div className="text-sm text-gray-500 mt-1">{label}</div>
    </div>
  );
}

export function LoadingSpinner() {
  return (
    <div className="flex justify-center py-8">
      <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary" />
    </div>
  );
}

export function ErrorMessage({ message }: { message: string }) {
  return (
    <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg text-sm">
      {message}
    </div>
  );
}

export function JsonViewer({ data }: { data: unknown }) {
  return (
    <pre className="bg-gray-50 rounded-lg p-4 text-xs overflow-auto max-h-96 text-gray-700">
      {JSON.stringify(data, null, 2)}
    </pre>
  );
}
