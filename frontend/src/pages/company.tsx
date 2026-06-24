import { useState } from 'react';
import Layout, { Card, LoadingSpinner, ErrorMessage, JsonViewer } from '../components/Layout';
import { api } from '../services/api';

export default function CompanyPage() {
  const [company, setCompany] = useState('Google');
  const [role, setRole] = useState('Software Engineer');
  const [result, setResult] = useState<unknown>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [action, setAction] = useState<'analyze' | 'faqs' | 'topics' | 'readiness'>('analyze');

  const run = async () => {
    setLoading(true);
    setError('');
    const data = { company, role };
    try {
      let res;
      switch (action) {
        case 'faqs': res = await api.company.faqs(data); break;
        case 'topics': res = await api.company.topics(data); break;
        case 'readiness': res = await api.company.readiness(data); break;
        default: res = await api.company.analyze(data);
      }
      setResult(res);
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : 'Failed');
    } finally {
      setLoading(false);
    }
  };

  const companies = ['Google', 'Microsoft', 'Amazon', 'TCS', 'Infosys', 'Meta', 'Wipro'];

  return (
    <Layout>
      <h1 className="text-2xl font-bold mb-6">Company Intelligence</h1>

      <Card title="Company Preparation">
        <div className="flex flex-wrap gap-2 mb-4">
          {companies.map((c) => (
            <button
              key={c}
              onClick={() => setCompany(c)}
              className={`px-3 py-1.5 rounded-full text-sm ${
                company === c ? 'bg-primary text-white' : 'bg-gray-100 text-gray-600'
              }`}
            >
              {c}
            </button>
          ))}
        </div>

        <input
          className="w-full border rounded-lg p-2 mb-3"
          value={role}
          onChange={(e) => setRole(e.target.value)}
          placeholder="Target role"
        />

        <div className="flex flex-wrap gap-2 mb-4">
          {([
            ['analyze', 'Analyze Company'],
            ['faqs', 'FAQs'],
            ['topics', 'Important Topics'],
            ['readiness', 'Readiness Report'],
          ] as const).map(([key, label]) => (
            <button
              key={key}
              onClick={() => setAction(key)}
              className={`px-3 py-2 rounded-lg text-sm ${
                action === key ? 'bg-primary text-white' : 'bg-gray-100'
              }`}
            >
              {label}
            </button>
          ))}
        </div>

        <button onClick={run} disabled={loading} className="bg-primary text-white px-6 py-2.5 rounded-lg">
          {loading ? 'Loading...' : 'Get Intelligence'}
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
