export interface Paginated<T> {
  count: number
  next: string | null
  previous: string | null
  results: T[]
}

export interface OrgRef {
  id: string
  name: string
  org_type: string
  role: string
  permissions: string[]
}

export interface User {
  id: string
  email: string
  display_name: string
  first_name: string
  last_name: string
  title?: string
  avatar_color?: string
  is_investigator?: boolean
  last_organization?: string
  organizations?: OrgRef[]
  permissions?: string[]
  role?: string
}

export interface AuthResponse {
  access: string
  refresh: string
  user: User
  organizations?: OrgRef[]
  organization_id?: string
}

export interface Study {
  id: string
  code: string
  title: string
  phase: string
  status: string
  therapeutic_area: string
  indication: string
  enrollment_target: number
  screening_target: number
  sponsor_name?: string
  start_date?: string
  nct_id?: string
  description?: string
}

export interface Site {
  id: string
  name: string
  institution: string
  city: string
  country_name?: string
  pi_name?: string
  email?: string
}

export interface StudySite {
  id: string
  study: string
  site: string
  site_name?: string
  study_code?: string
  status: string
  enrollment_target: number
  monitoring_status: string
}

export interface Participant {
  id: string
  subject_id: string
  screening_number: string
  status: string
  eligibility_status: string
  study: string
  study_code?: string
  site_name?: string
  pii_masked?: boolean
  first_name?: string
  last_name?: string
  enrolled_on?: string
}

export interface Visit {
  id: string
  name: string
  status: string
  scheduled_date: string
  actual_date?: string
  subject_id?: string
  window_end?: string
}

export interface Issue {
  id: string
  title: string
  kind: string
  severity: string
  status: string
  category?: string
  due_date?: string
}

export interface NotificationItem {
  id: string
  kind: string
  title: string
  body: string
  link: string
  is_read: boolean
  created_at: string
}

export type Dict = Record<string, unknown>
