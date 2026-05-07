import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useTranslation } from 'i18next-react';
import { useAuth } from '../components/AuthContext';
import CosmicBackground from '../components/CosmicBackground';
import GlassCard from '../components/GlassCard';
import AnimatedButton from '../components/AnimatedButton';
import GlowBadge from '../components/GlowBadge';
import LanguageSwitcher from '../components/LanguageSwitcher';

const Login: React.FC = () => {
  const { t } = useTranslation();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const { login } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setError('');

    try {
      await login({ username: email, password });
      navigate('/dashboard');
    } catch (err: any) {
      const message = err?.response?.data?.detail || err?.message || 'Login failed';
      setError(message);
    } finally {
      setIsLoading(false);
    }
  };

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
            <div className="text-4xl font-bold bg-gradient-to-r from-blue-400 via-cyan-400 to-purple-400 bg-clip-text text-transparent animate-slide-in-fade">
              {t('common.leadpilot')}
            </div>
          </div>
          <h1 className="mt-6 text-3xl font-bold text-light-primary animate-slide-in-fade">
            {t('auth.welcomeBack')}
          </h1>
          <p className="mt-2 text-light-secondary animate-slide-in-fade">
            {t('auth.login')}
          </p>
        </div>

        {/* Login Card */}
        <GlassCard glow="blue" className="p-8 space-y-6 animate-slide-in-fade">
          {/* Admin Link */}
          <div className="text-center">
            <p className="text-sm text-light-tertiary mb-2">
              {t('auth.useAdminLogin')}
            </p>
            <a
              href="/admin/login"
              className="text-sm text-cyan-400 hover:text-cyan-300 transition"
            >
              {t('auth.useAdminLogin')}
            </a>
          </div>

          {/* Form */}
          <form onSubmit={handleSubmit} className="space-y-4">
            {/* Email Input */}
            <div>
              <label htmlFor="email" className="block text-sm font-medium text-light-secondary mb-2">
                {t('auth.email')}
              </label>
              <input
                id="email"
                name="email"
                type="email"
                required
                disabled={isLoading}
                className="w-full px-4 py-3 rounded-lg glass-panel focus:ring-2 focus:ring-cyan-400 focus:border-transparent text-light-primary placeholder-light-tertiary transition"
                placeholder="you@example.com"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
              />
            </div>

            {/* Password Input */}
            <div>
              <label htmlFor="password" className="block text-sm font-medium text-light-secondary mb-2">
                {t('auth.password')}
              </label>
              <input
                id="password"
                name="password"
                type="password"
                required
                disabled={isLoading}
                className="w-full px-4 py-3 rounded-lg glass-panel focus:ring-2 focus:ring-cyan-400 focus:border-transparent text-light-primary placeholder-light-tertiary transition"
                placeholder="••••••••"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
              />
            </div>

            {/* Info Message */}
            <div className="bg-blue-500/10 border border-blue-500/30 rounded-lg p-3">
              <p className="text-xs text-light-secondary">
                💡 {t('auth.accountsNote')}
              </p>
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
            >
              {isLoading ? t('auth.signingIn') : t('auth.signIn')}
            </AnimatedButton>
          </form>
        </GlassCard>

        {/* Footer Info */}
        <div className="mt-8 text-center">
          <p className="text-xs text-light-tertiary">
            {t('auth.poweredBy')} <span className="text-cyan-400 font-semibold">{t('common.leadpilot')}</span>
          </p>
        </div>
      </div>
    </div>
  );
};

export default Login;

