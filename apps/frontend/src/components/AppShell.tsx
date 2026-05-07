import { NavLink, Outlet, useNavigate } from 'react-router-dom'
import { useAuth } from './AuthContext'

const navItems = [
  { name: 'Dashboard', to: '/dashboard' },
  { name: 'Calendar', to: '/calendar' },
  { name: 'Leads', to: '/leads' },
  { name: 'Customers', to: '/customers' },
  { name: 'Jobs', to: '/jobs' },
  { name: 'Reminders', to: '/reminders' },
  { name: 'Settings', to: '/settings' },
]

const AppShell: React.FC = () => {
  const { user, adminEmail, logout, isAdmin } = useAuth()
  const navigate = useNavigate()

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  return (
    <div className="min-h-screen bg-slate-100">
      <div className="border-b border-slate-200 bg-white shadow-sm">
        <div className="mx-auto flex max-w-7xl items-center justify-between px-4 py-4 sm:px-6 lg:px-8">
          <div>
            <h1 className="text-xl font-semibold text-slate-900">LeadPilot</h1>
            <p className="text-sm text-slate-500">A better service workflow dashboard for your team.</p>
          </div>
          <div className="flex items-center gap-3">
            <div className="text-right">
              <p className="text-sm font-medium text-slate-900">{isAdmin ? adminEmail : (user?.first_name || user?.email)}</p>
              <p className="text-xs text-slate-500">
                {isAdmin ? `Administrator • ${adminEmail}` : `User • Tenant ${user?.tenant_id ?? 'N/A'}`}
              </p>
            </div>
            <button
              onClick={handleLogout}
              className="rounded-md bg-indigo-600 px-4 py-2 text-sm font-medium text-white shadow-sm transition hover:bg-indigo-700"
            >
              Logout
            </button>
          </div>
        </div>
      </div>

      <div className="mx-auto grid max-w-7xl grid-cols-1 gap-6 px-4 py-6 sm:px-6 lg:grid-cols-[240px_1fr] lg:px-8">
        <aside className="rounded-3xl border border-slate-200 bg-white p-5 shadow-sm">
          <nav className="space-y-1">
            {isAdmin && (
              <NavLink
                to="/admin"
                className={({ isActive }) =>
                  `block rounded-2xl px-4 py-3 text-sm font-medium transition ${
                    isActive
                      ? 'bg-red-600 text-white shadow-sm'
                      : 'text-red-700 hover:bg-red-50 hover:text-red-900'
                  }`
                }
              >
                🔧 Admin Panel
              </NavLink>
            )}
            {navItems.map((item) => (
              <NavLink
                key={item.to}
                to={item.to}
                className={({ isActive }) =>
                  `block rounded-2xl px-4 py-3 text-sm font-medium transition ${
                    isActive
                      ? 'bg-indigo-600 text-white shadow-sm'
                      : 'text-slate-700 hover:bg-slate-100 hover:text-slate-900'
                  }`
                }
              >
                {item.name}
              </NavLink>
            ))}
          </nav>
        </aside>

        <main className="space-y-6">
          <Outlet />
        </main>
      </div>
    </div>
  )
}

export default AppShell
