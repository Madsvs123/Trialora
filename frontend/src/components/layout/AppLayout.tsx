import { useState } from 'react'
import { Outlet } from 'react-router-dom'
import { Sidebar } from './Sidebar'
import { TopBar } from './TopBar'

export function AppLayout() {
  const [open, setOpen] = useState(false)
  return (
    <div className="tr-shell">
      <Sidebar open={open} onClose={() => setOpen(false)} />
      <div className="tr-main">
        <TopBar onMenu={() => setOpen(true)} />
        <div className="tr-content">
          <Outlet />
        </div>
      </div>
    </div>
  )
}
