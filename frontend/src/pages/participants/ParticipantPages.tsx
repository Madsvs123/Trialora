import { useState } from 'react'
import { useParams } from 'react-router-dom'
import { participantsApi, visitsApi } from '../../api/client'
import type { Participant, Visit } from '../../api/types'
import { Button, Card, Input, Modal, PageHeader, Select, StatCard } from '../../components/ui'
import { useApi, useMutation } from '../../hooks/useApi'
import { DataTable, results, StatusBadge } from '../_shared'

export function ParticipantListPage() {
  const [status, setStatus] = useState('')
  const list = useApi(() => participantsApi.list({ page_size: 50, status: status || undefined }), [status])
  const [open, setOpen] = useState(false)
  const [form, setForm] = useState({ subject_id: '', screening_number: '', status: 'prescreen' })
  const create = useMutation((body: typeof form) => participantsApi.create(body))

  return (
    <div className="tr-page">
      <PageHeader title="Participants" subtitle="Screening, eligibility, enrollment, randomization metadata, and controlled PII access." actions={<Button onClick={() => setOpen(true)}>Register subject</Button>} />
      <Select label="Status" value={status} onChange={(e) => setStatus(e.target.value)}>
        <option value="">All statuses</option>
        {['prescreen', 'screening', 'screen_failed', 'enrolled', 'randomized', 'active', 'withdrawn', 'completed'].map((s) => <option key={s} value={s}>{s}</option>)}
      </Select>
      <Card>
        <DataTable
          loading={list.loading}
          rows={results<Participant>(list.data)}
          empty="No participants"
          href={(row) => `/app/participants/${row.id}`}
          columns={[
            { key: 'subject_id', label: 'Subject' },
            { key: 'study_code', label: 'Study' },
            { key: 'site_name', label: 'Site' },
            { key: 'status', label: 'Status', render: (r) => <StatusBadge value={r.status} /> },
            { key: 'eligibility_status', label: 'Eligibility', render: (r) => <StatusBadge value={r.eligibility_status} /> },
            { key: 'first_name', label: 'PII', render: (r) => r.pii_masked ? 'Restricted' : `${r.first_name || ''} ${r.last_name || ''}` },
          ]}
        />
      </Card>
      <Modal open={open} title="Register participant" onClose={() => setOpen(false)}>
        <form className="tr-form" onSubmit={async (e) => { e.preventDefault(); await create.mutate(form); setOpen(false); list.reload() }}>
          <Input label="Subject ID" value={form.subject_id} onChange={(e) => setForm({ ...form, subject_id: e.target.value })} required />
          <Input label="Screening number" value={form.screening_number} onChange={(e) => setForm({ ...form, screening_number: e.target.value })} />
          <Button type="submit">Create</Button>
        </form>
      </Modal>
    </div>
  )
}

export function ParticipantDetailPage() {
  const { id = '' } = useParams()
  const item = useApi(() => participantsApi.retrieve(id) as Promise<Participant>, [id])
  const visits = useApi(() => visitsApi.list({ participant: id }), [id])
  const p = item.data

  return (
    <div className="tr-page">
      <PageHeader title={p?.subject_id || 'Participant'} subtitle={p?.pii_masked ? 'Personally identifiable fields are masked for your role.' : `${p?.first_name || ''} ${p?.last_name || ''}`} />
      <div className="tr-grid-stats">
        <StatCard label="Status" value={<StatusBadge value={p?.status} />} />
        <StatCard label="Eligibility" value={<StatusBadge value={p?.eligibility_status} />} />
        <StatCard label="Site" value={p?.site_name || '—'} />
        <StatCard label="Enrolled" value={p?.enrolled_on || '—'} />
      </div>
      <Card title="Visit schedule">
        <DataTable loading={visits.loading} rows={results<Visit>(visits.data)} empty="No visits scheduled" href={(r) => `/app/visits/${r.id}`} columns={[{ key: 'name', label: 'Visit' }, { key: 'scheduled_date', label: 'Window' }, { key: 'status', label: 'Status', render: (r) => <StatusBadge value={r.status} /> }]} />
      </Card>
    </div>
  )
}
