import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useTranslation } from 'i18next-react'
import { useAuth } from '../components/AuthContext'
import CosmicBackground from '../components/CosmicBackground'
import GlassCard from '../components/GlassCard'
import AnimatedButton from '../components/AnimatedButton'
import LanguageSwitcher from '../components/LanguageSwitcher'

const AdminLogin: React.FC = () => {
  const { t } = useTranslation()
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState('')
  const { adminLogin } = useAuth()
  const navigate = useNavigate()

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setIsLoading(true)
    setError('')

    try {
      await adminLogin({ username: email, password })
      navigate('/admin')
    } catch (err: any) {
      const message = err?.response?.data?.detail || err?.message || 'Admin login failed'
      setError(message)
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="relative min-h-screen cosmic-bg flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8 overflow-hidden">
      <CosmicBackground intensity="high" />
      
      {/* Language Switcher */}
      <div className="absolute top-4 right-4 z-20">
        <LanguageSwitcher />
      </div>

      {/* Content */}
      <div className="relative z-10 w-full max-w-md">
        {/* Welcome Section */}
        <div className="text-center mb-8">
          <div className="inline-block mb-4">
            <div className="text-3xl font-bold text-red-400">⚡</div>
          </div>
          <h1 className="text-3xl font-bold text-light-primary">
            {t('auth.adminLogin')}
          </h1>
          <p className="mt-2 text-light-secondary text-sm">
            {t('auth.restrictedAccess')}
          </p>
        </div>

        {/* Login Card */}
        <GlassCard className="p-8 space-y-6 border-red-500/20">
          <div className="flex items-center justify-center gap-2 px-4 py-2 bg-red-500/10 border border-red-500/30 rounded-lg">
            <span className="text-red-400 text-sm font-semibold">🔒 {t('auth.restrictedAccess')}</span>
          </div>

          {/* Form */}
          <form onSubmit={handleSubmit} className="space-y-4">
            {/* Email Input */}
            <div>
              <label htmlFor="email" className="block text-sm font-medium text-light-secondary mb-2">
                {t('auth.adminEmail')}
              </label>
              <input
                id="email"
                name="email"
                type="email"
                required
                disabled={isLoading}
                className="w-full px-4 py-3 rounded-lg glass-panel focus:ring-2 focus:ring-red-400 focus:border-transparent text-light-primary placeholder-light-tertiary transition"
                placeholder="admin@system.local"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
              />
            </div>

            {/* Password Input */}
            <div>
              <label htmlFor="password" className="block text-sm font-medium text-light-secondary mb-2">
                {t('auth.adminPassword')}
              </label>
              <input
                id="password"
                name="password"
                type="password"
                required
                disabled={isLoading}
                className="w-full px-4 py-3 rounded-lg glass-panel focus:ring-2 focus:ring-red-400 focus:border-transparent text-light-primary placeholder-light-tertiary transition"
                placeholder="••••••••"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
              />
            </div>

            {/* Error Message */}
            {error && (
              <div className="bg-red-500/10 border border-red-500/30 rounded-lg p-3">
                <p className="text-sm text-red-300 text-center">
                  {error}
                </p>
              </div>
            )}

            {/* Submit Button */}
            <AnimatedButton
              type="submit"
              variant="primary"
              size="md"
              loading={isLoading}
              className="w-full"
              style={{
                background: 'linear-gradient(135deg, rgba(239, 68, 68, 0.8), rgba(236, 72, 153, 0.8))',
              }}
            >
              {isLoading ? t('auth.signingIn') : t('auth.signIn')}
            </AnimatedButton>
          </form>

          {/* Back Link */}
          <div className="text-center pt-4 border-t border-slate-700/30">
            <p className="text-xs text-light-tertiary mb-2">{t('auth.returnToUserLogin')}</p>
            <a
              href="/login"
              className="text-sm text-cyan-400 hover:text-cyan-300 transition"
            >
              {t('auth.returnToUserLogin')}
            </a>
          </div>
        </GlassCard>

        {/* Footer Info */}
        <div className="mt-8 text-center">
          <p className="text-xs text-light-tertiary">
            {t('auth.poweredBy')} <span className="text-red-400 font-semibold">{t('common.leadpilot')}</span>
          </p>
        </div>
      </div>
    </div>
  )
}

export default AdminLogin

