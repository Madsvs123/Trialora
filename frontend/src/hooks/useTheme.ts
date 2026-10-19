import { useEffect, useState } from 'react'

export function useTheme() {
  const [theme, setTheme] = useState(localStorage.getItem('tr_theme') || 'light')
  useEffect(() => {
    document.documentElement.dataset.theme = theme
    localStorage.setItem('tr_theme', theme)
  }, [theme])
  return { theme, toggle: () => setTheme((t) => (t === 'light' ? 'dark' : 'light')) }
}
