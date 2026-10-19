import { Link } from 'react-router-dom'
import { Badge, EmptyState, Spinner } from '../components/ui'
import { titleize } from '../utils/format'

export function toneFor(status?: string) {
  const s = (status || '').toLowerCase()
  if (['active', 'enrolling', 'completed', 'paid', 'valid', 'complete', 'eligible'].includes(s)) return 'success' as const
  if (['overdue', 'critical', 'withdrawn', 'screen_failed', 'missed'].includes(s)) return 'danger' as const
  if (['open', 'major', 'high', 'delayed', 'activating', 'scheduled'].includes(s)) return 'warning' as const
  if (['draft', 'startup', 'pending'].includes(s)) return 'info' as const
  return 'neutral' as const
}

export function StatusBadge({ value }: { value?: string }) {
  return <Badge tone={toneFor(value)}>{titleize(value)}</Badge>
}

export function DataTable<T extends { id: string }>({
  loading,
  rows,
  columns,
  href,
  empty,
}: {
  loading?: boolean
  rows?: T[] | null
  columns: Array<{ key: string; label: string; render?: (row: T) => unknown }>
  href?: (row: T) => string
  empty: string
}) {
  if (loading) return <Spinner label="Loading records…" />
  if (!rows?.length) return <EmptyState title={empty} />
  return (
    <div className="tr-table-wrap">
      <table className="tr-table">
        <thead>
          <tr>{columns.map((c) => <th key={c.key}>{c.label}</th>)}</tr>
        </thead>
        <tbody>
          {rows.map((row) => (
            <tr key={row.id}>
              {columns.map((c) => (
                <td key={c.key}>
                  {c.key === columns[0].key && href ? (
                    <Link to={href(row)}>{String((c.render ? c.render(row) : (row as Record<string, unknown>)[c.key]) ?? '—')}</Link>
                  ) : (
                    <>{c.render ? c.render(row) : String((row as Record<string, unknown>)[c.key] ?? '—')}</>
                  )}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}

export function results<T>(data: { results?: T[] } | T[] | null | undefined): T[] {
  if (!data) return []
  if (Array.isArray(data)) return data
  return data.results || []
}
