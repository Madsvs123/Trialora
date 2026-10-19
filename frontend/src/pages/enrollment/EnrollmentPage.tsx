import { Bar, BarChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts'
import { reportsApi } from '../../api/client'
import { Card, PageHeader, StatCard } from '../../components/ui'
import { useApi } from '../../hooks/useApi'
import { formatNumber, pct } from '../../utils/format'
import { DataTable, results } from '../_shared'

export function EnrollmentPage() {
  const report = useApi(() => reportsApi.enrollment(), [])
  const data = report.data as { totals?: Record<string, number>; by_site?: Array<Record<string, unknown>> } | null
  const totals = data?.totals || {}
  const chart = (data?.by_site || []).map((row) => ({
    name: String(row.study_site__site__name || 'Site'),
    enrolled: Number(row.enrolled || 0),
    screened: Number(row.screened || 0),
  }))

  return (
    <div className="tr-page">
      <PageHeader title="Subject enrollment" subtitle="Screening rates, accrual, screen failures, withdrawals, and site-level targets." />
      <div className="tr-grid-stats">
        <StatCard label="Screened" value={formatNumber(totals.screened)} />
        <StatCard label="Enrolled" value={formatNumber(totals.enrolled)} hint={`${pct(totals.enrolled, totals.target)}% of target`} />
        <StatCard label="Screen failed" value={formatNumber(totals.screen_failed)} />
        <StatCard label="Active" value={formatNumber(totals.active)} />
        <StatCard label="Withdrawn" value={formatNumber(totals.withdrawn)} />
        <StatCard label="Completed" value={formatNumber(totals.completed)} />
      </div>
      <Card title="Enrollment by site">
        <div style={{ height: 280 }}>
          <ResponsiveContainer>
            <BarChart data={chart.length ? chart : [{ name: 'No data', enrolled: 0, screened: 0 }]}>
              <CartesianGrid strokeDasharray="3 3" stroke="var(--tr-line)" />
              <XAxis dataKey="name" />
              <YAxis />
              <Tooltip />
              <Bar dataKey="screened" fill="#6b9b7a" />
              <Bar dataKey="enrolled" fill="#1b4d3e" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </Card>
      <Card title="Site table">
        <DataTable
          loading={report.loading}
          rows={(data?.by_site || []).map((r, i) => ({ id: String(i), ...r }))}
          empty="No enrollment activity"
          columns={[
            { key: 'study__code', label: 'Study' },
            { key: 'study_site__site__name', label: 'Site' },
            { key: 'screened', label: 'Screened' },
            { key: 'enrolled', label: 'Enrolled' },
            { key: 'failed', label: 'Failed' },
            { key: 'withdrawn', label: 'Withdrawn' },
            { key: 'completed', label: 'Completed' },
          ]}
        />
      </Card>
    </div>
  )
}
