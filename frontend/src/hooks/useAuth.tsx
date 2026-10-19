import { createContext, createElement, useCallback, useContext, useEffect, useState, type ReactNode } from 'react'
import { authApi } from '../api/client'
import { configureHttp } from '../api/http'
import type { User } from '../api/types'
import { authStore } from '../store/authStore'

configureHttp({
  getAccessToken: () => authStore.accessToken,
  getOrgId: () => authStore.orgId,
  onUnauthorized: () => authStore.clearSession(),
})

interface AuthContextValue {
  user: User | null
  orgId: string | null
  isAuthenticated: boolean
  loading: boolean
  login: (email: string, password: string) => Promise<void>
  register: (payload: Record<string, string>) => Promise<void>
  logout: () => Promise<void>
  refreshMe: () => Promise<void>
  setOrgId: (id: string) => void
}

const AuthContext = createContext<AuthContextValue | null>(null)

export function AuthProvider({ children }: { children: ReactNode }) {
  const [, setTick] = useState(0)
  const [loading, setLoading] = useState(Boolean(authStore.accessToken))

  useEffect(() => authStore.subscribe(() => setTick((t) => t + 1)), [])

  const refreshMe = useCallback(async () => {
    if (!authStore.accessToken) {
      setLoading(false)
      return
    }
    try {
      authStore.setUser(await authApi.me())
    } catch {
      authStore.clearSession()
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => {
    void refreshMe()
  }, [refreshMe])

  const login = useCallback(async (email: string, password: string) => {
    const res = await authApi.login(email, password)
    authStore.setSession(res)
    authStore.setUser(await authApi.me())
  }, [])

  const register = useCallback(async (payload: Record<string, string>) => {
    const res = await authApi.register(payload)
    authStore.setSession(res)
    if (res.organization_id) authStore.setOrgId(res.organization_id)
    try {
      authStore.setUser(await authApi.me())
    } catch {
      /* first-load */
    }
  }, [])

  const logout = useCallback(async () => {
    try {
      await authApi.logout(authStore.refreshToken || undefined)
    } catch {
      /* ignore */
    }
    authStore.clearSession()
  }, [])

  return createElement(AuthContext.Provider, {
    value: {
      user: authStore.user,
      orgId: authStore.orgId,
      isAuthenticated: Boolean(authStore.user),
      loading,
      login,
      register,
      logout,
      refreshMe,
      setOrgId: (id) => authStore.setOrgId(id),
    },
  }, children)
}

export function useAuth() {
  const ctx = useContext(AuthContext)
  if (!ctx) throw new Error('useAuth must be used within AuthProvider')
  return ctx
}
