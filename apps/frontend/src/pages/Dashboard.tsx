import React from 'react'
import { useQuery } from '@tanstack/react-query'
import { useAuth } from '../components/AuthContext'
import api from '../lib/api'
import { AnalyticsData } from '../types'

const formatCurrency = (amount?: number) => {
  if (amount == null) return '$0.00'
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
    maximumFractionDigits: 2,
  }).format(amount)
}

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
      <div className="rounded-3xl border border-slate-200 bg-white p-8 shadow-sm text-center">
        <div className="mx-auto h-12 w-12 animate-spin rounded-full border-4 border-indigo-500 border-t-transparent"></div>
        <p className="mt-4 text-sm text-slate-600">Loading dashboard...</p>
      </div>
    )
  }

  if (error) {
    return (
      <div className="rounded-3xl border border-red-200 bg-red-50 p-8 shadow-sm text-center">
        <p className="text-sm font-medium text-red-700">Error loading dashboard data.</p>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
        <div className="flex flex-col gap-3 sm:flex-row sm:items-end sm:justify-between">
          <div>
            <h2 className="text-2xl font-semibold text-slate-900">Welcome back, {user?.first_name || user?.email}</h2>
            <p className="mt-2 text-sm text-slate-500">Your home for leads, jobs, customers, and reminders.</p>
          </div>
          <div className="rounded-2xl bg-slate-50 px-4 py-3 text-sm text-slate-600">
            Updated live from tenant {user?.tenant_id ?? 'N/A'}
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 gap-6 xl:grid-cols-2">
        <div className="grid gap-6 md:grid-cols-2">
          {[
            { label: 'Total Leads', value: analytics?.total_leads ?? 0, accent: 'bg-blue-500' },
            { label: 'Total Customers', value: analytics?.total_customers ?? 0, accent: 'bg-emerald-500' },
            { label: 'Active Jobs', value: analytics?.active_jobs ?? 0, accent: 'bg-yellow-500' },
            { label: 'Active Reminders', value: analytics?.active_reminders ?? 0, accent: 'bg-purple-500' },
          ].map((card) => (
            <div key={card.label} className="rounded-3xl border border-slate-200 bg-white p-5 shadow-sm">
              <div className="flex items-center gap-4">
                <div className={`flex h-11 w-11 items-center justify-center rounded-2xl ${card.accent}`}>
                  <span className="text-sm font-bold text-white">{card.label.charAt(0)}</span>
                </div>
                <div>
                  <p className="text-sm text-slate-500">{card.label}</p>
                  <p className="mt-2 text-3xl font-semibold text-slate-900">{card.value}</p>
                </div>
              </div>
            </div>
          ))}
        </div>

        <div className="space-y-6">
          {[
            { label: 'Revenue This Month', value: formatCurrency(analytics?.revenue_this_month), description: 'Completed jobs revenue.' },
            { label: 'Average Job Value', value: formatCurrency(analytics?.average_job_value), description: 'Average job value for completed work.' },
            { label: 'Conversion Rate', value: `${analytics?.conversion_rate?.toFixed(1) ?? 0}%`, description: 'Leads converted into customers.' },
          ].map((metric) => (
            <div key={metric.label} className="rounded-3xl border border-slate-200 bg-white p-5 shadow-sm">
              <p className="text-sm text-slate-500">{metric.label}</p>
              <p className="mt-2 text-3xl font-semibold text-slate-900">{metric.value}</p>
              <p className="mt-3 text-sm text-slate-500">{metric.description}</p>
            </div>
          ))}
        </div>
      </div>

      <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
        <div className="grid gap-6 lg:grid-cols-2">
          <section>
            <h3 className="text-lg font-semibold text-slate-900">Lead status overview</h3>
            <p className="mt-1 text-sm text-slate-500">Track where your pipeline currently stands.</p>
            <div className="mt-5 space-y-3">
              {analytics?.lead_status && Object.entries(analytics.lead_status).length > 0 ? (
                Object.entries(analytics.lead_status).map(([status, count]) => (
                  <div key={status} className="flex items-center justify-between rounded-3xl bg-slate-50 px-4 py-3 text-sm text-slate-700">
                    <span>{status}</span>
                    <span className="font-semibold text-slate-900">{count}</span>
                  </div>
                ))
              ) : (
                <p className="text-sm text-slate-500">No lead status data available yet.</p>
              )}
            </div>
          </section>

          <section>
            <h3 className="text-lg font-semibold text-slate-900">Job status overview</h3>
            <p className="mt-1 text-sm text-slate-500">See which jobs are scheduled, in progress, or completed.</p>
            <div className="mt-5 space-y-3">
              {analytics?.job_status && Object.entries(analytics.job_status).length > 0 ? (
                Object.entries(analytics.job_status).map(([status, count]) => (
                  <div key={status} className="flex items-center justify-between rounded-3xl bg-slate-50 px-4 py-3 text-sm text-slate-700">
                    <span>{status}</span>
                    <span className="font-semibold text-slate-900">{count}</span>
                  </div>
                ))
              ) : (
                <p className="text-sm text-slate-500">No job status data available yet.</p>
              )}
            </div>
          </section>
        </div>
      </div>
    </div>
  )
}

export default Dashboard;