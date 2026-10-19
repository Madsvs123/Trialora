import { useState } from 'react'
import { useParams } from 'react-router-dom'
import { issuesApi } from '../../api/client'
import type { Issue } from '../../api/types'
import { Button, Card, Input, Modal, PageHeader, Select, Textarea } from '../../components/ui'
import { useApi, useMutation } from '../../hooks/useApi'
import { DataTable, results, StatusBadge } from '../_shared'

export function IssueListPage() {
  const list = useApi(() => issuesApi.list({ page_size: 50 }), [])
  const [open, setOpen] = useState(false)
  const [form, setForm] = useState({ title: '', kind: 'deviation', severity: 'medium', category: '', description: '' })
  const create = useMutation((body: typeof form) => issuesApi.create(body))

  return (
    <div className="tr-page">
      <PageHeader title="Issues & deviations" subtitle="Severity, category, root cause, CAPA, owners, due dates, and escalation." actions={<Button onClick={() => setOpen(true)}>Log issue</Button>} />
      <Card>
        <DataTable
          loading={list.loading}
          rows={results<Issue>(list.data)}
          empty="No issues"
          href={(row) => `/app/issues/${row.id}`}
          columns={[
            { key: 'title', label: 'Issue' },
            { key: 'kind', label: 'Type' },
            { key: 'severity', label: 'Severity', render: (r) => <StatusBadge value={r.severity} /> },
            { key: 'status', label: 'Status', render: (r) => <StatusBadge value={r.status} /> },
            { key: 'due_date', label: 'Due' },
          ]}
        />
      </Card>
      <Modal open={open} title="Log issue" onClose={() => setOpen(false)}>
        <form className="tr-form" onSubmit={async (e) => { e.preventDefault(); await create.mutate(form); setOpen(false); list.reload() }}>
          <Input label="Title" value={form.title} onChange={(e) => setForm({ ...form, title: e.target.value })} required />
          <div className="tr-form-row">
            <Select label="Type" value={form.kind} onChange={(e) => setForm({ ...form, kind: e.target.value })}>
              <option value="deviation">Protocol deviation</option>
              <option value="issue">Operational issue</option>
              <option value="query">Data query</option>
              <option value="safety">Safety</option>
            </Select>
            <Select label="Severity" value={form.severity} onChange={(e) => setForm({ ...form, severity: e.target.value })}>
              <option>low</option><option>medium</option><option>high</option><option>critical</option>
            </Select>
          </div>
          <Input label="Category" value={form.category} onChange={(e) => setForm({ ...form, category: e.target.value })} />
          <Textarea label="Description" value={form.description} onChange={(e) => setForm({ ...form, description: e.target.value })} />
          <Button type="submit">Save</Button>
        </form>
      </Modal>
    </div>
  )
}

export function IssueDetailPage() {
  const { id = '' } = useParams()
  const item = useApi(() => issuesApi.retrieve(id) as Promise<Issue & { root_cause?: string; resolution?: string }>, [id])
  const i = item.data
  return (
    <div className="tr-page">
      <PageHeader title={i?.title || 'Issue'} subtitle={`${i?.kind || ''} · ${i?.category || ''}`} />
      <Card title="Investigation">
        <p>Severity <StatusBadge value={i?.severity} /> · Status <StatusBadge value={i?.status} /></p>
        <p style={{ marginTop: 12 }}>{i?.root_cause || 'Root cause not recorded.'}</p>
        <p className="tr-muted" style={{ marginTop: 8 }}>{i?.resolution || 'No resolution yet.'}</p>
      </Card>
    </div>
  )
}
