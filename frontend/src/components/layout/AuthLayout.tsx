import { Outlet } from 'react-router-dom'

export function AuthLayout() {
  return (
    <div style={{ minHeight: '100vh', display: 'grid', placeItems: 'center', padding: 24 }}>
      <div style={{ width: 'min(440px, 100%)' }}>
        <div style={{ marginBottom: 18 }}>
          <div style={{ fontFamily: 'var(--tr-display)', fontSize: 32, color: 'var(--tr-forest)' }}>Trialora</div>
          <p className="tr-muted">Clinical trial operations for sponsors, CROs, and sites.</p>
        </div>
        <div className="tr-panel" style={{ padding: 22 }}>
          <Outlet />
        </div>
      </div>
    </div>
  )
}
