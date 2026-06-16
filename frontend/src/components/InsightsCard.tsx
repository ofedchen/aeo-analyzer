import ReactMarkdown from 'react-markdown'

interface InsightsCardProps {
  summary: string
  actionItems: string[]
}

export function InsightsCard({ summary, actionItems }: InsightsCardProps) {
  const markdown = [
    '## Executive Summary',
    summary,
    '',
    '## Recommended Actions',
    ...actionItems.map((item, index) => `${index + 1}. ${item}`),
  ].join('\n')

  return (
    <div className="rounded-2xl border border-border bg-panel p-6">
      <h3 className="mb-4 text-lg font-semibold text-white">AI Insights</h3>
      <div className="prose prose-invert max-w-none prose-headings:text-accent prose-p:text-gray-300 prose-li:text-gray-300 prose-strong:text-white">
        <ReactMarkdown>{markdown}</ReactMarkdown>
      </div>
    </div>
  )
}
