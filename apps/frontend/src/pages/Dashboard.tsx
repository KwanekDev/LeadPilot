import React from 'react'
import { useQuery } from '@tanstack/react-query'
import { useAuth } from '../components/AuthContext'
import api from '../lib/api'
import { AnalyticsData } from '../types'
import GlassCard from '../components/GlassCard'
import GlowBadge from '../components/GlowBadge'

const formatCurrency = (amount?: number) => {
  if (amount == null) return '$0.00'
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
    maximumFractionDigits: 2,
  }).format(amount)
}

const StatCard: React.FC<{
  label: string
  value: string | number
  icon: string
  glow?: 'blue' | 'purple' | 'cyan'
}> = ({ label, value, icon, glow = 'blue' }) => (
  <GlassCard glow={glow} className="p-6 flex items-center gap-4">
    <div className="text-4xl">{icon}</div>
    <div>
      <p className="text-light-tertiary text-sm font-medium">{label}</p>
      <p className="text-3xl font-bold text-light-primary mt-1">{value}</p>
    </div>
  </GlassCard>
)

const Dashboard: React.FC = () => {
  const { user } = useAuth()

  const { data: analytics, isLoading, error } = useQuery<AnalyticsData>({
    queryKey: ['analytics'],
    queryFn: async () => {
      const response = await api.get('/analytics/dashboard')
      return response.data
    },
  })

  if (isLoading) {
    return (
      <GlassCard glow="blue" className="p-12 text-center">
        <div className="mx-auto h-12 w-12 animate-spin rounded-full border-4 border-cyan-500 border-t-transparent"></div>
        <p className="mt-6 text-light-secondary">Loading your dashboard...</p>
      </GlassCard>
    )
  }

  if (error) {
    return (
      <GlassCard className="p-12 text-center border-red-500/30">
        <p className="text-red-300 font-medium">❌ Error loading dashboard data</p>
      </GlassCard>
    )
  }

  return (
    <div className="space-y-6 animate-slide-in-fade">
      {/* Welcome Banner */}
      <GlassCard glow="blue" className="p-8">
        <div className="flex flex-col gap-4 sm:flex-row sm:items-end sm:justify-between">
          <div>
            <h2 className="text-3xl font-bold text-light-primary">
              Welcome back, {user?.first_name || user?.email}
            </h2>
            <p className="mt-2 text-light-secondary">
              Your command center for leads, jobs, customers, and reminders
            </p>
          </div>
          <GlowBadge variant="cyan" size="md">
            Tenant {user?.tenant_id ?? 'N/A'}
          </GlowBadge>
        </div>
      </GlassCard>

      {/* KPI Cards Grid */}
      <div className="grid grid-cols-1 gap-4 md:grid-cols-2 xl:grid-cols-4">
        <StatCard
          label="Total Leads"
          value={analytics?.total_leads ?? 0}
          icon="👥"
          glow="blue"
        />
        <StatCard
          label="Total Customers"
          value={analytics?.total_customers ?? 0}
          icon="🏢"
          glow="cyan"
        />
        <StatCard
          label="Active Jobs"
          value={analytics?.active_jobs ?? 0}
          icon="⚙️"
          glow="purple"
        />
        <StatCard
          label="Active Reminders"
          value={analytics?.active_reminders ?? 0}
          icon="🔔"
          glow="blue"
        />
      </div>

      {/* Metrics Section */}
      <div className="grid grid-cols-1 gap-4 md:grid-cols-3">
        <GlassCard glow="cyan" className="p-6">
          <p className="text-light-tertiary text-sm font-medium">Revenue This Month</p>
          <p className="text-3xl font-bold text-light-primary mt-2">
            {formatCurrency(analytics?.revenue_this_month)}
          </p>
          <p className="text-xs text-light-tertiary mt-3">From completed jobs</p>
        </GlassCard>

        <GlassCard glow="purple" className="p-6">
          <p className="text-light-tertiary text-sm font-medium">Average Job Value</p>
          <p className="text-3xl font-bold text-light-primary mt-2">
            {formatCurrency(analytics?.average_job_value)}
          </p>
          <p className="text-xs text-light-tertiary mt-3">Per completed job</p>
        </GlassCard>

        <GlassCard glow="blue" className="p-6">
          <p className="text-light-tertiary text-sm font-medium">Conversion Rate</p>
          <p className="text-3xl font-bold text-light-primary mt-2">
            {(analytics?.conversion_rate?.toFixed(1) ?? 0)}%
          </p>
          <p className="text-xs text-light-tertiary mt-3">Leads to customers</p>
        </GlassCard>
      </div>

      {/* Pipeline Overview */}
      <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
        {/* Lead Status */}
        <GlassCard glow="blue" className="p-6">
          <h3 className="text-xl font-bold text-light-primary mb-1">Lead Pipeline</h3>
          <p className="text-light-tertiary text-sm mb-6">Status distribution across your leads</p>
          <div className="space-y-3">
            {analytics?.lead_status && Object.entries(analytics.lead_status).length > 0 ? (
              Object.entries(analytics.lead_status).map(([status, count]) => {
                const percentage = ((count as number) / Object.values(analytics.lead_status).reduce((a, b) => (a as number) + (b as number), 0)) * 100
                return (
                  <div key={status} className="flex items-center justify-between">
                    <div className="flex items-center gap-3 flex-1">
                      <span className="text-light-secondary text-sm font-medium">{status}</span>
                      <div className="flex-1 h-2 rounded-full bg-slate-700/30 overflow-hidden">
                        <div
                          className="h-full bg-gradient-to-r from-cyan-500 to-blue-500 rounded-full transition-all"
                          style={{ width: `${percentage}%` }}
                        ></div>
                      </div>
                    </div>
                    <span className="text-light-primary font-bold ml-2 min-w-max">{count}</span>
                  </div>
                )
              })
            ) : (
              <p className="text-light-tertiary text-sm">No lead data available</p>
            )}
          </div>
        </GlassCard>

        {/* Job Status */}
        <GlassCard glow="purple" className="p-6">
          <h3 className="text-xl font-bold text-light-primary mb-1">Job Overview</h3>
          <p className="text-light-tertiary text-sm mb-6">Status of your active jobs</p>
          <div className="space-y-3">
            {analytics?.job_status && Object.entries(analytics.job_status).length > 0 ? (
              Object.entries(analytics.job_status).map(([status, count]) => {
                const percentage = ((count as number) / Object.values(analytics.job_status).reduce((a, b) => (a as number) + (b as number), 0)) * 100
                return (
                  <div key={status} className="flex items-center justify-between">
                    <div className="flex items-center gap-3 flex-1">
                      <span className="text-light-secondary text-sm font-medium">{status}</span>
                      <div className="flex-1 h-2 rounded-full bg-slate-700/30 overflow-hidden">
                        <div
                          className="h-full bg-gradient-to-r from-purple-500 to-pink-500 rounded-full transition-all"
                          style={{ width: `${percentage}%` }}
                        ></div>
                      </div>
                    </div>
                    <span className="text-light-primary font-bold ml-2 min-w-max">{count}</span>
                  </div>
                )
              })
            ) : (
              <p className="text-light-tertiary text-sm">No job data available</p>
            )}
          </div>
        </GlassCard>
      </div>
    </div>
  )
}

export default Dashboard
