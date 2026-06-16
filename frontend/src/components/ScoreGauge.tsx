interface ScoreGaugeProps {
  score: number
}

function scoreColor(score: number): string {
  if (score >= 75) return 'text-success'
  if (score >= 50) return 'text-warning'
  return 'text-danger'
}

function scoreLabel(score: number): string {
  if (score >= 75) return 'Strong'
  if (score >= 50) return 'Moderate'
  return 'Needs work'
}

export function ScoreGauge({ score }: ScoreGaugeProps) {
  const clamped = Math.max(0, Math.min(score, 100))
  const circumference = 2 * Math.PI * 54
  const offset = circumference - (clamped / 100) * circumference

  return (
    <div className="flex flex-col items-center">
      <div className="relative h-40 w-40">
        <svg className="h-full w-full -rotate-90" viewBox="0 0 120 120">
          <circle
            cx="60"
            cy="60"
            r="54"
            fill="none"
            stroke="currentColor"
            strokeWidth="10"
            className="text-border"
          />
          <circle
            cx="60"
            cy="60"
            r="54"
            fill="none"
            stroke="currentColor"
            strokeWidth="10"
            strokeLinecap="round"
            strokeDasharray={circumference}
            strokeDashoffset={offset}
            className={`${scoreColor(clamped)} transition-all duration-700`}
          />
        </svg>
        <div className="absolute inset-0 flex flex-col items-center justify-center">
          <span className={`text-4xl font-bold ${scoreColor(clamped)}`}>{clamped}</span>
          <span className="text-xs uppercase tracking-wider text-muted">/ 100</span>
        </div>
      </div>
      <p className="mt-3 text-sm font-medium text-gray-200">Machine Legibility Score</p>
      <p className={`text-xs ${scoreColor(clamped)}`}>{scoreLabel(clamped)}</p>
    </div>
  )
}
