const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
const DEFAULT_TIMEOUT_MS = 8000;

async function request<T>(endpoint: string, options: RequestInit = {}, timeoutMs = DEFAULT_TIMEOUT_MS): Promise<T> {
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), timeoutMs);

  try {
    const res = await fetch(`${API_URL}${endpoint}`, {
      headers: { 'Content-Type': 'application/json', ...options.headers },
      signal: controller.signal,
      ...options,
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({ detail: res.statusText }));
      throw new Error(err.detail || 'Request failed');
    }
    return res.json();
  } catch (e) {
    if (e instanceof Error && e.name === 'AbortError') {
      throw new Error('Request timed out — is the backend running on port 8000?');
    }
    throw e;
  } finally {
    clearTimeout(timer);
  }
}

export const api = {
  health: () => request('/api/v1/health'),
  agentStatus: () => request('/api/v1/agents/status'),

  resume: {
    analyzeText: (resume_text: string, job_description?: string) =>
      request('/api/v1/resume/analyze-text', {
        method: 'POST',
        body: JSON.stringify({ resume_text, job_description }),
      }),
    list: () => request('/api/v1/resume/list'),
  },

  career: {
    create: (user_data: Record<string, unknown>) =>
      request('/api/v1/career/create', { method: 'POST', body: JSON.stringify(user_data) }),
    analyzeGaps: (data: Record<string, unknown>) =>
      request('/api/v1/career/analyze-gaps', { method: 'POST', body: JSON.stringify(data) }),
    generateRoadmap: (data: Record<string, unknown>) =>
      request('/api/v1/career/generate-roadmap', { method: 'POST', body: JSON.stringify(data) }),
    myPlan: () => request('/api/v1/career/my-plan'),
  },

  dsa: {
    logProblem: (data: Record<string, unknown>) =>
      request('/api/v1/dsa/log-problem', { method: 'POST', body: JSON.stringify(data) }),
    weakTopics: () => request('/api/v1/dsa/weak-topics'),
    dailyPlan: (data: Record<string, unknown>) =>
      request('/api/v1/dsa/daily-plan', { method: 'POST', body: JSON.stringify(data) }),
    consistency: (days = 30) => request(`/api/v1/dsa/consistency?days=${days}`),
    progress: () => request('/api/v1/dsa/progress'),
    problems: () => request('/api/v1/dsa/problems'),
  },

  analytics: {
    summary: () => request('/api/v1/analytics/summary', {}, 5000),
    readiness: () => request('/api/v1/analytics/readiness-score'),
    skills: () => request('/api/v1/analytics/skills'),
    progress: () => request('/api/v1/analytics/progress'),
    prediction: () => request('/api/v1/analytics/placement-prediction'),
    dashboard: () => request('/api/v1/analytics/dashboard', {}, 60000),
    snapshot: () => request('/api/v1/analytics/snapshot', { method: 'POST' }),
  },

  interview: {
    start: (data: Record<string, unknown>) =>
      request('/api/v1/interview/start', { method: 'POST', body: JSON.stringify(data) }),
    submitAnswer: (data: Record<string, unknown>) =>
      request('/api/v1/interview/submit-answer', { method: 'POST', body: JSON.stringify(data) }),
    complete: (sessionId: string) =>
      request(`/api/v1/interview/complete/${sessionId}`, { method: 'POST' }),
    evaluateCode: (data: Record<string, unknown>) =>
      request('/api/v1/interview/evaluate-code', { method: 'POST', body: JSON.stringify(data) }),
    sessions: () => request('/api/v1/interview/sessions'),
  },

  company: {
    analyze: (data: Record<string, unknown>) =>
      request('/api/v1/company/analyze', { method: 'POST', body: JSON.stringify(data) }),
    faqs: (data: Record<string, unknown>) =>
      request('/api/v1/company/faqs', { method: 'POST', body: JSON.stringify(data) }),
    topics: (data: Record<string, unknown>) =>
      request('/api/v1/company/important-topics', { method: 'POST', body: JSON.stringify(data) }),
    readiness: (data: Record<string, unknown>) =>
      request('/api/v1/company/readiness-report', { method: 'POST', body: JSON.stringify(data) }),
    compare: (data: Record<string, unknown>) =>
      request('/api/v1/company/compare', { method: 'POST', body: JSON.stringify(data) }),
    search: (query: string, company?: string) =>
      request(`/api/v1/company/search?query=${encodeURIComponent(query)}${company ? `&company=${company}` : ''}`),
  },

  voice: {
    analyze: (data: Record<string, unknown>) =>
      request('/api/v1/voice/analyze', { method: 'POST', body: JSON.stringify(data) }),
    completeSession: (data: Record<string, unknown>) =>
      request('/api/v1/voice/complete-session', { method: 'POST', body: JSON.stringify(data) }),
    practicePrompts: (data: Record<string, unknown>) =>
      request('/api/v1/voice/practice-prompts', { method: 'POST', body: JSON.stringify(data) }),
  },
};
