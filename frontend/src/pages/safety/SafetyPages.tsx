import { useState } from 'react'
import { useParams } from 'react-router-dom'
import { resource } from '../../api/client'
import { Button, Card, Input, Modal, PageHeader, Select, StatCard } from '../../components/ui'
import { useApi, useMutation } from '../../hooks/useApi'
import { DataTable, results, StatusBadge } from '../_shared'

const aesApi = resource('adverse-events')
const saeApi = resource('saes')
const signalsApi = resource('safety-signals')

export function SafetyListPage() {
  const aes = useApi(() => aesApi.list({ page_size: 50 }), [])
  const saes = useApi(() => saeApi.list({ page_size: 20 }), [])
  const signals = useApi(() => signalsApi.list({ page_size: 20 }), [])
  const rows = results(aes.data)
  const [open, setOpen] = useState(false)
  const [form, setForm] = useState({ ae_number: '', term: '', seriousness: 'non_serious', severity: 'mild', causality: 'possible', onset_date: '' })
  const create = useMutation((body: typeof form) => aesApi.create(body))

  return (
    <div className="tr-page">
      <PageHeader title="Safety" subtitle="Adverse events, SAEs, SUSARs, reporting clocks, and emerging signals." actions={<Button onClick={() => setOpen(true)}>Log AE</Button>} />
      <div className="tr-grid-stats">
        <StatCard label="AEs" value={rows.length} />
        <StatCard label="Serious" value={rows.filter((r) => (r as { seriousness: string }).seriousness === 'serious').length} />
        <StatCard label="Open" value={rows.filter((r) => (r as { status: string }).status === 'open').length} />
        <StatCard label="Signals" value={results(signals.data).length} />
      </div>
      <Card title="Adverse events">
        <DataTable
          loading={aes.loading}
          rows={rows}
          empty="No adverse events"
          href={(r) => `/app/safety/${r.id}`}
          columns={[
            { key: 'ae_number', label: 'ID' },
            { key: 'term', label: 'Term' },
            { key: 'subject_id', label: 'Subject' },
            { key: 'seriousness', label: 'Seriousness', render: (r) => <StatusBadge value={String((r as { seriousness: string }).seriousness)} /> },
            { key: 'severity', label: 'Severity' },
            { key: 'causality', label: 'Causality' },
            { key: 'status', label: 'Status', render: (r) => <StatusBadge value={String((r as { status: string }).status)} /> },
          ]}
        />
      </Card>
      <Card title="SAE records">
        <DataTable loading={saes.loading} rows={results(saes.data)} empty="No SAEs" columns={[{ key: 'days_to_report', label: 'Clock (days)' }, { key: 'is_susar', label: 'SUSAR' }, { key: 'reported_to_sponsor_on', label: 'Sponsor' }, { key: 'reported_to_irb_on', label: 'IRB' }]} />
      </Card>
      <Card title="Signals">
        <DataTable loading={signals.loading} rows={results(signals.data)} empty="No signals" columns={[{ key: 'name', label: 'Signal' }, { key: 'events_count', label: 'Events' }, { key: 'status', label: 'Status' }]} />
      </Card>
      <Modal open={open} title="Log adverse event" onClose={() => setOpen(false)}>
        <form className="tr-form" onSubmit={async (e) => { e.preventDefault(); await create.mutate(form); setOpen(false); aes.reload() }}>
          <div className="tr-form-row">
            <Input label="AE number" value={form.ae_number} onChange={(e) => setForm({ ...form, ae_number: e.target.value })} required />
            <Input label="Onset" type="date" value={form.onset_date} onChange={(e) => setForm({ ...form, onset_date: e.target.value })} required />
          </div>
          <Input label="Term" value={form.term} onChange={(e) => setForm({ ...form, term: e.target.value })} required />
          <div className="tr-form-row">
            <Select label="Seriousness" value={form.seriousness} onChange={(e) => setForm({ ...form, seriousness: e.target.value })}>
              <option value="non_serious">Non-serious</option>
              <option value="serious">Serious</option>
            </Select>
            <Select label="Severity" value={form.severity} onChange={(e) => setForm({ ...form, severity: e.target.value })}>
              <option>mild</option><option>moderate</option><option>severe</option>
            </Select>
          </div>
          <Button type="submit">Save</Button>
        </form>
      </Modal>
    </div>
  )
}

export function SafetyDetailPage() {
  const { id = '' } = useParams()
  const item = useApi(() => aesApi.retrieve(id) as Promise<Record<string, string>>, [id])
  const a = item.data
  return (
    <div className="tr-page">
      <PageHeader title={a?.term || 'Adverse event'} subtitle={`${a?.ae_number || ''} · Subject ${a?.subject_id || ''}`} />
      <Card title="Assessment">
        <p>Seriousness <StatusBadge value={a?.seriousness} /> · Severity <StatusBadge value={a?.severity} /> · Causality <StatusBadge value={a?.causality} /></p>
        <p style={{ marginTop: 12 }}>{a?.narrative || 'No narrative recorded.'}</p>
      </Card>
    </div>
  )
}
