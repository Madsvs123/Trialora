import { Navigate, Route, Routes } from 'react-router-dom'
import { AppLayout } from './components/layout/AppLayout'
import { AuthLayout } from './components/layout/AuthLayout'
import { ProtectedRoute } from './components/layout/ProtectedRoute'
import { Spinner } from './components/ui'
import { useAuth } from './hooks/useAuth'
import { useTheme } from './hooks/useTheme'
import { AcceptInvitePage, ForgotPasswordPage, LoginPage, RegisterPage, ResetPasswordPage } from './pages/auth/AuthPages'
import { DashboardPage } from './pages/dashboard/DashboardPage'
import { EnrollmentPage } from './pages/enrollment/EnrollmentPage'
import { IssueDetailPage, IssueListPage } from './pages/issues/IssuePages'
import { MonitoringDetailPage, MonitoringPage } from './pages/monitoring/MonitoringPages'
import {
  AdminPage,
  AnalyticsPage,
  DocumentsPage,
  NotificationsPage,
  PaymentsPage,
  ReportsPage,
  SearchPage,
  StaffPage,
  TasksPage,
} from './pages/operations/OperationsPages'
import { ParticipantDetailPage, ParticipantListPage } from './pages/participants/ParticipantPages'
import { SiteDetailPage, SiteListPage } from './pages/sites/SitePages'
import { StudyDetailPage, StudyListPage } from './pages/studies/StudyPages'
import { VisitDetailPage, VisitListPage } from './pages/visits/VisitPages'
import { SafetyDetailPage, SafetyListPage } from './pages/safety/SafetyPages'
import { RegulatoryPage } from './pages/regulatory/RegulatoryPages'
import { InventoryPage } from './pages/inventory/InventoryPages'

function HomeRedirect() {
  const { isAuthenticated, loading } = useAuth()
  if (loading) {
    return (
      <div style={{ minHeight: '100vh', display: 'grid', placeItems: 'center' }}>
        <Spinner label="Loading Trialora…" />
      </div>
    )
  }
  return <Navigate to={isAuthenticated ? '/app' : '/login'} replace />
}

export default function App() {
  useTheme()
  return (
    <Routes>
      <Route path="/" element={<HomeRedirect />} />
      <Route element={<AuthLayout />}>
        <Route path="/login" element={<LoginPage />} />
        <Route path="/register" element={<RegisterPage />} />
        <Route path="/forgot-password" element={<ForgotPasswordPage />} />
        <Route path="/reset-password" element={<ResetPasswordPage />} />
        <Route path="/accept-invite" element={<AcceptInvitePage />} />
      </Route>
      <Route element={<ProtectedRoute />}>
        <Route path="/app" element={<AppLayout />}>
          <Route index element={<DashboardPage />} />
          <Route path="enrollment" element={<EnrollmentPage />} />
          <Route path="studies" element={<StudyListPage />} />
          <Route path="studies/:id" element={<StudyDetailPage />} />
          <Route path="sites" element={<SiteListPage />} />
          <Route path="sites/:id" element={<SiteDetailPage />} />
          <Route path="participants" element={<ParticipantListPage />} />
          <Route path="participants/:id" element={<ParticipantDetailPage />} />
          <Route path="visits" element={<VisitListPage />} />
          <Route path="visits/:id" element={<VisitDetailPage />} />
          <Route path="monitoring" element={<MonitoringPage />} />
          <Route path="monitoring/:id" element={<MonitoringDetailPage />} />
          <Route path="issues" element={<IssueListPage />} />
          <Route path="issues/:id" element={<IssueDetailPage />} />
          <Route path="safety" element={<SafetyListPage />} />
          <Route path="safety/:id" element={<SafetyDetailPage />} />
          <Route path="regulatory" element={<RegulatoryPage />} />
          <Route path="inventory" element={<InventoryPage />} />
          <Route path="documents" element={<DocumentsPage />} />
          <Route path="staff" element={<StaffPage />} />
          <Route path="tasks" element={<TasksPage />} />
          <Route path="payments" element={<PaymentsPage />} />
          <Route path="analytics" element={<AnalyticsPage />} />
          <Route path="reports" element={<ReportsPage />} />
          <Route path="search" element={<SearchPage />} />
          <Route path="notifications" element={<NotificationsPage />} />
          <Route path="admin" element={<AdminPage />} />
        </Route>
      </Route>
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  )
}
