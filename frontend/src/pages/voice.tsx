import { useState } from 'react';
import Layout, { Card, LoadingSpinner, ErrorMessage, JsonViewer } from '../components/Layout';
import { api } from '../services/api';

export default function VoicePage() {
  const [transcript, setTranscript] = useState('');
  const [question, setQuestion] = useState('Tell me about yourself.');
  const [duration, setDuration] = useState(60);
  const [result, setResult] = useState<unknown>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [isRecording, setIsRecording] = useState(false);

  const analyze = async () => {
    if (!transcript.trim()) return;
    setLoading(true);
    setError('');
    try {
      const data = await api.voice.analyze({
        transcript,
        question,
        duration_seconds: duration,
      });
      setResult(data);
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : 'Analysis failed');
    } finally {
      setLoading(false);
    }
  };

  const startRecording = () => {
    if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
      setError('Speech recognition not supported in this browser. Type your answer instead.');
      return;
    }
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    const SpeechRecognitionCtor = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;
    const recognition = new SpeechRecognitionCtor();
    recognition.continuous = true;
    recognition.interimResults = true;
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    recognition.onresult = (event: any) => {
      let text = '';
      for (let i = 0; i < event.results.length; i++) {
        text += event.results[i][0].transcript;
      }
      setTranscript(text);
    };
    recognition.onend = () => setIsRecording(false);
    recognition.start();
    setIsRecording(true);
  };

  const metrics = (result as Record<string, unknown>)?.speech_metrics as Record<string, unknown> | undefined;
  const delivery = (result as Record<string, unknown>)?.delivery_analysis as Record<string, unknown> | undefined;

  return (
    <Layout>
      <h1 className="text-2xl font-bold mb-6">Voice Interview Practice</h1>
      <p className="text-gray-500 mb-6">
        Practice speaking your answers. Use the microphone or type your response.
      </p>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card title="Practice Response">
          <input
            className="w-full border rounded-lg p-2 mb-3"
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            placeholder="Interview question"
          />
          <textarea
            className="w-full h-40 border rounded-lg p-3"
            placeholder="Your spoken answer (or use microphone)..."
            value={transcript}
            onChange={(e) => setTranscript(e.target.value)}
          />
          <div className="flex gap-2 mt-3">
            <button
              onClick={startRecording}
              disabled={isRecording}
              className={`px-4 py-2 rounded-lg text-white ${isRecording ? 'bg-danger' : 'bg-accent'}`}
            >
              {isRecording ? 'Recording...' : 'Start Mic'}
            </button>
            <button onClick={analyze} disabled={loading} className="px-4 py-2 rounded-lg bg-primary text-white">
              Analyze Delivery
            </button>
          </div>
        </Card>

        <div>
          {loading && <LoadingSpinner />}
          {error && <ErrorMessage message={error} />}
          {metrics && (
            <Card title="Speech Metrics">
              <div className="grid grid-cols-2 gap-4 text-center">
                <div>
                  <div className="text-2xl font-bold">{metrics.word_count as number}</div>
                  <div className="text-xs text-gray-500">Words</div>
                </div>
                <div>
                  <div className="text-2xl font-bold text-danger">{metrics.filler_word_count as number}</div>
                  <div className="text-xs text-gray-500">Filler Words</div>
                </div>
                <div>
                  <div className="text-2xl font-bold">{metrics.words_per_minute as number || 'N/A'}</div>
                  <div className="text-xs text-gray-500">WPM</div>
                </div>
                <div>
                  <div className="text-2xl font-bold text-primary">
                    {(delivery?.overall_delivery_score as number) || 0}
                  </div>
                  <div className="text-xs text-gray-500">Delivery Score</div>
                </div>
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
