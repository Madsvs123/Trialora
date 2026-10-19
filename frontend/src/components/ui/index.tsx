import type { ButtonHTMLAttributes, CSSProperties, InputHTMLAttributes, ReactNode, SelectHTMLAttributes, TextareaHTMLAttributes } from 'react'
import { cn } from '../../utils/format'

export function Spinner({ label }: { label?: string }) {
  return (
    <div style={{ display: 'grid', placeItems: 'center', gap: 8 }}>
      <div style={{ width: 22, height: 22, border: '2px solid var(--tr-line-strong)', borderTopColor: 'var(--tr-forest)', borderRadius: '50%', animation: 'spin 0.7s linear infinite' }} />
      {label && <span className="tr-muted" style={{ fontSize: 13 }}>{label}</span>}
      <style>{`@keyframes spin { to { transform: rotate(360deg) } }`}</style>
    </div>
  )
}

export function Button({
  variant = 'primary',
  size = 'md',
  loading,
  fullWidth,
  children,
  style,
  ...rest
}: ButtonHTMLAttributes<HTMLButtonElement> & { variant?: 'primary' | 'secondary' | 'ghost' | 'danger' | 'outline'; size?: 'sm' | 'md'; loading?: boolean; fullWidth?: boolean }) {
  const variants: Record<string, CSSProperties> = {
    primary: { background: 'linear-gradient(135deg, #1b4d3e, #3d7a64)', color: '#fff', border: 'none' },
    secondary: { background: 'var(--tr-primary-soft)', color: 'var(--tr-forest)', border: 'none' },
    ghost: { background: 'transparent', color: 'var(--tr-muted)', border: 'none' },
    danger: { background: 'var(--tr-danger)', color: '#fff', border: 'none' },
    outline: { background: 'var(--tr-surface)', border: '1px solid var(--tr-line-strong)', color: 'var(--tr-text)' },
  }
  return (
    <button
      {...rest}
      disabled={rest.disabled || loading}
      style={{
        display: 'inline-flex',
        alignItems: 'center',
        justifyContent: 'center',
        gap: 8,
        height: size === 'sm' ? 32 : 40,
        padding: '0 14px',
        borderRadius: 10,
        fontWeight: 700,
        cursor: 'pointer',
        width: fullWidth ? '100%' : undefined,
        opacity: rest.disabled || loading ? 0.65 : 1,
        ...variants[variant],
        ...style,
      }}
    >
      {loading ? 'Working…' : children}
    </button>
  )
}

export function Input({ label, ...rest }: InputHTMLAttributes<HTMLInputElement> & { label?: string }) {
  return (
    <label style={{ display: 'grid', gap: 6, fontSize: 13, fontWeight: 650 }}>
      {label}
      <input
        {...rest}
        style={{
          height: 40,
          padding: '0 12px',
          borderRadius: 10,
          border: '1px solid var(--tr-line-strong)',
          background: 'var(--tr-cream)',
          fontWeight: 500,
        }}
      />
    </label>
  )
}

export function Select({ label, children, ...rest }: SelectHTMLAttributes<HTMLSelectElement> & { label?: string }) {
  return (
    <label style={{ display: 'grid', gap: 6, fontSize: 13, fontWeight: 650 }}>
      {label}
      <select {...rest} style={{ height: 40, padding: '0 12px', borderRadius: 10, border: '1px solid var(--tr-line-strong)', background: 'var(--tr-cream)' }}>
        {children}
      </select>
    </label>
  )
}

export function Textarea({ label, ...rest }: TextareaHTMLAttributes<HTMLTextAreaElement> & { label?: string }) {
  return (
    <label style={{ display: 'grid', gap: 6, fontSize: 13, fontWeight: 650 }}>
      {label}
      <textarea {...rest} style={{ minHeight: 90, padding: 12, borderRadius: 10, border: '1px solid var(--tr-line-strong)', background: 'var(--tr-cream)' }} />
    </label>
  )
}

export function Card({ title, subtitle, actions, children, style }: { title?: string; subtitle?: string; actions?: ReactNode; children: ReactNode; style?: CSSProperties }) {
  return (
    <div className="tr-panel" style={{ overflow: 'hidden', ...style }}>
      {(title || actions) && (
        <div style={{ display: 'flex', justifyContent: 'space-between', gap: 12, padding: '14px 16px', borderBottom: '1px solid var(--tr-line)' }}>
          <div>
            {title && <h3>{title}</h3>}
            {subtitle && <p className="tr-muted" style={{ marginTop: 4, fontSize: 13 }}>{subtitle}</p>}
          </div>
          {actions}
        </div>
      )}
      <div style={{ padding: 16 }}>{children}</div>
    </div>
  )
}

export function Badge({ children, tone = 'neutral' }: { children: ReactNode; tone?: 'neutral' | 'success' | 'warning' | 'danger' | 'info' }) {
  const map = {
    neutral: { background: 'var(--tr-primary-soft)', color: 'var(--tr-forest)' },
    success: { background: 'var(--tr-success-bg)', color: 'var(--tr-success)' },
    warning: { background: 'var(--tr-warning-bg)', color: 'var(--tr-warning)' },
    danger: { background: 'var(--tr-danger-bg)', color: 'var(--tr-danger)' },
    info: { background: 'var(--tr-info-bg)', color: 'var(--tr-info)' },
  }
  return <span className="tr-chip" style={map[tone]}>{children}</span>
}

export function StatCard({ label, value, hint, icon }: { label: string; value: ReactNode; hint?: string; icon?: ReactNode }) {
  return (
    <div className="tr-panel" style={{ padding: 16 }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', color: 'var(--tr-muted)', fontSize: 12, fontWeight: 700, letterSpacing: '0.04em', textTransform: 'uppercase' }}>
        {label}
        {icon}
      </div>
      <div style={{ fontFamily: 'var(--tr-display)', fontSize: 28, marginTop: 8 }}>{value}</div>
      {hint && <p className="tr-muted" style={{ marginTop: 4, fontSize: 12 }}>{hint}</p>}
    </div>
  )
}

export function EmptyState({ title, body }: { title: string; body?: string }) {
  return (
    <div style={{ padding: 28, textAlign: 'center' }}>
      <h3>{title}</h3>
      {body && <p className="tr-muted" style={{ marginTop: 6 }}>{body}</p>}
    </div>
  )
}

export function Modal({ open, title, onClose, children }: { open: boolean; title: string; onClose: () => void; children: ReactNode }) {
  if (!open) return null
  return (
    <div style={{ position: 'fixed', inset: 0, background: 'rgba(18,36,28,0.4)', display: 'grid', placeItems: 'center', zIndex: 60 }} onClick={onClose}>
      <div className="tr-panel" style={{ width: 'min(560px, calc(100vw - 32px))', padding: 20 }} onClick={(e) => e.stopPropagation()}>
        <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 14 }}>
          <h3>{title}</h3>
          <button onClick={onClose} style={{ border: 0, background: 'none', cursor: 'pointer' }}>Close</button>
        </div>
        {children}
      </div>
    </div>
  )
}

export function Tabs({ tabs, value, onChange }: { tabs: string[]; value: string; onChange: (v: string) => void }) {
  return (
    <div style={{ display: 'flex', gap: 6, flexWrap: 'wrap' }}>
      {tabs.map((tab) => (
        <button
          key={tab}
          onClick={() => onChange(tab)}
          className={cn(value === tab && 'active')}
          style={{
            border: 0,
            background: value === tab ? 'var(--tr-forest)' : 'transparent',
            color: value === tab ? '#fff' : 'var(--tr-muted)',
            borderRadius: 999,
            padding: '7px 12px',
            fontWeight: 700,
            cursor: 'pointer',
          }}
        >
          {tab}
        </button>
      ))}
    </div>
  )
}

export function ToastProvider({ children }: { children: ReactNode }) {
  return <>{children}</>
}

export function PageHeader({ title, subtitle, actions }: { title: string; subtitle?: string; actions?: ReactNode }) {
  return (
    <div style={{ display: 'flex', justifyContent: 'space-between', gap: 16, alignItems: 'flex-start' }}>
      <div>
        <h1>{title}</h1>
        {subtitle && <p className="tr-muted" style={{ marginTop: 6, maxWidth: 640 }}>{subtitle}</p>}
      </div>
      {actions}
    </div>
  )
}
