import { useParams } from 'react-router-dom'
import { actionItemsApi, findingsApi, monitoringApi, riskApi } from '../../api/client'
import { Card, PageHeader, StatCard } from '../../components/ui'
import { useApi } from '../../hooks/useApi'
import { DataTable, results, StatusBadge } from '../_shared'

export function MonitoringPage() {
  const visits = useApi(() => monitoringApi.list({ page_size: 40 }), [])
  const findings = useApi(() => findingsApi.list({ page_size: 40 }), [])
  const actions = useApi(() => actionItemsApi.list({ page_size: 20, status: 'open' }), [])
  const risks = useApi(() => riskApi.list({ page_size: 20 }), [])

  return (
    <div className="tr-page">
      <PageHeader title="Monitoring" subtitle="Monitoring visits, trip reports, findings, action items, follow-up letters, and risk indicators." />
      <div className="tr-grid-stats">
        <StatCard label="Visits" value={results(visits.data).length} />
        <StatCard label="Open findings" value={results(findings.data).filter((f) => (f as { status: string }).status === 'open').length} />
        <StatCard label="Open actions" value={results(actions.data).length} />
      </div>
      <Card title="Monitoring visits">
        <DataTable loading={visits.loading} rows={results(visits.data)} empty="No monitoring visits" href={(r) => `/app/monitoring/${r.id}`} columns={[{ key: 'kind', label: 'Type' }, { key: 'scheduled_date', label: 'Scheduled' }, { key: 'status', label: 'Status', render: (r) => <StatusBadge value={String((r as { status: string }).status)} /> }, { key: 'monitor_name', label: 'Monitor' }]} />
      </Card>
      <Card title="Findings">
        <DataTable loading={findings.loading} rows={results(findings.data)} empty="No findings" columns={[{ key: 'title', label: 'Finding' }, { key: 'severity', label: 'Severity', render: (r) => <StatusBadge value={String((r as { severity: string }).severity)} /> }, { key: 'status', label: 'Status' }, { key: 'due_date', label: 'Due' }]} />
      </Card>
      <Card title="Risk indicators">
        <DataTable loading={risks.loading} rows={results(risks.data)} empty="No risk signals" columns={[{ key: 'name', label: 'Indicator' }, { key: 'score', label: 'Score' }, { key: 'trend', label: 'Trend' }]} />
      </Card>
    </div>
  )
}

export function MonitoringDetailPage() {
  const { id = '' } = useParams()
  const item = useApi(() => monitoringApi.retrieve(id), [id])
  const v = item.data as Record<string, unknown> | null
  return (
    <div className="tr-page">
      <PageHeader title="Monitoring visit" subtitle={String(v?.kind || '')} />
      <Card title="Visit record">
        <p>Scheduled {String(v?.scheduled_date || '—')} · Status <StatusBadge value={String(v?.status || '')} /></p>
        <p className="tr-muted" style={{ marginTop: 8 }}>{String(v?.agenda || 'No agenda recorded.')}</p>
      </Card>
    </div>
  )
}
