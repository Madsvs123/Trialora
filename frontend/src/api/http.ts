const API_BASE = import.meta.env.VITE_API_BASE_URL || '/api/v1'

type TokenGetter = () => string | null
type OrgGetter = () => string | null

let getAccessToken: TokenGetter = () => localStorage.getItem('tr_access')
let getOrgId: OrgGetter = () => localStorage.getItem('tr_org_id')
let onUnauthorized = () => {
  localStorage.removeItem('tr_access')
  localStorage.removeItem('tr_refresh')
}

export function configureHttp(opts: {
  getAccessToken?: TokenGetter
  getOrgId?: OrgGetter
  onUnauthorized?: () => void
}) {
  if (opts.getAccessToken) getAccessToken = opts.getAccessToken
  if (opts.getOrgId) getOrgId = opts.getOrgId
  if (opts.onUnauthorized) onUnauthorized = opts.onUnauthorized
}

export class ApiError extends Error {
  status: number
  body: unknown
  constructor(status: number, body: unknown, message?: string) {
    super(message || extractError(body, status))
    this.status = status
    this.body = body
  }
}

function extractError(body: unknown, status: number) {
  if (body && typeof body === 'object') {
    const rec = body as Record<string, unknown>
    if (typeof rec.detail === 'string') return rec.detail
    if (typeof rec.message === 'string') return rec.message
  }
  return `Request failed (${status})`
}

function buildQuery(params?: Record<string, string | number | boolean | undefined | null>) {
  if (!params) return ''
  const qs = new URLSearchParams()
  Object.entries(params).forEach(([k, v]) => {
    if (v !== undefined && v !== null && v !== '') qs.set(k, String(v))
  })
  const s = qs.toString()
  return s ? `?${s}` : ''
}

export async function http<T>(
  path: string,
  options: RequestInit & {
    params?: Record<string, string | number | boolean | undefined | null>
    skipAuth?: boolean
    skipOrg?: boolean
  } = {},
): Promise<T> {
  const { params, skipAuth, skipOrg, headers: custom, ...rest } = options
  const headers = new Headers(custom || {})
  if (!headers.has('Content-Type') && rest.body && !(rest.body instanceof FormData)) {
    headers.set('Content-Type', 'application/json')
  }
  if (!skipAuth) {
    const token = getAccessToken()
    if (token) headers.set('Authorization', `Bearer ${token}`)
  }
  if (!skipOrg) {
    const orgId = getOrgId()
    if (orgId) headers.set('X-Organization-Id', orgId)
  }
  const res = await fetch(`${API_BASE}${path}${buildQuery(params)}`, { ...rest, headers })
  if (res.status === 204) return undefined as T
  const text = await res.text()
  let data: unknown = null
  if (text) {
    try {
      data = JSON.parse(text)
    } catch {
      data = { detail: text }
    }
  }
  if (!res.ok) {
    if (res.status === 401) onUnauthorized()
    throw new ApiError(res.status, data)
  }
  return data as T
}

export const get = <T>(path: string, params?: Record<string, string | number | boolean | undefined | null>) =>
  http<T>(path, { method: 'GET', params })
export const post = <T>(path: string, body?: unknown, opts?: { skipAuth?: boolean; skipOrg?: boolean }) =>
  http<T>(path, { method: 'POST', body: body instanceof FormData ? body : JSON.stringify(body ?? {}), ...opts })
export const patch = <T>(path: string, body?: unknown) =>
  http<T>(path, { method: 'PATCH', body: JSON.stringify(body ?? {}) })
export const del = <T = void>(path: string) => http<T>(path, { method: 'DELETE' })
