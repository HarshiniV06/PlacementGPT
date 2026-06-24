import { useState } from 'react';
import Layout, { Card, LoadingSpinner, ErrorMessage, JsonViewer } from '../components/Layout';
import { api } from '../services/api';

export default function CareerPlanPage() {
  const [skills, setSkills] = useState('Python, JavaScript');
  const [role, setRole] = useState('Software Engineer');
  const [companies, setCompanies] = useState('Google, Microsoft');
  const [interests, setInterests] = useState('Backend, Web Development');
  const [result, setResult] = useState<unknown>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [mode, setMode] = useState<'plan' | 'gaps' | 'roadmap'>('plan');

  const run = async () => {
    setLoading(true);
    setError('');
    const skillList = skills.split(',').map((s) => s.trim()).filter(Boolean);
    const companyList = companies.split(',').map((s) => s.trim()).filter(Boolean);
    const interestList = interests.split(',').map((s) => s.trim()).filter(Boolean);

    try {
      let data;
      if (mode === 'gaps') {
        data = await api.career.analyzeGaps({
          current_skills: skillList,
          target_role: role,
          target_companies: companyList,
        });
      } else if (mode === 'roadmap') {
        data = await api.career.generateRoadmap({
          current_skills: skillList,
          target_role: role,
          available_weeks: 16,
        });
      } else {
        data = await api.career.create({
          skills: skillList,
          target_role: role,
          target_companies: companyList,
          interests: interestList,
          experience_years: 0,
        });
      }
      setResult(data);
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : 'Request failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Layout>
      <h1 className="text-2xl font-bold mb-6">Career Planner</h1>

      <Card title="Your Profile">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label className="text-sm text-gray-600">Skills (comma-separated)</label>
            <input className="w-full border rounded-lg p-2 mt-1" value={skills} onChange={(e) => setSkills(e.target.value)} />
          </div>
          <div>
            <label className="text-sm text-gray-600">Target Role</label>
            <input className="w-full border rounded-lg p-2 mt-1" value={role} onChange={(e) => setRole(e.target.value)} />
          </div>
          <div>
            <label className="text-sm text-gray-600">Target Companies</label>
            <input className="w-full border rounded-lg p-2 mt-1" value={companies} onChange={(e) => setCompanies(e.target.value)} />
          </div>
          <div>
            <label className="text-sm text-gray-600">Interests</label>
            <input className="w-full border rounded-lg p-2 mt-1" value={interests} onChange={(e) => setInterests(e.target.value)} />
          </div>
        </div>

        <div className="flex gap-2 mt-4">
          {(['plan', 'gaps', 'roadmap'] as const).map((m) => (
            <button
              key={m}
              onClick={() => setMode(m)}
              className={`px-4 py-2 rounded-lg text-sm font-medium ${
                mode === m ? 'bg-primary text-white' : 'bg-gray-100 text-gray-600'
              }`}
            >
              {m === 'plan' ? 'Full Plan' : m === 'gaps' ? 'Skill Gaps' : 'Roadmap'}
            </button>
          ))}
        </div>

        <button
          onClick={run}
          disabled={loading}
          className="mt-4 bg-secondary text-white px-6 py-2.5 rounded-lg font-medium hover:bg-green-600 disabled:opacity-50"
        >
          {loading ? 'Generating...' : 'Generate'}
        </button>
      </Card>

      {loading && <LoadingSpinner />}
      {error && <div className="mt-4"><ErrorMessage message={error} /></div>}
      {result != null && (
        <Card title="Results" className="mt-6">
          <JsonViewer data={result} />
        </Card>
      )}
    </Layout>
  );
}
