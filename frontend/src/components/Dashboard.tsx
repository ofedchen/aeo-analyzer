import type { AnalyzeResponse } from '../types'
import { InsightsCard } from './InsightsCard'
import { ProtocolBadges } from './ProtocolBadges'
import { ScoreGauge } from './ScoreGauge'

interface DashboardProps {
  data: AnalyzeResponse
}

export function Dashboard({ data }: DashboardProps) {
  return (
    <div className="mt-10 w-full max-w-4xl space-y-6">
      <div className="rounded-2xl border border-border bg-panel/80 p-6 backdrop-blur">
        <p className="text-xs uppercase tracking-wider text-muted">Target</p>
        <a
          href={data.target_url}
          target="_blank"
          rel="noreferrer"
          className="mt-1 block truncate text-lg font-medium text-accent hover:underline"
        >
          {data.target_url}
        </a>
      </div>

      <div className="grid gap-6 lg:grid-cols-[auto_1fr]">
        <div className="rounded-2xl border border-border bg-panel p-6">
          <ScoreGauge score={data.metrics.legibility_score} />
        </div>
        <div className="rounded-2xl border border-border bg-panel p-6">
          <h3 className="mb-4 text-lg font-semibold text-white">Protocol Checklist</h3>
          <ProtocolBadges
            llmsTxtFound={data.protocols.llms_txt_found}
            jsonLdFound={data.protocols.json_ld_found}
          />
        </div>
      </div>

      <InsightsCard
        summary={data.analysis.summary}
        actionItems={data.analysis.action_items}
      />
    </div>
  )
}
