import { useEffect, useState } from 'react'
import { analyzeUrl } from './api'
import { Dashboard } from './components/Dashboard'
import { LoadingState } from './components/LoadingState'
import { UrlForm } from './components/UrlForm'
import type { AnalyzeResponse, AppStatus } from './types'

function App() {
  const [url, setUrl] = useState('https://example.com')
  const [status, setStatus] = useState<AppStatus>('idle')
  const [phaseIndex, setPhaseIndex] = useState(0)
  const [result, setResult] = useState<AnalyzeResponse | null>(null)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    if (status !== 'loading') return

    const timer = window.setInterval(() => {
      setPhaseIndex((current) => current + 1)
    }, 2200)

    return () => window.clearInterval(timer)
  }, [status])

  async function handleSubmit(event: React.FormEvent) {
    event.preventDefault()
    setStatus('loading')
    setPhaseIndex(0)
    setError(null)
    setResult(null)

    try {
      const data = await analyzeUrl(url.trim())
      setResult(data)
      setStatus('success')
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unexpected error')
      setStatus('error')
    }
  }

  return (
    <div className="mx-auto flex min-h-screen max-w-5xl flex-col items-center px-4 py-12 sm:px-6">
      <header className="mb-10 text-center">
        <p className="mb-2 text-xs font-semibold uppercase tracking-[0.2em] text-accent">
          AEO Validator
        </p>
        <h1 className="text-3xl font-bold text-white sm:text-4xl">
          AI Search Readiness Checker
        </h1>
        <p className="mx-auto mt-3 max-w-xl text-sm text-muted sm:text-base">
          Analyze llms.txt coverage, JSON-LD structure, and machine legibility with a
          two-agent CrewAI workflow powered by Gemini.
        </p>
      </header>

      <UrlForm
        url={url}
        loading={status === 'loading'}
        onUrlChange={setUrl}
        onSubmit={handleSubmit}
      />

      {status === 'loading' && <LoadingState phaseIndex={phaseIndex} />}

      {status === 'error' && error && (
        <div className="mt-10 w-full max-w-2xl rounded-2xl border border-danger/40 bg-danger/10 p-6 text-sm text-danger">
          {error}
        </div>
      )}

      {status === 'success' && result && <Dashboard data={result} />}
    </div>
  )
}

export default App
