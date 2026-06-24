import { useState } from 'react';
import Layout, { Card, LoadingSpinner, ErrorMessage, JsonViewer } from '../components/Layout';
import { api } from '../services/api';

export default function InterviewPage() {
  const [session, setSession] = useState<Record<string, unknown> | null>(null);
  const [currentQ, setCurrentQ] = useState(0);
  const [answer, setAnswer] = useState('');
  const [evaluation, setEvaluation] = useState<unknown>(null);
  const [finalResult, setFinalResult] = useState<unknown>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [type, setType] = useState<'technical' | 'hr'>('technical');

  const start = async () => {
    setLoading(true);
    setError('');
    setFinalResult(null);
    setEvaluation(null);
    try {
      const data = await api.interview.start({
        interview_type: type,
        role: 'Software Engineer',
        difficulty: 'medium',
        question_count: 3,
      });
      setSession(data as Record<string, unknown>);
      setCurrentQ(0);
      setAnswer('');
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : 'Failed to start');
    } finally {
      setLoading(false);
    }
  };

  const submit = async () => {
    if (!session || !answer.trim()) return;
    const questions = session.questions as Array<Record<string, unknown>>;
    const q = questions[currentQ];
    setLoading(true);
    try {
      const evalResult = await api.interview.submitAnswer({
        session_id: session.session_id,
        question: q.question as string,
        answer,
      });
      setEvaluation(evalResult);

      if (currentQ < questions.length - 1) {
        setCurrentQ(currentQ + 1);
        setAnswer('');
        setEvaluation(null);
      } else {
        const result = await api.interview.complete(session.session_id as string);
        setFinalResult(result);
      }
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : 'Submit failed');
    } finally {
      setLoading(false);
    }
  };

  const questions = (session?.questions as Array<Record<string, unknown>>) || [];

  return (
    <Layout>
      <h1 className="text-2xl font-bold mb-6">Mock Interview</h1>

      {!session && (
        <Card title="Start Interview">
          <div className="flex gap-2 mb-4">
            {(['technical', 'hr'] as const).map((t) => (
              <button
                key={t}
                onClick={() => setType(t)}
                className={`px-4 py-2 rounded-lg text-sm font-medium capitalize ${
                  type === t ? 'bg-primary text-white' : 'bg-gray-100'
                }`}
              >
                {t}
              </button>
            ))}
          </div>
          <button onClick={start} disabled={loading} className="bg-primary text-white px-6 py-2.5 rounded-lg">
            Start {type} Interview
          </button>
        </Card>
      )}

      {session && !finalResult && questions.length > 0 && (
        <Card title={`Question ${currentQ + 1} of ${questions.length}`}>
          <p className="text-gray-800 mb-4">{questions[currentQ]?.question as string}</p>
          <textarea
            className="w-full h-32 border rounded-lg p-3"
            placeholder="Type your answer..."
            value={answer}
            onChange={(e) => setAnswer(e.target.value)}
          />
          <button onClick={submit} disabled={loading} className="mt-3 bg-secondary text-white px-6 py-2 rounded-lg">
            {currentQ < questions.length - 1 ? 'Next Question' : 'Finish Interview'}
          </button>
          {evaluation != null && (
            <div className="mt-4">
              <JsonViewer data={evaluation} />
            </div>
          )}
        </Card>
      )}

      {finalResult != null && (
        <Card title="Interview Results">
          <JsonViewer data={finalResult} />
        </Card>
      )}

      {loading && <LoadingSpinner />}
      {error && <div className="mt-4"><ErrorMessage message={error} /></div>}
    </Layout>
  );
}
