import React from 'react'
import { useQuery } from '@tanstack/react-query'
import api from '../lib/api'
import { Job } from '../types'

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
      <div className="rounded-3xl border border-slate-200 bg-white p-8 shadow-sm text-center">
        <div className="mx-auto h-12 w-12 animate-spin rounded-full border-4 border-indigo-500 border-t-transparent"></div>
        <p className="mt-4 text-sm text-slate-600">Loading jobs...</p>
      </div>
    )
  }

  if (error) {
    return (
      <div className="rounded-3xl border border-red-200 bg-red-50 p-8 shadow-sm text-center">
        <p className="text-sm font-medium text-red-700">Unable to load jobs.</p>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
        <div className="flex flex-col gap-2 sm:flex-row sm:items-end sm:justify-between">
          <div>
            <h2 className="text-xl font-semibold text-slate-900">Jobs</h2>
            <p className="mt-1 text-sm text-slate-500">Track scheduled work, status, and completed installations.</p>
          </div>
          <div className="rounded-2xl bg-slate-50 px-4 py-3 text-sm text-slate-600">
            {data?.length ?? 0} jobs loaded
          </div>
        </div>
      </div>

      <div className="overflow-hidden rounded-3xl border border-slate-200 bg-white shadow-sm">
        <table className="min-w-full divide-y divide-slate-200">
          <thead className="bg-slate-50">
            <tr>
              <th className="px-4 py-3 text-left text-xs font-semibold uppercase tracking-wider text-slate-500">Job</th>
              <th className="px-4 py-3 text-left text-xs font-semibold uppercase tracking-wider text-slate-500">Customer</th>
              <th className="px-4 py-3 text-left text-xs font-semibold uppercase tracking-wider text-slate-500">Status</th>
              <th className="px-4 py-3 text-left text-xs font-semibold uppercase tracking-wider text-slate-500">Due</th>
              <th className="px-4 py-3 text-left text-xs font-semibold uppercase tracking-wider text-slate-500">Value</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-200 bg-white">
            {data?.map((job) => (
              <tr key={job.id}>
                <td className="whitespace-nowrap px-4 py-4 text-sm text-slate-900">{job.title}</td>
                <td className="whitespace-nowrap px-4 py-4 text-sm text-slate-500">{job.customer_id}</td>
                <td className="whitespace-nowrap px-4 py-4 text-sm text-slate-900">{job.status}</td>
                <td className="whitespace-nowrap px-4 py-4 text-sm text-slate-500">
                  {job.scheduled_date ? new Date(job.scheduled_date).toLocaleDateString() : 'TBD'}
                </td>
                <td className="whitespace-nowrap px-4 py-4 text-sm text-slate-500">
                  {job.total_cost ? `$${(job.total_cost / 100).toLocaleString()}` : 'N/A'}
                </td>
              </tr>
            ))}
            {data?.length === 0 && (
              <tr>
                <td colSpan={5} className="px-4 py-6 text-center text-sm text-slate-500">
                  No jobs available yet.
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  )
}

export default Jobs
