import { NavLink, Outlet, useNavigate } from 'react-router-dom'
import { useTranslation } from 'i18next-react'
import { useAuth } from './AuthContext'
import GlassCard from './GlassCard'
import AnimatedButton from './AnimatedButton'
import CosmicBackground from './CosmicBackground'
import LanguageSwitcher from './LanguageSwitcher'

const AppShell: React.FC = () => {
  const { t } = useTranslation()
  const { user, adminEmail, logout, isAdmin } = useAuth()
  const navigate = useNavigate()

  const navItems = [
    { name: t('navigation.dashboard'), to: '/dashboard', icon: '📊' },
    { name: t('navigation.calendar'), to: '/calendar', icon: '📅' },
    { name: t('navigation.leads'), to: '/leads', icon: '👥' },
    { name: t('navigation.customers'), to: '/customers', icon: '🏢' },
    { name: t('navigation.jobs'), to: '/jobs', icon: '⚙️' },
    { name: t('navigation.reminders'), to: '/reminders', icon: '🔔' },
    { name: t('navigation.settings'), to: '/settings', icon: '⚡' },
  ]

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  return (
    <div className="relative min-h-screen cosmic-bg text-light-primary">
      <CosmicBackground intensity="medium" />

      {/* Header */}
      <header className="relative z-10 border-b border-slate-700/30 glass-panel-lg glass-panel rounded-none">
        <div className="mx-auto flex max-w-7xl items-center justify-between px-4 py-4 sm:px-6 lg:px-8">
          {/* Logo Section */}
          <div className="flex items-center gap-3">
            <div className="text-2xl font-bold bg-gradient-to-r from-blue-400 to-cyan-400 bg-clip-text text-transparent">
              {t('common.leadpilot')}
            </div>
            <div className="hidden md:block h-8 w-px bg-slate-700/30"></div>
            <p className="hidden md:block text-xs text-light-tertiary">Premium lead management</p>
          </div>

          {/* User Info & Language & Logout */}
          <div className="flex items-center gap-3 sm:gap-4">
            <LanguageSwitcher />
            <div className="hidden sm:block h-6 w-px bg-slate-700/30"></div>
            <div className="hidden sm:block text-right">
              <p className="text-sm font-semibold text-light-primary">
                {isAdmin ? adminEmail : (user?.first_name || user?.email)}
              </p>
              <p className="text-xs text-light-tertiary">
                {isAdmin ? t('auth.adminLogin') : `Tenant ${user?.tenant_id ?? 'N/A'}`}
              </p>
            </div>
            <AnimatedButton
              onClick={handleLogout}
              variant="secondary"
              size="sm"
            >
              {t('common.logout')}
            </AnimatedButton>
          </div>
        </div>
      </header>

      {/* Main Layout */}
      <div className="relative z-10 mx-auto flex max-w-7xl gap-6 px-4 py-6 sm:px-6 lg:px-8">
        {/* Sidebar */}
        <aside className="w-full lg:w-64 flex-shrink-0">
          <GlassCard glow="blue" className="p-4 sticky top-24">
            <nav className="space-y-2">
              {isAdmin && (
                <NavLink
                  to="/admin"
                  className={({ isActive }) =>
                    `flex items-center gap-3 rounded-lg px-4 py-3 text-sm font-medium transition smooth-transition ${
                      isActive
                        ? 'bg-gradient-to-r from-red-500/30 to-pink-500/30 text-red-200 glow-sm border border-red-500/30'
                        : 'text-light-tertiary hover:text-light-secondary hover:bg-slate-700/30'
                    }`
                  }
                >
                  <span>🔧</span>
                  <span>{t('navigation.admin')}</span>
                </NavLink>
              )}
              {navItems.map((item) => (
                <NavLink
                  key={item.to}
                  to={item.to}
                  className={({ isActive }) =>
                    `flex items-center gap-3 rounded-lg px-4 py-3 text-sm font-medium transition smooth-transition ${
                      isActive
                        ? 'bg-gradient-to-r from-blue-500/30 to-cyan-500/30 text-cyan-200 glow-sm border border-cyan-500/30'
                        : 'text-light-tertiary hover:text-light-secondary hover:bg-slate-700/30'
                    }`
                  }
                >
                  <span>{item.icon}</span>
                  <span>{item.name}</span>
                </NavLink>
              ))}
            </nav>
          </GlassCard>
        </aside>

        {/* Main Content */}
        <main className="flex-1 min-h-96">
          <Outlet />
        </main>
      </div>
    </div>
  )
}

export default AppShell


