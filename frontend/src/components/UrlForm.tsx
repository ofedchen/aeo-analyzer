interface UrlFormProps {
  url: string
  loading: boolean
  onUrlChange: (value: string) => void
  onSubmit: (event: React.FormEvent) => void
}

export function UrlForm({ url, loading, onUrlChange, onSubmit }: UrlFormProps) {
  return (
    <form onSubmit={onSubmit} className="w-full max-w-2xl">
      <label htmlFor="url" className="mb-2 block text-sm font-medium text-muted">
        Website URL
      </label>
      <div className="flex flex-col gap-3 sm:flex-row">
        <input
          id="url"
          type="url"
          required
          placeholder="https://example.com"
          value={url}
          onChange={(event) => onUrlChange(event.target.value)}
          disabled={loading}
          className="flex-1 rounded-xl border border-border bg-panel px-4 py-3 text-base text-white outline-none transition focus:border-accent focus:ring-2 focus:ring-accent/30 disabled:opacity-60"
        />
        <button
          type="submit"
          disabled={loading}
          className="rounded-xl bg-accent-soft px-6 py-3 text-sm font-semibold text-white transition hover:bg-accent disabled:cursor-not-allowed disabled:opacity-60"
        >
          {loading ? 'Analyzing…' : 'Run AEO Check'}
        </button>
      </div>
    </form>
  )
}
