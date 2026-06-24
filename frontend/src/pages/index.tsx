import { useEffect, useState } from 'react';
import Layout, { Card, ScoreRing, ErrorMessage } from '../components/Layout';
import { api } from '../services/api';
import Link from 'next/link';

function ScoreSkeleton() {
  return (
    <div className="animate-pulse">
      <div className="h-10 w-16 bg-gray-200 rounded mx-auto" />
      <div className="h-3 w-24 bg-gray-100 rounded mx-auto mt-2" />
    </div>
  );
}

export default function Dashboard() {
  const [data, setData] = useState<Record<string, unknown> | null>(null);
  const [statsLoading, setStatsLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    api.analytics
      .summary()
      .then((dash) => setData(dash as Record<string, unknown>))
      .catch((e) => setError(e.message))
      .finally(() => setStatsLoading(false));
  }, []);

  const readiness = data?.readiness as Record<string, unknown> | undefined;
  const prediction = data?.prediction as Record<string, unknown> | undefined;
  const overall = (readiness?.overall_readiness_score as number) || 0;

  const features = [
    { href: '/resume', title: 'Resume Agent', desc: 'ATS scoring & keyword analysis', phase: 'Phase 1' },
    { href: '/career-plan', title: 'Career Planner', desc: 'Skill gaps & learning roadmap', phase: 'Phase 1' },
    { href: '/dsa', title: 'DSA Tracker', desc: 'Track problems & daily plans', phase: 'Phase 2' },
    { href: '/interview', title: 'Mock Interview', desc: 'Technical & HR interviews', phase: 'Phase 3' },
    { href: '/company', title: 'Company Prep', desc: 'Company-specific intelligence', phase: 'Phase 4' },
    { href: '/voice', title: 'Voice Practice', desc: 'Speech & delivery analysis', phase: 'Phase 5' },
  ];

  return (
    <Layout>
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">Placement Dashboard</h1>
        <p className="text-gray-500 mt-1">Your AI-powered placement preparation hub</p>
      </div>

      {error && (
        <div className="mb-4">
          <ErrorMessage message={`Could not load stats: ${error}. Feature cards below still work.`} />
        </div>
      )}

      <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
        <Card className="text-center">
          {statsLoading ? (
            <ScoreSkeleton />
          ) : (
            <ScoreRing score={overall} label="Overall Readiness" />
          )}
        </Card>
        <Card className="text-center">
          {statsLoading ? (
            <ScoreSkeleton />
          ) : (
            <ScoreRing
              score={(prediction?.success_probability as number) || 0}
              label="Success Probability"
            />
          )}
        </Card>
        <Card className="text-center">
          {statsLoading ? (
            <ScoreSkeleton />
          ) : (
            <>
              <div className="text-4xl font-bold text-primary capitalize">
                {(readiness?.readiness_level as string)?.replace(/_/g, ' ') || 'N/A'}
              </div>
              <div className="text-sm text-gray-500 mt-1">Status</div>
            </>
          )}
        </Card>
        <Card className="text-center">
          <div className="text-4xl font-bold text-secondary">6</div>
          <div className="text-sm text-gray-500 mt-1">Active Agents</div>
        </Card>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {features.map((f) => (
          <Link key={f.href} href={f.href}>
            <Card className="hover:shadow-md transition-shadow cursor-pointer h-full">
              <span className="text-xs font-medium text-primary bg-blue-50 px-2 py-1 rounded">
                {f.phase}
              </span>
              <h3 className="text-lg font-semibold mt-2">{f.title}</h3>
              <p className="text-gray-500 text-sm mt-1">{f.desc}</p>
            </Card>
          </Link>
        ))}
      </div>
    </Layout>
  );
}
