import type { AnalyzeResponse } from './types'

const API_BASE = import.meta.env.VITE_API_BASE ?? 'http://127.0.0.1:8000'

export async function analyzeUrl(url: string): Promise<AnalyzeResponse> {
  const params = new URLSearchParams({ url })
  const response = await fetch(`${API_BASE}/api/analyze?${params.toString()}`, {
    method: 'POST',
  })

  if (!response.ok) {
    const payload = await response.json().catch(() => ({}))
    const detail =
      typeof payload.detail === 'string'
        ? payload.detail
        : 'Analysis request failed. Check the backend logs.'
    throw new Error(detail)
  }

  return response.json()
}
