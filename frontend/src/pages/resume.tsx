import { useState } from 'react';
import Layout, { Card, LoadingSpinner, ErrorMessage, JsonViewer } from '../components/Layout';
import { api } from '../services/api';

export default function ResumePage() {
  const [text, setText] = useState('');
  const [jobDesc, setJobDesc] = useState('');
  const [result, setResult] = useState<unknown>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const analyze = async () => {
    if (!text.trim()) return;
    setLoading(true);
    setError('');
    try {
      const data = await api.resume.analyzeText(text, jobDesc || undefined);
      setResult(data);
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : 'Analysis failed');
    } finally {
      setLoading(false);
    }
  };

  const atsScore = (result as Record<string, unknown>)?.ats_analysis as Record<string, unknown> | undefined;

  return (
    <Layout>
      <h1 className="text-2xl font-bold mb-6">Resume Analysis</h1>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card title="Upload Resume Text">
          <textarea
            className="w-full h-48 border border-gray-300 rounded-lg p-3 text-sm"
            placeholder="Paste your resume text here..."
            value={text}
            onChange={(e) => setText(e.target.value)}
          />
          <textarea
            className="w-full h-20 border border-gray-300 rounded-lg p-3 text-sm mt-3"
            placeholder="Job description (optional)"
            value={jobDesc}
            onChange={(e) => setJobDesc(e.target.value)}
          />
          <button
            onClick={analyze}
            disabled={loading}
            className="mt-4 w-full bg-primary text-white py-2.5 rounded-lg font-medium hover:bg-blue-600 disabled:opacity-50"
          >
            {loading ? 'Analyzing...' : 'Analyze Resume'}
          </button>
        </Card>

        <div>
          {loading && <LoadingSpinner />}
          {error && <ErrorMessage message={error} />}
          {atsScore && (
            <Card title="ATS Score">
              <div className="text-5xl font-bold text-primary text-center mb-4">
                {atsScore.ats_score as number}
              </div>
            </Card>
          )}
          {result != null && (
            <Card title="Full Analysis" className="mt-4">
              <JsonViewer data={result} />
            </Card>
          )}
        </div>
      </div>
    </Layout>
  );
}
