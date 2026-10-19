import { del, get, http, patch, post } from './http'
import type { AuthResponse, Paginated, User } from './types'

export const authApi = {
  login: (email: string, password: string) => post<AuthResponse>('/auth/login/', { email, password }, { skipAuth: true, skipOrg: true }),
  register: (payload: Record<string, string>) => post<AuthResponse>('/auth/register/', payload, { skipAuth: true, skipOrg: true }),
  me: () => get<User>('/auth/me/'),
  logout: (refresh?: string) => post('/auth/logout/', { refresh }),
  forgot: (email: string) => post('/auth/forgot-password/', { email }, { skipAuth: true, skipOrg: true }),
  reset: (token: string, password: string) => post('/auth/reset-password/', { token, password }, { skipAuth: true, skipOrg: true }),
  acceptInvite: (payload: Record<string, string>) => post<AuthResponse>('/auth/accept-invite/', payload, { skipAuth: true, skipOrg: true }),
}

export function resource<T = Record<string, unknown>>(path: string) {
  return {
    list: (params?: Record<string, string | number | boolean | undefined | null>) => get<Paginated<T>>(`/${path}/`, params),
    retrieve: (id: string) => get<T>(`/${path}/${id}/`),
    create: (body: unknown) => post<T>(`/${path}/`, body),
    update: (id: string, body: unknown) => patch<T>(`/${path}/${id}/`, body),
    remove: (id: string) => del(`/${path}/${id}/`),
    summary: () => get<Record<string, unknown>>(`/${path}/summary/`),
    action: <R>(id: string, name: string, body?: unknown) => post<R>(`/${path}/${id}/${name}/`, body),
  }
}

export const studiesApi = resource('studies')
export const sitesApi = resource('sites')
export const studySitesApi = resource('study-sites')
export const participantsApi = resource('participants')
export const visitsApi = resource('visits')
export const issuesApi = resource('issues')
export const documentsApi = resource('documents')
export const tasksApi = resource('tasks')
export const paymentsApi = resource('payments')
export const monitoringApi = resource('monitoring-visits')
export const findingsApi = resource('findings')
export const staffApi = resource('investigators')
export const membersApi = resource('members')
export const notificationsApi = {
  ...resource('notifications'),
  read: (id: string) => post(`/notifications/${id}/read/`),
  readAll: () => post('/notifications/read_all/'),
}
export const reportsApi = {
  dashboard: () => get<Record<string, unknown>>('/dashboards/overview/'),
  enrollment: (study?: string) => get<Record<string, unknown>>('/reports/enrollment/', { study }),
  operations: () => get<Record<string, unknown>>('/reports/operations/'),
}
export const searchApi = {
  query: (q: string) => get<{ results: Array<{ type: string; id: string; title: string; subtitle: string }> }>('/search/', { q }),
}

export const settingsApi = {
  current: () => get('/settings/current/'),
  update: (body: unknown) => http('/settings/current/', { method: 'PATCH', body: JSON.stringify(body) }),
}

export const orgsApi = resource('organizations')
export const sponsorsApi = resource('sponsors')
export const departmentsApi = resource('departments')
export const milestonesApi = resource('milestones')
export const protocolsApi = resource('protocols')
export const credentialsApi = resource('credentials')
export const trainingsApi = resource('trainings')
export const budgetsApi = resource('budgets')
export const invoicesApi = resource('invoices')
export const expensesApi = resource('expenses')
export const grantsApi = resource('grants')
export const auditApi = resource('audit-logs')
export const rolesApi = resource('roles')
export const invitationsApi = resource('invitations')
export const templatesApi = resource('templates')
export const customFieldsApi = resource('custom-fields')
export const workflowsApi = resource('workflows')
export const feasibilityApi = resource('feasibility')
export const contractsApi = resource('site-contracts')
export const visitDefsApi = resource('visit-definitions')
export const actionItemsApi = resource('action-items')
export const deviationsApi = resource('deviations')
export const siteMetricsApi = resource('site-metrics')
export const riskApi = resource('risk-indicators')
export const studyAccessApi = resource('study-access')
export const adverseEventsApi = resource('adverse-events')
export const saesApi = resource('saes')
export const safetyReportsApi = resource('safety-reports')
export const safetySignalsApi = resource('safety-signals')
export const committeesApi = resource('ethics-committees')
export const submissionsApi = resource('submissions')
export const approvalsApi = resource('approvals')
export const obligationsApi = resource('regulatory-obligations')
export const productsApi = resource('products')
export const kitsApi = resource('kits')
export const shipmentsApi = resource('shipments')
export const accountabilityApi = resource('accountability')
export const excursionsApi = resource('excursions')
