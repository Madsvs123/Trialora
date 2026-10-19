import { NavLink } from 'react-router-dom'
import {
  Activity,
  AlertTriangle,
  BarChart3,
  Bell,
  ClipboardList,
  FileStack,
  FolderKanban,
  Landmark,
  LayoutDashboard,
  Search,
  Settings,
  ShieldCheck,
  Users,
  UserRound,
  Wallet,
  HeartPulse,
  Scale,
  Package,
} from 'lucide-react'
import { useAuth } from '../../hooks/useAuth'

const nav = [
  { to: '/app', label: 'Command center', icon: LayoutDashboard, end: true },
  { to: '/app/enrollment', label: 'Enrollment', icon: Activity },
  { to: '/app/studies', label: 'Studies', icon: FolderKanban },
  { to: '/app/sites', label: 'Sites', icon: Landmark },
  { to: '/app/participants', label: 'Participants', icon: Users },
  { to: '/app/visits', label: 'Visits', icon: ClipboardList },
  { to: '/app/monitoring', label: 'Monitoring', icon: ShieldCheck },
  { to: '/app/issues', label: 'Issues', icon: AlertTriangle },
  { to: '/app/safety', label: 'Safety', icon: HeartPulse },
  { to: '/app/regulatory', label: 'Regulatory', icon: Scale },
  { to: '/app/inventory', label: 'Inventory', icon: Package },
  { to: '/app/documents', label: 'Documents', icon: FileStack },
  { to: '/app/staff', label: 'Staff', icon: UserRound },
  { to: '/app/tasks', label: 'Tasks', icon: ClipboardList },
  { to: '/app/payments', label: 'Payments', icon: Wallet },
  { to: '/app/analytics', label: 'Analytics', icon: BarChart3 },
  { to: '/app/reports', label: 'Reports', icon: BarChart3 },
  { to: '/app/search', label: 'Search', icon: Search },
  { to: '/app/notifications', label: 'Notifications', icon: Bell },
  { to: '/app/admin', label: 'Administration', icon: Settings },
]

export function Sidebar({ open, onClose }: { open?: boolean; onClose?: () => void }) {
  const { user, orgId } = useAuth()
  const orgName = user?.organizations?.find((o) => o.id === orgId)?.name || user?.organizations?.[0]?.name || 'Trialora'

  return (
    <aside className={`tr-sidebar ${open ? 'open' : ''}`}>
      <div style={{ padding: '8px 10px 18px' }}>
        <div style={{ fontFamily: 'var(--tr-display)', fontSize: 22 }}>Trialora</div>
        <div style={{ fontSize: 12, opacity: 0.7, marginTop: 4 }}>{orgName}</div>
      </div>
      <nav style={{ display: 'grid', gap: 2 }}>
        {nav.map((item) => (
          <NavLink key={item.to} to={item.to} end={item.end} onClick={onClose}>
            <item.icon size={16} />
            {item.label}
          </NavLink>
        ))}
      </nav>
    </aside>
  )
}
