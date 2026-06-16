export interface Protocols {
  llms_txt_found: boolean
  json_ld_found: boolean
}

export interface Metrics {
  legibility_score: number
}

export interface Analysis {
  summary: string
  action_items: string[]
}

export interface AnalyzeResponse {
  target_url: string
  protocols: Protocols
  metrics: Metrics
  analysis: Analysis
}

export type AppStatus = 'idle' | 'loading' | 'success' | 'error'
