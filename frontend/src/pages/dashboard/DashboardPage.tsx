import { Activity, AlertTriangle, Building2, FolderKanban } from 'lucide-react'
import { useNavigate } from 'react-router-dom'
import { Area, AreaChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts'
import { reportsApi, issuesApi, visitsApi } from '../../api/client'
import { Card, PageHeader, Spinner, StatCard } from '../../components/ui'
import { useApi } from '../../hooks/useApi'
import { formatNumber } from '../../utils/format'
import { DataTable, results, StatusBadge } from '../_shared'
import type { Issue, Visit } from '../../api/types'

const spark = [
  { name: 'Jan', enrolled: 8 },
  { name: 'Feb', enrolled: 16 },
  { name: 'Mar', enrolled: 29 },
  { name: 'Apr', enrolled: 41 },
  { name: 'May', enrolled: 54 },
  { name: 'Jun', enrolled: 68 },
]

export function DashboardPage() {
  const navigate = useNavigate()
  const dash = useApi(() => reportsApi.dashboard(), [])
  const issues = useApi(() => issuesApi.list({ page_size: 6, status: 'open' }), [])
  const visits = useApi(() => visitsApi.list({ page_size: 6, status: 'overdue' }), [])
  const d = dash.data as Record<string, Record<string, number>> | null

  if (dash.loading && !d) {
    return <div style={{ padding: 48 }}><Spinner label="Assembling the study portfolio…" /></div>
  }

  return (
    <div className="tr-page">
      <PageHeader title="Command center" subtitle="Enrollment, site activation, monitoring risk, and study progress across the organization." />
      {dash.error && <p style={{ color: 'var(--tr-danger)' }}>{dash.error}</p>}
      <div className="tr-grid-stats">
        <StatCard label="Studies" value={formatNumber(d?.studies?.total)} hint={`${d?.studies?.enrolling || 0} enrolling`} icon={<FolderKanban size={16} />} />
        <StatCard label="Enrolled" value={formatNumber(d?.enrollment?.enrolled)} hint={`${formatNumber(d?.enrollment?.target)} target`} icon={<Activity size={16} />} />
        <StatCard label="Active sites" value={formatNumber(d?.sites?.active)} hint={`${d?.sites?.activating || 0} activating`} icon={<Building2 size={16} />} />
        <StatCard label="Open risks" value={formatNumber((d?.risks?.open_issues || 0) + (d?.risks?.open_findings || 0))} hint={`${d?.visits?.overdue || 0} overdue visits`} icon={<AlertTriangle size={16} />} />
        <StatCard label="Open AEs" value={formatNumber(d?.safety?.open)} hint={`${d?.safety?.saes || 0} serious`} />
        <StatCard label="Approvals" value={formatNumber(d?.regulatory?.active_approvals)} hint={`${d?.regulatory?.expiring || 0} expired`} />
        <StatCard label="Available kits" value={formatNumber(d?.inventory?.available_kits)} hint={`${d?.inventory?.quarantine || 0} quarantine`} />
      </div>
      <div style={{ display: 'grid', gridTemplateColumns: '1.4fr 1fr', gap: 16 }}>
        <Card title="Enrollment trajectory" subtitle="Portfolio-level subject accrual">
          <div style={{ height: 240 }}>
            <ResponsiveContainer>
              <AreaChart data={spark}>
                <CartesianGrid strokeDasharray="3 3" stroke="var(--tr-line)" />
                <XAxis dataKey="name" />
                <YAxis />
                <Tooltip />
                <Area type="monotone" dataKey="enrolled" stroke="#1b4d3e" fill="#3d7a64" fillOpacity={0.25} />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </Card>
        <Card title="Screening funnel">
          <div style={{ display: 'grid', gap: 10 }}>
            {[
              ['Screened', d?.enrollment?.screened],
              ['Screen failed', d?.enrollment?.screen_failed],
              ['Active', d?.enrollment?.active],
              ['Withdrawn', d?.enrollment?.withdrawn],
              ['Completed', d?.enrollment?.completed],
            ].map(([label, value]) => (
              <div key={String(label)} style={{ display: 'flex', justifyContent: 'space-between' }}>
                <span className="tr-muted">{label}</span>
                <strong>{formatNumber(value as number)}</strong>
              </div>
            ))}
          </div>
        </Card>
      </div>
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 16 }}>
        <Card title="Open issues" actions={<button onClick={() => navigate('/app/issues')} style={{ border: 0, background: 'none', cursor: 'pointer' }}>View all</button>}>
          <DataTable
            loading={issues.loading}
            rows={results<Issue>(issues.data)}
            empty="No open issues"
            href={(row) => `/app/issues/${row.id}`}
            columns={[
              { key: 'title', label: 'Issue' },
              { key: 'severity', label: 'Severity', render: (r) => <StatusBadge value={r.severity} /> },
              { key: 'status', label: 'Status', render: (r) => <StatusBadge value={r.status} /> },
            ]}
          />
        </Card>
        <Card title="Overdue visits">
          <DataTable
            loading={visits.loading}
            rows={results<Visit>(visits.data)}
            empty="No overdue visits"
            href={(row) => `/app/visits/${row.id}`}
            columns={[
              { key: 'name', label: 'Visit' },
              { key: 'subject_id', label: 'Subject' },
              { key: 'scheduled_date', label: 'Scheduled' },
            ]}
          />
        </Card>
      </div>
    </div>
  )
}
