import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { AuthProvider, useAuth } from './components/AuthContext'

// React Router v7 future flags
const futureFlags = {
  v7_startTransition: true,
  v7_relativeSplatPath: true,
}
import AppShell from './components/AppShell'
import Login from './pages/Login'
import AdminLogin from './pages/AdminLogin'
import Admin from './pages/Admin'
import Dashboard from './pages/Dashboard'
import Calendar from './pages/Calendar'
import Leads from './pages/Leads'
import Customers from './pages/Customers'
import Jobs from './pages/Jobs'
import Reminders from './pages/Reminders'
import Settings from './pages/Settings'
import './App.css'

function ProtectedRoute({ children }: { children: React.ReactNode }) {
  const { user, isLoading, isAdmin } = useAuth()

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-indigo-600"></div>
      </div>
    )
  }

  if (isAdmin) {
    return <Navigate to="/admin" replace />
  }

  if (!user) {
    return <Navigate to="/login" replace />
  }

  return <>{children}</>
}

function AdminRoute({ children }: { children: React.ReactNode }) {
  const { isLoading, isAdmin } = useAuth()

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-indigo-600"></div>
      </div>
    )
  }

  if (!isAdmin) {
    return <Navigate to="/admin/login" replace />
  }

  return <>{children}</>
}

function AppRoutes() {
  const { user, isLoading, isAdmin } = useAuth()

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-indigo-600"></div>
      </div>
    )
  }

  return (
    <Routes>
      <Route
        path="/login"
        element={user && !isAdmin ? <Navigate to="/dashboard" replace /> : <Login />}
      />
      <Route
        path="/admin/login"
        element={isAdmin ? <Navigate to="/admin" replace /> : <AdminLogin />}
      />
      <Route
        path="/admin"
        element={
          <AdminRoute>
            <Admin />
          </AdminRoute>
        }
      />
      <Route
        element={
          <ProtectedRoute>
            <AppShell />
          </ProtectedRoute>
        }
      >
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/calendar" element={<Calendar />} />
        <Route path="/leads" element={<Leads />} />
        <Route path="/customers" element={<Customers />} />
        <Route path="/jobs" element={<Jobs />} />
        <Route path="/reminders" element={<Reminders />} />
        <Route path="/settings" element={<Settings />} />
        <Route path="/" element={<Navigate to="/dashboard" replace />} />
      </Route>
      <Route path="*" element={<Navigate to={isAdmin ? '/admin' : user ? '/dashboard' : '/login'} replace />} />
    </Routes>
  )
}


function App() {
  return (
    <AuthProvider>
      <BrowserRouter future={futureFlags}>
        <AppRoutes />
      </BrowserRouter>
    </AuthProvider>
  )
}

export default App