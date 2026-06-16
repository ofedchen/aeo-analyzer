interface ProtocolBadgesProps {
  llmsTxtFound: boolean
  jsonLdFound: boolean
}

function Badge({ label, found }: { label: string; found: boolean }) {
  return (
    <div
      className={`flex items-center gap-2 rounded-xl border px-4 py-3 ${
        found
          ? 'border-success/40 bg-success/10 text-success'
          : 'border-danger/40 bg-danger/10 text-danger'
      }`}
    >
      <span className="text-lg">{found ? '✓' : '✗'}</span>
      <div>
        <p className="text-sm font-semibold">{label}</p>
        <p className="text-xs opacity-80">{found ? 'Detected' : 'Not found'}</p>
      </div>
    </div>
  )
}

export function ProtocolBadges({ llmsTxtFound, jsonLdFound }: ProtocolBadgesProps) {
  return (
    <div className="grid gap-3 sm:grid-cols-2">
      <Badge label="/llms.txt" found={llmsTxtFound} />
      <Badge label="JSON-LD Schema" found={jsonLdFound} />
    </div>
  )
}
