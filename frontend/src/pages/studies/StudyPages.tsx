import { useState } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import { milestonesApi, protocolsApi, studiesApi, studySitesApi } from '../../api/client'
import type { Study, StudySite } from '../../api/types'
import { Button, Card, Input, Modal, PageHeader, Select, StatCard, Textarea } from '../../components/ui'
import { useApi, useMutation } from '../../hooks/useApi'
import { formatNumber } from '../../utils/format'
import { DataTable, results, StatusBadge } from '../_shared'

export function StudyListPage() {
  const navigate = useNavigate()
  const list = useApi(() => studiesApi.list({ page_size: 50 }), [])
  const [open, setOpen] = useState(false)
  const [form, setForm] = useState({ code: '', title: '', phase: 'II', therapeutic_area: '', indication: '', enrollment_target: '0' })
  const create = useMutation((body: typeof form) => studiesApi.create({ ...body, enrollment_target: Number(body.enrollment_target) }))

  return (
    <div className="tr-page">
      <PageHeader title="Studies" subtitle="Protocols, phases, indications, milestones, and participating countries." actions={<Button onClick={() => setOpen(true)}>New study</Button>} />
      <Card>
        <DataTable
          loading={list.loading}
          rows={results<Study>(list.data)}
          empty="No studies yet"
          href={(row) => `/app/studies/${row.id}`}
          columns={[
            { key: 'code', label: 'Code' },
            { key: 'title', label: 'Title' },
            { key: 'phase', label: 'Phase' },
            { key: 'status', label: 'Status', render: (r) => <StatusBadge value={r.status} /> },
            { key: 'therapeutic_area', label: 'Area' },
            { key: 'enrollment_target', label: 'Target', render: (r) => formatNumber(r.enrollment_target) },
          ]}
        />
      </Card>
      <Modal open={open} title="Create study" onClose={() => setOpen(false)}>
        <form className="tr-form" onSubmit={async (e) => { e.preventDefault(); const created = await create.mutate(form); if (created && 'id' in created) { setOpen(false); navigate(`/app/studies/${(created as Study).id}`) } }}>
          <div className="tr-form-row">
            <Input label="Code" value={form.code} onChange={(e) => setForm({ ...form, code: e.target.value })} required />
            <Select label="Phase" value={form.phase} onChange={(e) => setForm({ ...form, phase: e.target.value })}>
              {['I', 'I/II', 'II', 'II/III', 'III', 'IV', 'OBS'].map((p) => <option key={p}>{p}</option>)}
            </Select>
          </div>
          <Input label="Title" value={form.title} onChange={(e) => setForm({ ...form, title: e.target.value })} required />
          <div className="tr-form-row">
            <Input label="Therapeutic area" value={form.therapeutic_area} onChange={(e) => setForm({ ...form, therapeutic_area: e.target.value })} />
            <Input label="Indication" value={form.indication} onChange={(e) => setForm({ ...form, indication: e.target.value })} />
          </div>
          <Input label="Enrollment target" type="number" value={form.enrollment_target} onChange={(e) => setForm({ ...form, enrollment_target: e.target.value })} />
          <Button type="submit" loading={create.loading}>Create</Button>
        </form>
      </Modal>
    </div>
  )
}

export function StudyDetailPage() {
  const { id = '' } = useParams()
  const study = useApi(() => studiesApi.retrieve(id) as Promise<Study>, [id])
  const sites = useApi(() => studySitesApi.list({ study: id }), [id])
  const milestones = useApi(() => milestonesApi.list({ study: id }), [id])
  const protocols = useApi(() => protocolsApi.list({ study: id }), [id])
  const s = study.data

  return (
    <div className="tr-page">
      <PageHeader title={s?.title || 'Study'} subtitle={`${s?.code || ''} · ${s?.indication || ''}`} />
      <div className="tr-grid-stats">
        <StatCard label="Status" value={<StatusBadge value={s?.status} />} />
        <StatCard label="Phase" value={s?.phase || '—'} />
        <StatCard label="Target" value={formatNumber(s?.enrollment_target)} />
        <StatCard label="NCT" value={s?.nct_id || '—'} />
      </div>
      <Card title="Protocol summary">
        <p>{s?.description || 'No protocol narrative yet.'}</p>
        <DataTable loading={protocols.loading} rows={results(protocols.data)} empty="No protocol versions" columns={[{ key: 'version', label: 'Version' }, { key: 'title', label: 'Title' }, { key: 'is_current', label: 'Current', render: (r) => (r as { is_current?: boolean }).is_current ? 'Yes' : 'No' }]} />
      </Card>
      <Card title="Milestones">
        <DataTable loading={milestones.loading} rows={results(milestones.data)} empty="No milestones" columns={[{ key: 'name', label: 'Milestone' }, { key: 'status', label: 'Status', render: (r) => <StatusBadge value={String((r as { status: string }).status)} /> }, { key: 'due_date', label: 'Due' }]} />
      </Card>
      <Card title="Participating sites">
        <DataTable loading={sites.loading} rows={results<StudySite>(sites.data)} empty="No sites assigned" href={(r) => `/app/sites/${r.site}`} columns={[{ key: 'site_name', label: 'Site' }, { key: 'status', label: 'Status', render: (r) => <StatusBadge value={r.status} /> }, { key: 'enrollment_target', label: 'Target' }]} />
      </Card>
    </div>
  )
}
