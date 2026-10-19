import { useCallback, useEffect, useRef, useState } from 'react'
import { ApiError } from '../api/http'

export function useApi<T>(fetcher: () => Promise<T>, deps: unknown[] = [], options?: { enabled?: boolean }) {
  const [data, setData] = useState<T | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [loading, setLoading] = useState(true)
  const [nonce, setNonce] = useState(0)
  const enabled = options?.enabled !== false
  const fetcherRef = useRef(fetcher)
  fetcherRef.current = fetcher

  useEffect(() => {
    if (!enabled) {
      setLoading(false)
      return
    }
    let cancelled = false
    setLoading(true)
    fetcherRef
      .current()
      .then((res) => {
        if (!cancelled) setData(res)
      })
      .catch((err: unknown) => {
        if (cancelled) return
        setError(err instanceof ApiError || err instanceof Error ? err.message : 'Something went wrong')
      })
      .finally(() => {
        if (!cancelled) setLoading(false)
      })
    return () => {
      cancelled = true
    }
  }, [...deps, enabled, nonce])

  return { data, error, loading, reload: useCallback(() => setNonce((n) => n + 1), []) }
}

export function useMutation<TArgs extends unknown[], TResult>(action: (...args: TArgs) => Promise<TResult>) {
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const mutate = useCallback(
    async (...args: TArgs) => {
      setLoading(true)
      setError(null)
      try {
        return await action(...args)
      } catch (err) {
        const message = err instanceof Error ? err.message : 'Request failed'
        setError(message)
        return undefined
      } finally {
        setLoading(false)
      }
    },
    [action],
  )
  return { mutate, loading, error, setError }
}
