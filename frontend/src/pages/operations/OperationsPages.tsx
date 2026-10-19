import { useState } from 'react'
import { auditApi, budgetsApi, credentialsApi, customFieldsApi, documentsApi, expensesApi, grantsApi, invitationsApi, invoicesApi, membersApi, notificationsApi, paymentsApi, reportsApi, rolesApi, searchApi, settingsApi, tasksApi, templatesApi, trainingsApi, workflowsApi } from '../../api/client'
import type { NotificationItem } from '../../api/types'
import { Button, Card, Input, PageHeader, StatCard, Tabs } from '../../components/ui'
import { useApi } from '../../hooks/useApi'
import { formatCurrency, formatNumber, formatRelative } from '../../utils/format'
import { DataTable, results, StatusBadge } from '../_shared'

export function DocumentsPage() {
  const list = useApi(() => documentsApi.list({ page_size: 50 }), [])
  return (
    <div className="tr-page">
      <PageHeader title="Documents" subtitle="Protocols, investigator files, consents, approvals, contracts, training records, and correspondence." />
      <Card>
        <DataTable loading={list.loading} rows={results(list.data)} empty="No documents" columns={[{ key: 'title', label: 'Document' }, { key: 'category', label: 'Category' }, { key: 'status', label: 'Status', render: (r) => <StatusBadge value={String((r as { status: string }).status)} /> }, { key: 'current_version', label: 'Version' }, { key: 'expires_at', label: 'Expires' }]} />
      </Card>
    </div>
  )
}

export function StaffPage() {
  const members = useApi(() => membersApi.list({ page_size: 50 }), [])
  const credentials = useApi(() => credentialsApi.list({ page_size: 50 }), [])
  const trainings = useApi(() => trainingsApi.list({ page_size: 50 }), [])
  return (
    <div className="tr-page">
      <PageHeader title="Investigators & staff" subtitle="Licenses, certifications, CVs, training completion, and expiration reminders." />
      <Card title="Team">
        <DataTable loading={members.loading} rows={results(members.data)} empty="No staff" columns={[{ key: 'user_name', label: 'Name' }, { key: 'user_email', label: 'Email' }, { key: 'role_name', label: 'Role' }, { key: 'title', label: 'Title' }]} />
      </Card>
      <Card title="Credentials">
        <DataTable loading={credentials.loading} rows={results(credentials.data)} empty="No credentials" columns={[{ key: 'user_name', label: 'Staff' }, { key: 'name', label: 'Credential' }, { key: 'kind', label: 'Type' }, { key: 'expires_on', label: 'Expires' }, { key: 'status', label: 'Status' }]} />
      </Card>
      <Card title="Training">
        <DataTable loading={trainings.loading} rows={results(trainings.data)} empty="No training assignments" columns={[{ key: 'user_name', label: 'Staff' }, { key: 'course', label: 'Course' }, { key: 'due_date', label: 'Due' }, { key: 'status', label: 'Status' }]} />
      </Card>
    </div>
  )
}

export function TasksPage() {
  const list = useApi(() => tasksApi.list({ page_size: 50 }), [])
  return (
    <div className="tr-page">
      <PageHeader title="Study tasks" subtitle="Assignments, priorities, milestones, dependencies, comments, and recurring work." />
      <Card>
        <DataTable loading={list.loading} rows={results(list.data)} empty="No tasks" columns={[{ key: 'title', label: 'Task' }, { key: 'priority', label: 'Priority', render: (r) => <StatusBadge value={String((r as { priority: string }).priority)} /> }, { key: 'status', label: 'Status' }, { key: 'assignee_name', label: 'Owner' }, { key: 'due_date', label: 'Due' }]} />
      </Card>
    </div>
  )
}

export function PaymentsPage() {
  const payments = useApi(() => paymentsApi.list({ page_size: 50 }), [])
  const budgets = useApi(() => budgetsApi.list({ page_size: 20 }), [])
  const invoices = useApi(() => invoicesApi.list({ page_size: 20 }), [])
  const expenses = useApi(() => expensesApi.list({ page_size: 20 }), [])
  const grants = useApi(() => grantsApi.list({ page_size: 20 }), [])
  return (
    <div className="tr-page">
      <PageHeader title="Financial tracking" subtitle="Study budgets, site and investigator payments, invoices, expenses, and grants." />
      <Card title="Budgets">
        <DataTable loading={budgets.loading} rows={results(budgets.data)} empty="No budget lines" columns={[{ key: 'category', label: 'Category' }, { key: 'planned', label: 'Planned', render: (r) => formatCurrency((r as { planned: number }).planned) }, { key: 'actual', label: 'Actual', render: (r) => formatCurrency((r as { actual: number }).actual) }]} />
      </Card>
      <Card title="Payments">
        <DataTable loading={payments.loading} rows={results(payments.data)} empty="No payments" columns={[{ key: 'title', label: 'Payment' }, { key: 'kind', label: 'Type' }, { key: 'amount', label: 'Amount', render: (r) => formatCurrency((r as { amount: number }).amount) }, { key: 'status', label: 'Status', render: (r) => <StatusBadge value={String((r as { status: string }).status)} /> }]} />
      </Card>
      <Card title="Invoices & expenses">
        <DataTable loading={invoices.loading} rows={results(invoices.data)} empty="No invoices" columns={[{ key: 'number', label: 'Invoice' }, { key: 'amount', label: 'Amount' }, { key: 'status', label: 'Status' }]} />
        <div style={{ height: 12 }} />
        <DataTable loading={expenses.loading} rows={results(expenses.data)} empty="No expenses" columns={[{ key: 'category', label: 'Expense' }, { key: 'vendor', label: 'Vendor' }, { key: 'amount', label: 'Amount' }]} />
      </Card>
      <Card title="Grants">
        <DataTable loading={grants.loading} rows={results(grants.data)} empty="No grants" columns={[{ key: 'source', label: 'Source' }, { key: 'amount', label: 'Amount' }, { key: 'status', label: 'Status' }]} />
      </Card>
    </div>
  )
}

export function AnalyticsPage() {
  const dash = useApi(() => reportsApi.dashboard(), [])
  const ops = useApi(() => reportsApi.operations(), [])
  const d = dash.data as Record<string, Record<string, number>> | null
  const o = ops.data as { document_completeness?: { total: number; current: number }; payments?: Array<{ status: string; amount: number }> } | null
  return (
    <div className="tr-page">
      <PageHeader title="Analytics" subtitle="Enrollment, site performance, monitoring activity, deviations, milestones, and operational risk." />
      <div className="tr-grid-stats">
        <StatCard label="Enrolled" value={formatNumber(d?.enrollment?.enrolled)} hint={`${formatNumber(d?.enrollment?.target)} target`} />
        <StatCard label="Open findings" value={formatNumber(d?.risks?.open_findings)} />
        <StatCard label="Critical issues" value={formatNumber(d?.risks?.critical_issues)} />
        <StatCard label="Overdue visits" value={formatNumber(d?.visits?.overdue)} />
        <StatCard label="Documents current" value={`${o?.document_completeness?.current || 0}/${o?.document_completeness?.total || 0}`} />
      </div>
    </div>
  )
}

export function ReportsPage() {
  const enrollment = useApi(() => reportsApi.enrollment(), [])
  const ops = useApi(() => reportsApi.operations(), [])
  const data = enrollment.data as { by_site?: Array<Record<string, unknown>> } | null
  return (
    <div className="tr-page">
      <PageHeader title="Reports" subtitle="Exportable enrollment, site, monitoring, milestone, budget, and completeness views." />
      <Card title="Enrollment report" actions={<Button variant="outline" onClick={() => window.open('/api/v1/reports/enrollment/?export=csv', '_blank')}>Export CSV</Button>}>
        <DataTable
          loading={enrollment.loading}
          rows={(data?.by_site || []).map((r, i) => ({ id: String(i), ...r }))}
          empty="No enrollment rows"
          columns={[
            { key: 'study__code', label: 'Study' },
            { key: 'study_site__site__name', label: 'Site' },
            { key: 'screened', label: 'Screened' },
            { key: 'enrolled', label: 'Enrolled' },
            { key: 'failed', label: 'Failed' },
            { key: 'completed', label: 'Completed' },
          ]}
        />
      </Card>
      <Card title="Operations report">
        <DataTable
          loading={ops.loading}
          rows={[{ id: 'ops', ...(ops.data as Record<string, unknown> || {}) }]}
          empty="No operational snapshot"
          columns={[
            { key: 'document_completeness', label: 'Documents', render: (r) => JSON.stringify((r as { document_completeness?: unknown }).document_completeness || {}) },
          ]}
        />
      </Card>
    </div>
  )
}

export function SearchPage() {
  const [q, setQ] = useState('')
  const result = useApi(() => searchApi.query(q), [q], { enabled: q.length > 1 })
  return (
    <div className="tr-page">
      <PageHeader title="Global search" subtitle="Find studies, sites, participants, issues, and documents." />
      <Input label="Search" value={q} onChange={(e) => setQ(e.target.value)} placeholder="LUM-ONC, Harborview, 204-001…" />
      <Card>
        <DataTable loading={result.loading} rows={(result.data?.results || []).map((r) => ({ id: r.id, ...r }))} empty="No matches" columns={[{ key: 'title', label: 'Result' }, { key: 'type', label: 'Type' }, { key: 'subtitle', label: 'Detail' }]} />
      </Card>
    </div>
  )
}

export function NotificationsPage() {
  const list = useApi(() => notificationsApi.list({ page_size: 40 }), [])
  return (
    <div className="tr-page">
      <PageHeader title="Notifications" subtitle="Overdue visits, expiring documents, findings, enrollment, training, and study events." actions={<Button variant="outline" onClick={() => notificationsApi.readAll().then(list.reload)}>Mark all read</Button>} />
      <Card>
        <DataTable loading={list.loading} rows={results<NotificationItem>(list.data)} empty="Inbox is clear" columns={[{ key: 'title', label: 'Alert' }, { key: 'kind', label: 'Type' }, { key: 'created_at', label: 'When', render: (r) => formatRelative(r.created_at) }, { key: 'is_read', label: 'State', render: (r) => r.is_read ? 'Read' : 'New' }]} />
      </Card>
    </div>
  )
}

export function AdminPage() {
  const [tab, setTab] = useState('Organization')
  const settings = useApi(() => settingsApi.current() as Promise<Record<string, unknown>>, [])
  const audit = useApi(() => auditApi.list({ page_size: 30 }), [])
  const members = useApi(() => membersApi.list({ page_size: 30 }), [])
  const roles = useApi(() => rolesApi.list({ page_size: 30 }), [])
  const invitations = useApi(() => invitationsApi.list({ page_size: 20 }), [])
  const templates = useApi(() => templatesApi.list({ page_size: 20 }), [])
  const fields = useApi(() => customFieldsApi.list({ page_size: 20 }), [])
  const workflows = useApi(() => workflowsApi.list({ page_size: 20 }), [])
  return (
    <div className="tr-page">
      <PageHeader title="Administration" subtitle="Roles, invitations, templates, custom fields, workflows, and organization settings." />
      <Tabs tabs={['Organization', 'People', 'Templates', 'Audit']} value={tab} onChange={setTab} />
      {tab === 'Organization' && (
        <Card title="Workspace settings">
          <div style={{ display: 'grid', gap: 8 }}>
            {Object.entries(settings.data || {}).filter(([k]) => !['id', 'created_at', 'updated_at'].includes(k)).map(([key, value]) => (
              <div key={key} style={{ display: 'flex', justifyContent: 'space-between', gap: 12 }}>
                <span className="tr-muted">{key.replace(/_/g, ' ')}</span>
                <strong>{typeof value === 'object' ? JSON.stringify(value) : String(value)}</strong>
              </div>
            ))}
          </div>
        </Card>
      )}
      {tab === 'People' && (
        <>
          <Card title="Roles">
            <DataTable loading={roles.loading} rows={results(roles.data)} empty="No roles" columns={[{ key: 'name', label: 'Role' }, { key: 'slug', label: 'Slug' }, { key: 'is_system', label: 'System' }]} />
          </Card>
          <Card title="Memberships">
            <DataTable loading={members.loading} rows={results(members.data)} empty="No members" columns={[{ key: 'user_name', label: 'Name' }, { key: 'role_name', label: 'Role' }, { key: 'title', label: 'Title' }]} />
          </Card>
          <Card title="Invitations">
            <DataTable loading={invitations.loading} rows={results(invitations.data)} empty="No open invitations" columns={[{ key: 'email', label: 'Email' }, { key: 'role_name', label: 'Role' }, { key: 'is_open', label: 'Open' }]} />
          </Card>
        </>
      )}
      {tab === 'Templates' && (
        <>
          <Card title="Study templates">
            <DataTable loading={templates.loading} rows={results(templates.data)} empty="No templates" columns={[{ key: 'name', label: 'Template' }, { key: 'phase', label: 'Phase' }, { key: 'therapeutic_area', label: 'Area' }]} />
          </Card>
          <Card title="Custom fields">
            <DataTable loading={fields.loading} rows={results(fields.data)} empty="No custom fields" columns={[{ key: 'name', label: 'Field' }, { key: 'entity_type', label: 'Entity' }, { key: 'field_type', label: 'Type' }]} />
          </Card>
          <Card title="Status workflows">
            <DataTable loading={workflows.loading} rows={results(workflows.data)} empty="No workflows" columns={[{ key: 'name', label: 'Workflow' }, { key: 'entity_type', label: 'Entity' }]} />
          </Card>
        </>
      )}
      {tab === 'Audit' && (
        <Card title="Audit log">
          <DataTable loading={audit.loading} rows={results(audit.data)} empty="No audit events" columns={[{ key: 'created_at', label: 'When' }, { key: 'actor_name', label: 'Actor' }, { key: 'action', label: 'Action' }, { key: 'message', label: 'Message' }]} />
        </Card>
      )}
    </div>
  )
}
