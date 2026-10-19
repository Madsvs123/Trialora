import { useState, type FormEvent } from 'react'
import { Link, useNavigate, useSearchParams } from 'react-router-dom'
import { Button, Input, Select } from '../../components/ui'
import { useAuth } from '../../hooks/useAuth'
import { authApi } from '../../api/client'
import { ApiError } from '../../api/http'

export function LoginPage() {
  const { login } = useAuth()
  const navigate = useNavigate()
  const [email, setEmail] = useState('admin@northwind.research')
  const [password, setPassword] = useState('Trialora!2026')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  async function onSubmit(e: FormEvent) {
    e.preventDefault()
    setLoading(true)
    setError('')
    try {
      await login(email, password)
      navigate('/app', { replace: true })
    } catch (err) {
      setError(err instanceof ApiError ? err.message : 'Login failed')
    } finally {
      setLoading(false)
    }
  }

  return (
    <form className="tr-form" onSubmit={onSubmit}>
      <div>
        <h2>Welcome back</h2>
        <p className="tr-muted" style={{ fontSize: 13 }}>Sign in to your research workspace.</p>
      </div>
      <Input label="Email" type="email" value={email} onChange={(e) => setEmail(e.target.value)} required />
      <Input label="Password" type="password" value={password} onChange={(e) => setPassword(e.target.value)} required />
      {error && <p style={{ color: 'var(--tr-danger)', fontSize: 13 }}>{error}</p>}
      <Button type="submit" loading={loading} fullWidth>Enter Trialora</Button>
      <div style={{ padding: 10, background: 'var(--tr-primary-soft)', borderRadius: 10, fontSize: 12 }}>
        Demo: <strong>admin@northwind.research</strong> / <strong>Trialora!2026</strong>
      </div>
      <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: 13 }}>
        <Link to="/forgot-password">Forgot password</Link>
        <Link to="/register">Create organization</Link>
      </div>
    </form>
  )
}

export function RegisterPage() {
  const { register } = useAuth()
  const navigate = useNavigate()
  const [form, setForm] = useState({ email: '', password: '', organization_name: '', org_type: 'research', display_name: '' })
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  async function onSubmit(e: FormEvent) {
    e.preventDefault()
    setLoading(true)
    try {
      await register(form)
      navigate('/app', { replace: true })
    } catch (err) {
      setError(err instanceof ApiError ? err.message : 'Registration failed')
    } finally {
      setLoading(false)
    }
  }

  return (
    <form className="tr-form" onSubmit={onSubmit}>
      <h2>Open a workspace</h2>
      <Input label="Organization" value={form.organization_name} onChange={(e) => setForm({ ...form, organization_name: e.target.value })} required />
      <Select label="Organization type" value={form.org_type} onChange={(e) => setForm({ ...form, org_type: e.target.value })}>
        <option value="research">Research organization</option>
        <option value="sponsor">Sponsor</option>
        <option value="cro">CRO</option>
        <option value="hospital">Hospital</option>
        <option value="academic">Academic center</option>
      </Select>
      <Input label="Your name" value={form.display_name} onChange={(e) => setForm({ ...form, display_name: e.target.value })} />
      <Input label="Email" type="email" value={form.email} onChange={(e) => setForm({ ...form, email: e.target.value })} required />
      <Input label="Password" type="password" value={form.password} onChange={(e) => setForm({ ...form, password: e.target.value })} required />
      {error && <p style={{ color: 'var(--tr-danger)', fontSize: 13 }}>{error}</p>}
      <Button type="submit" loading={loading} fullWidth>Create workspace</Button>
      <Link to="/login">Already have an account</Link>
    </form>
  )
}

export function ForgotPasswordPage() {
  const [email, setEmail] = useState('')
  const [done, setDone] = useState(false)
  return (
    <form className="tr-form" onSubmit={async (e) => { e.preventDefault(); await authApi.forgot(email); setDone(true) }}>
      <h2>Reset password</h2>
      <Input label="Email" type="email" value={email} onChange={(e) => setEmail(e.target.value)} required />
      <Button type="submit" fullWidth>Send reset</Button>
      {done && <p className="tr-muted">If the account exists, a reset token was issued.</p>}
      <Link to="/login">Back to sign in</Link>
    </form>
  )
}

export function ResetPasswordPage() {
  const [params] = useSearchParams()
  const [password, setPassword] = useState('')
  const navigate = useNavigate()
  return (
    <form className="tr-form" onSubmit={async (e) => { e.preventDefault(); await authApi.reset(params.get('token') || '', password); navigate('/login') }}>
      <h2>Choose a new password</h2>
      <Input label="Password" type="password" value={password} onChange={(e) => setPassword(e.target.value)} required />
      <Button type="submit" fullWidth>Update password</Button>
    </form>
  )
}

export function AcceptInvitePage() {
  const [params] = useSearchParams()
  const [form, setForm] = useState({ password: '', display_name: '' })
  const navigate = useNavigate()
  return (
    <form className="tr-form" onSubmit={async (e) => {
      e.preventDefault()
      await authApi.acceptInvite({ token: params.get('token') || '', ...form })
      navigate('/login')
    }}>
      <h2>Join your study team</h2>
      <Input label="Display name" value={form.display_name} onChange={(e) => setForm({ ...form, display_name: e.target.value })} />
      <Input label="Password" type="password" value={form.password} onChange={(e) => setForm({ ...form, password: e.target.value })} required />
      <Button type="submit" fullWidth>Accept invitation</Button>
    </form>
  )
}
