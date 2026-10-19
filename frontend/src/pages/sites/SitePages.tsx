import { useState } from 'react'
import { useParams } from 'react-router-dom'
import { contractsApi, feasibilityApi, siteMetricsApi, sitesApi, studySitesApi } from '../../api/client'
import type { Site, StudySite } from '../../api/types'
import { Button, Card, Input, Modal, PageHeader, StatCard } from '../../components/ui'
import { useApi, useMutation } from '../../hooks/useApi'
import { DataTable, results, StatusBadge } from '../_shared'

export function SiteListPage() {
  const list = useApi(() => sitesApi.list({ page_size: 50 }), [])
  const [open, setOpen] = useState(false)
  const [form, setForm] = useState({ name: '', institution: '', city: '' })
  const create = useMutation((body: typeof form) => sitesApi.create(body))

  return (
    <div className="tr-page">
      <PageHeader title="Sites" subtitle="Feasibility, activation, contracts, contacts, and site performance." actions={<Button onClick={() => setOpen(true)}>Add site</Button>} />
      <Card>
        <DataTable
          loading={list.loading}
          rows={results<Site>(list.data)}
          empty="No sites"
          href={(row) => `/app/sites/${row.id}`}
          columns={[
            { key: 'name', label: 'Site' },
            { key: 'institution', label: 'Institution' },
            { key: 'city', label: 'City' },
            { key: 'country_name', label: 'Country' },
            { key: 'pi_name', label: 'Investigator' },
          ]}
        />
      </Card>
      <Modal open={open} title="New site" onClose={() => setOpen(false)}>
        <form className="tr-form" onSubmit={async (e) => { e.preventDefault(); await create.mutate(form); setOpen(false); list.reload() }}>
          <Input label="Name" value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} required />
          <Input label="Institution" value={form.institution} onChange={(e) => setForm({ ...form, institution: e.target.value })} />
          <Input label="City" value={form.city} onChange={(e) => setForm({ ...form, city: e.target.value })} />
          <Button type="submit">Save site</Button>
        </form>
      </Modal>
    </div>
  )
}

export function SiteDetailPage() {
  const { id = '' } = useParams()
  const site = useApi(() => sitesApi.retrieve(id) as Promise<Site>, [id])
  const participations = useApi(() => studySitesApi.list({ site: id }), [id])
  const feasibility = useApi(() => feasibilityApi.list({ page_size: 10 }), [id])
  const contracts = useApi(() => contractsApi.list({ page_size: 10 }), [id])
  const metrics = useApi(() => siteMetricsApi.list({ page_size: 10 }), [id])
  const s = site.data

  return (
    <div className="tr-page">
      <PageHeader title={s?.name || 'Site'} subtitle={`${s?.institution || ''} · ${s?.city || ''}`} />
      <div className="tr-grid-stats">
        <StatCard label="Country" value={s?.country_name || '—'} />
        <StatCard label="Investigator" value={s?.pi_name || '—'} />
        <StatCard label="Studies" value={results<StudySite>(participations.data).length} />
      </div>
      <Card title="Study participation">
        <DataTable loading={participations.loading} rows={results<StudySite>(participations.data)} empty="Not assigned to a study" columns={[{ key: 'study_code', label: 'Study' }, { key: 'status', label: 'Activation', render: (r) => <StatusBadge value={r.status} /> }, { key: 'enrollment_target', label: 'Target' }, { key: 'monitoring_status', label: 'Monitoring' }]} />
      </Card>
      <Card title="Feasibility">
        <DataTable loading={feasibility.loading} rows={results(feasibility.data)} empty="No assessments" columns={[{ key: 'status', label: 'Status' }, { key: 'score', label: 'Score' }, { key: 'completed_at', label: 'Completed' }]} />
      </Card>
      <Card title="Contracts">
        <DataTable loading={contracts.loading} rows={results(contracts.data)} empty="No contracts" columns={[{ key: 'title', label: 'Contract' }, { key: 'status', label: 'Status' }, { key: 'value', label: 'Value' }]} />
      </Card>
      <Card title="Performance">
        <DataTable loading={metrics.loading} rows={results(metrics.data)} empty="Metrics not refreshed yet" columns={[{ key: 'screened', label: 'Screened' }, { key: 'enrolled', label: 'Enrolled' }, { key: 'screen_failed', label: 'Failed' }, { key: 'open_findings', label: 'Findings' }]} />
      </Card>
    </div>
  )
}
