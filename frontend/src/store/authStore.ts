import type { OrgRef, User } from '../api/types'

type Listener = () => void

class AuthStore {
  accessToken = localStorage.getItem('tr_access')
  refreshToken = localStorage.getItem('tr_refresh')
  orgId = localStorage.getItem('tr_org_id')
  user: User | null = null
  private listeners = new Set<Listener>()

  subscribe(fn: Listener) {
    this.listeners.add(fn)
    return () => this.listeners.delete(fn)
  }

  private emit() {
    this.listeners.forEach((fn) => fn())
  }

  setSession(payload: { access: string; refresh: string; user: User; organizations?: OrgRef[] }) {
    this.accessToken = payload.access
    this.refreshToken = payload.refresh
    this.user = payload.user
    localStorage.setItem('tr_access', payload.access)
    localStorage.setItem('tr_refresh', payload.refresh)
    const org = payload.user.last_organization || payload.organizations?.[0]?.id || payload.user.organizations?.[0]?.id
    if (org) this.setOrgId(org)
    this.emit()
  }

  setUser(user: User) {
    this.user = user
    if (user.last_organization) this.setOrgId(user.last_organization)
    this.emit()
  }

  setOrgId(id: string) {
    this.orgId = id
    localStorage.setItem('tr_org_id', id)
    this.emit()
  }

  clearSession() {
    this.accessToken = null
    this.refreshToken = null
    this.user = null
    localStorage.removeItem('tr_access')
    localStorage.removeItem('tr_refresh')
    this.emit()
  }

  get isStaff() {
    return !this.user?.is_investigator || Boolean(this.user?.permissions?.includes('studies.read'))
  }
}

export const authStore = new AuthStore()
