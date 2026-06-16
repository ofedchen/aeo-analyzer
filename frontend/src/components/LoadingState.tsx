const PHASES = [
  'Agent 1 is crawling the site schema…',
  'Agent 1 is fetching /llms.txt…',
  'Agent 1 is extracting JSON-LD blocks…',
  'Agent 2 is analyzing machine legibility…',
  'Agent 2 is generating optimization insights…',
]

interface LoadingStateProps {
  phaseIndex: number
}

export function LoadingState({ phaseIndex }: LoadingStateProps) {
  const message = PHASES[phaseIndex % PHASES.length]

  return (
    <div className="mt-10 w-full max-w-2xl rounded-2xl border border-border bg-panel/80 p-8 backdrop-blur">
      <div className="mb-4 flex items-center gap-3">
        <span className="inline-block h-3 w-3 animate-pulse rounded-full bg-accent" />
        <p className="text-sm font-medium text-accent">{message}</p>
      </div>
      <div className="h-2 overflow-hidden rounded-full bg-border">
        <div
          className="h-full rounded-full bg-gradient-to-r from-accent-soft to-accent transition-all duration-700 ease-out"
          style={{ width: `${((phaseIndex % PHASES.length) + 1) * (100 / PHASES.length)}%` }}
        />
      </div>
      <p className="mt-4 text-xs text-muted">
        Two-agent workflow: Technical Crawler → AEO Strategist
      </p>
    </div>
  )
}
