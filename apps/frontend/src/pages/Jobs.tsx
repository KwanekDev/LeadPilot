import React from 'react'
import { useQuery } from '@tanstack/react-query'
import api from '../lib/api'
import { Job } from '../types'
import GlassCard from '../components/GlassCard'
import GlowBadge from '../components/GlowBadge'

const Jobs: React.FC = () => {
  const { data, isLoading, error } = useQuery<Job[]>({
    queryKey: ['jobs'],
    queryFn: async () => {
      const response = await api.get('/jobs')
      return response.data
    },
  })

  if (isLoading) {
    return (
      <GlassCard glow="blue" className="p-12 text-center">
        <div className="mx-auto h-12 w-12 animate-spin rounded-full border-4 border-cyan-500 border-t-transparent"></div>
        <p className="mt-6 text-light-secondary">Loading jobs...</p>
      </GlassCard>
    )
  }

  if (error) {
    return (
      <GlassCard className="p-12 text-center border-red-500/30">
        <p className="text-red-300 font-medium">❌ Unable to load jobs</p>
      </GlassCard>
    )
  }

  return (
    <div className="space-y-6 animate-slide-in-fade">
      <GlassCard glow="blue" className="p-6">
        <div className="flex flex-col gap-4 sm:flex-row sm:items-end sm:justify-between">
          <div>
            <h2 className="text-3xl font-bold text-light-primary">Jobs</h2>
            <p className="mt-2 text-light-secondary">Manage scheduled work and installations</p>
          </div>
          <GlowBadge variant="cyan" size="md">
            {data?.length ?? 0} jobs
          </GlowBadge>
        </div>
      </GlassCard>

      <GlassCard glow="blue" className="p-6 overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="border-b border-slate-700/30">
                <th className="px-4 py-3 text-left text-xs font-semibold uppercase tracking-wider text-light-tertiary">Job Title</th>
                <th className="px-4 py-3 text-left text-xs font-semibold uppercase tracking-wider text-light-tertiary">Customer</th>
                <th className="px-4 py-3 text-left text-xs font-semibold uppercase tracking-wider text-light-tertiary">Status</th>
                <th className="px-4 py-3 text-left text-xs font-semibold uppercase tracking-wider text-light-tertiary">Scheduled</th>
                <th className="px-4 py-3 text-left text-xs font-semibold uppercase tracking-wider text-light-tertiary">Value</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-700/20">
              {data?.map((job) => (
                <tr key={job.id} className="hover:bg-slate-700/20 transition-colors group">
                  <td className="px-4 py-4 text-sm text-light-primary font-medium group-hover:text-cyan-300 transition">
                    {job.title}
                  </td>
                  <td className="px-4 py-4 text-sm text-light-tertiary">{job.customer_id}</td>
                  <td className="px-4 py-4 text-sm">
                    <GlowBadge variant="blue" size="sm">
                      {job.status}
                    </GlowBadge>
                  </td>
                  <td className="px-4 py-4 text-sm text-light-tertiary">
                    {job.scheduled_date ? new Date(job.scheduled_date).toLocaleDateString() : 'TBD'}
                  </td>
                  <td className="px-4 py-4 text-sm text-light-primary font-medium">
                    {job.total_cost ? `$${(job.total_cost / 100).toLocaleString()}` : 'N/A'}
                  </td>
                </tr>
              ))}
              {data?.length === 0 && (
                <tr>
                  <td colSpan={5} className="px-4 py-8 text-center text-light-tertiary">
                    <div className="flex flex-col items-center gap-2">
                      <p className="text-lg">⚙️</p>
                      <p>No jobs available yet</p>
                    </div>
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </GlassCard>
    </div>
  )
}

export default Jobs
