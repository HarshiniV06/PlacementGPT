import { useEffect, useState } from 'react';
import Layout, { Card, LoadingSpinner, ErrorMessage, JsonViewer } from '../components/Layout';
import { api } from '../services/api';

export default function DSAPage() {
  const [progress, setProgress] = useState<unknown>(null);
  const [plan, setPlan] = useState<unknown>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const [title, setTitle] = useState('');
  const [topic, setTopic] = useState('arrays');
  const [difficulty, setDifficulty] = useState('medium');
  const [platform, setPlatform] = useState('leetcode');

  useEffect(() => {
    api.dsa.progress().then(setProgress).catch(() => {});
  }, []);

  const logProblem = async () => {
    if (!title.trim()) return;
    setLoading(true);
    setError('');
    try {
      await api.dsa.logProblem({
        problem_title: title,
        topic,
        difficulty,
        platform,
        is_correct: true,
        time_taken: 30,
      });
      setTitle('');
      const p = await api.dsa.progress();
      setProgress(p);
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : 'Failed');
    } finally {
      setLoading(false);
    }
  };

  const generatePlan = async () => {
    setLoading(true);
    setError('');
    try {
      const data = await api.dsa.dailyPlan({ available_hours: 2 });
      setPlan(data);
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : 'Failed');
    } finally {
      setLoading(false);
    }
  };

  const prog = progress as Record<string, unknown> | null;
  const dsaScore = prog?.dsa_score as Record<string, unknown> | undefined;

  return (
    <Layout>
      <h1 className="text-2xl font-bold mb-6">DSA Tracker</h1>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
        <Card className="text-center">
          <div className="text-3xl font-bold text-primary">
            {(dsaScore?.dsa_score as number) || 0}
          </div>
          <div className="text-sm text-gray-500">DSA Score</div>
        </Card>
        <Card className="text-center">
          <div className="text-3xl font-bold text-secondary">
            {(prog?.total_problems as number) || 0}
          </div>
          <div className="text-sm text-gray-500">Problems Solved</div>
        </Card>
        <Card className="text-center">
          <div className="text-3xl font-bold text-accent">
            {((prog?.consistency as Record<string, unknown>)?.consistency_score as number) || 0}%
          </div>
          <div className="text-sm text-gray-500">Consistency</div>
        </Card>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card title="Log a Problem">
          <input
            className="w-full border rounded-lg p-2 mb-3"
            placeholder="Problem title"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
          />
          <div className="grid grid-cols-3 gap-2 mb-3">
            <select className="border rounded-lg p-2" value={topic} onChange={(e) => setTopic(e.target.value)}>
              {['arrays', 'strings', 'trees', 'graphs', 'dp', 'greedy', 'binary search'].map((t) => (
                <option key={t} value={t}>{t}</option>
              ))}
            </select>
            <select className="border rounded-lg p-2" value={difficulty} onChange={(e) => setDifficulty(e.target.value)}>
              {['easy', 'medium', 'hard'].map((d) => (
                <option key={d} value={d}>{d}</option>
              ))}
            </select>
            <select className="border rounded-lg p-2" value={platform} onChange={(e) => setPlatform(e.target.value)}>
              {['leetcode', 'gfg', 'codeforces'].map((p) => (
                <option key={p} value={p}>{p}</option>
              ))}
            </select>
          </div>
          <button onClick={logProblem} disabled={loading} className="w-full bg-primary text-white py-2 rounded-lg">
            Log Problem
          </button>
        </Card>

        <Card title="Daily Plan">
          <button onClick={generatePlan} disabled={loading} className="w-full bg-secondary text-white py-2 rounded-lg mb-4">
            Generate Today&apos;s Plan
          </button>
          {plan != null && <JsonViewer data={plan} />}
        </Card>
      </div>

      {loading && <LoadingSpinner />}
      {error && <div className="mt-4"><ErrorMessage message={error} /></div>}
    </Layout>
  );
}
