import { Bell, Menu, Moon, Sun } from 'lucide-react'
import { Link } from 'react-router-dom'
import { useAuth } from '../../hooks/useAuth'
import { useTheme } from '../../hooks/useTheme'

export function TopBar({ onMenu }: { onMenu: () => void }) {
  const { user, logout, orgId, setOrgId } = useAuth()
  const { theme, toggle } = useTheme()

  return (
    <header style={{ height: 'var(--tr-topbar)', display: 'flex', alignItems: 'center', justifyContent: 'space-between', padding: '0 20px', borderBottom: '1px solid var(--tr-line)', background: 'rgba(255,253,248,0.8)', backdropFilter: 'blur(10px)' }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
        <button onClick={onMenu} className="tr-menu" style={{ border: 0, background: 'none', cursor: 'pointer' }}>
          <Menu size={18} />
        </button>
        <span className="tr-muted" style={{ fontSize: 13 }}>Clinical operations</span>
      </div>
      <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
        {user?.organizations && user.organizations.length > 1 && (
          <select value={orgId || ''} onChange={(e) => setOrgId(e.target.value)} style={{ height: 34, borderRadius: 8, border: '1px solid var(--tr-line-strong)', background: 'var(--tr-cream)' }}>
            {user.organizations.map((org) => (
              <option key={org.id} value={org.id}>{org.name}</option>
            ))}
          </select>
        )}
        <Link to="/app/notifications" style={{ color: 'var(--tr-text)' }}><Bell size={18} /></Link>
        <button onClick={toggle} style={{ border: 0, background: 'none', cursor: 'pointer', color: 'var(--tr-text)' }}>
          {theme === 'light' ? <Moon size={16} /> : <Sun size={16} />}
        </button>
        <div style={{ textAlign: 'right' }}>
          <div style={{ fontSize: 13, fontWeight: 700 }}>{user?.display_name || user?.email}</div>
          <button onClick={() => void logout()} style={{ border: 0, background: 'none', color: 'var(--tr-muted)', cursor: 'pointer', fontSize: 12 }}>Sign out</button>
        </div>
      </div>
    </header>
  )
}
