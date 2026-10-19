import { useParams } from 'react-router-dom'
import { visitsApi } from '../../api/client'
import type { Visit } from '../../api/types'
import { Card, PageHeader, StatCard } from '../../components/ui'
import { useApi } from '../../hooks/useApi'
import { DataTable, results, StatusBadge } from '../_shared'

export function VisitListPage() {
  const list = useApi(() => visitsApi.list({ page_size: 80 }), [])
  const rows = results<Visit>(list.data)
  const overdue = rows.filter((v) => v.status === 'overdue').length
  const missed = rows.filter((v) => v.status === 'missed').length

  return (
    <div className="tr-page">
      <PageHeader title="Visits" subtitle="Visit windows, scheduled assessments, missed visits, follow-ups, and completion." />
      <div className="tr-grid-stats">
        <StatCard label="Scheduled" value={rows.filter((v) => v.status === 'scheduled').length} />
        <StatCard label="Overdue" value={overdue} />
        <StatCard label="Missed" value={missed} />
        <StatCard label="Completed" value={rows.filter((v) => v.status === 'completed').length} />
      </div>
      <Card>
        <DataTable
          loading={list.loading}
          rows={rows}
          empty="No visits"
          href={(row) => `/app/visits/${row.id}`}
          columns={[
            { key: 'name', label: 'Visit' },
            { key: 'subject_id', label: 'Subject' },
            { key: 'scheduled_date', label: 'Scheduled' },
            { key: 'window_end', label: 'Window end' },
            { key: 'status', label: 'Status', render: (r) => <StatusBadge value={r.status} /> },
          ]}
        />
      </Card>
    </div>
  )
}

export function VisitDetailPage() {
  const { id = '' } = useParams()
  const item = useApi(() => visitsApi.retrieve(id) as Promise<Visit>, [id])
  const v = item.data
  return (
    <div className="tr-page">
      <PageHeader title={v?.name || 'Visit'} subtitle={`Subject ${v?.subject_id || ''}`} />
      <Card title="Visit window">
        <p>Scheduled {v?.scheduled_date || '—'} · Actual {v?.actual_date || 'not completed'} · Status <StatusBadge value={v?.status} /></p>
      </Card>
    </div>
  )
}
