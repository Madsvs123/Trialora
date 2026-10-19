import { resource } from '../../api/client'
import { Card, PageHeader, StatCard } from '../../components/ui'
import { useApi } from '../../hooks/useApi'
import { DataTable, results, StatusBadge } from '../_shared'

const committeesApi = resource('ethics-committees')
const submissionsApi = resource('submissions')
const approvalsApi = resource('approvals')
const obligationsApi = resource('regulatory-obligations')

export function RegulatoryPage() {
  const committees = useApi(() => committeesApi.list({ page_size: 30 }), [])
  const submissions = useApi(() => submissionsApi.list({ page_size: 40 }), [])
  const approvals = useApi(() => approvalsApi.list({ page_size: 40 }), [])
  const obligations = useApi(() => obligationsApi.list({ page_size: 30 }), [])

  return (
    <div className="tr-page">
      <PageHeader title="Regulatory" subtitle="IRB/EC committees, submissions, approvals, amendments, and country obligations." />
      <div className="tr-grid-stats">
        <StatCard label="Committees" value={results(committees.data).length} />
        <StatCard label="Submissions" value={results(submissions.data).length} />
        <StatCard label="Active approvals" value={results(approvals.data).filter((r) => (r as { status: string }).status === 'active').length} />
        <StatCard label="Open obligations" value={results(obligations.data).filter((r) => (r as { status: string }).status === 'open').length} />
      </div>
      <Card title="Ethics committees">
        <DataTable loading={committees.loading} rows={results(committees.data)} empty="No committees" columns={[{ key: 'name', label: 'Committee' }, { key: 'kind', label: 'Type' }, { key: 'city', label: 'City' }, { key: 'is_central', label: 'Central' }]} />
      </Card>
      <Card title="Submissions">
        <DataTable loading={submissions.loading} rows={results(submissions.data)} empty="No submissions" columns={[{ key: 'title', label: 'Submission' }, { key: 'kind', label: 'Kind' }, { key: 'status', label: 'Status', render: (r) => <StatusBadge value={String((r as { status: string }).status)} /> }, { key: 'submitted_on', label: 'Submitted' }]} />
      </Card>
      <Card title="Approvals">
        <DataTable loading={approvals.loading} rows={results(approvals.data)} empty="No approvals" columns={[{ key: 'number', label: 'Number' }, { key: 'approved_on', label: 'Approved' }, { key: 'expires_on', label: 'Expires' }, { key: 'status', label: 'Status' }]} />
      </Card>
      <Card title="Obligations">
        <DataTable loading={obligations.loading} rows={results(obligations.data)} empty="No obligations" columns={[{ key: 'name', label: 'Obligation' }, { key: 'authority', label: 'Authority' }, { key: 'due_date', label: 'Due' }, { key: 'status', label: 'Status' }]} />
      </Card>
    </div>
  )
}
