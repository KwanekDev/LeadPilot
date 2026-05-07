import React from 'react'
import { useQuery } from '@tanstack/react-query'
import api from '../lib/api'
import { Lead } from '../types'

const Leads: React.FC = () => {
  const { data, isLoading, error } = useQuery<Lead[]>({
    queryKey: ['leads'],
    queryFn: async () => {
      const response = await api.get('/leads')
      return response.data
    },
  })

  if (isLoading) {
    return (
      <div className="rounded-3xl border border-slate-200 bg-white p-8 shadow-sm text-center">
        <div className="mx-auto h-12 w-12 animate-spin rounded-full border-4 border-indigo-500 border-t-transparent"></div>
        <p className="mt-4 text-sm text-slate-600">Loading leads...</p>
      </div>
    )
  }

  if (error) {
    return (
      <div className="rounded-3xl border border-red-200 bg-red-50 p-8 shadow-sm text-center">
        <p className="text-sm font-medium text-red-700">Unable to load leads.</p>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
        <div className="flex flex-col gap-2 sm:flex-row sm:items-end sm:justify-between">
          <div>
            <h2 className="text-xl font-semibold text-slate-900">Leads</h2>
            <p className="mt-1 text-sm text-slate-500">Manage and review lead records for your team.</p>
          </div>
          <div className="rounded-2xl bg-slate-50 px-4 py-3 text-sm text-slate-600">
            {data?.length ?? 0} leads loaded
          </div>
        </div>
      </div>

      <div className="overflow-hidden rounded-3xl border border-slate-200 bg-white shadow-sm">
        <table className="min-w-full divide-y divide-slate-200">
          <thead className="bg-slate-50">
            <tr>
              <th className="px-4 py-3 text-left text-xs font-semibold uppercase tracking-wider text-slate-500">Lead</th>
              <th className="px-4 py-3 text-left text-xs font-semibold uppercase tracking-wider text-slate-500">Contact</th>
              <th className="px-4 py-3 text-left text-xs font-semibold uppercase tracking-wider text-slate-500">Status</th>
              <th className="px-4 py-3 text-left text-xs font-semibold uppercase tracking-wider text-slate-500">Source</th>
              <th className="px-4 py-3 text-left text-xs font-semibold uppercase tracking-wider text-slate-500">Created</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-200 bg-white">
            {data?.map((lead) => (
              <tr key={lead.id}>
                <td className="whitespace-nowrap px-4 py-4 text-sm text-slate-900">
                  {lead.first_name || ''} {lead.last_name || ''}
                </td>
                <td className="whitespace-nowrap px-4 py-4 text-sm text-slate-500">
                  {lead.email ?? '—'} · {lead.phone ?? '—'}
                </td>
                <td className="whitespace-nowrap px-4 py-4 text-sm text-slate-900">{lead.status}</td>
                <td className="whitespace-nowrap px-4 py-4 text-sm text-slate-500">{lead.source ?? 'Unknown'}</td>
                <td className="whitespace-nowrap px-4 py-4 text-sm text-slate-500">
                  {new Date(lead.created_at).toLocaleDateString()}
                </td>
              </tr>
            ))}
            {data?.length === 0 && (
              <tr>
                <td colSpan={5} className="px-4 py-6 text-center text-sm text-slate-500">
                  No leads available yet.
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  )
}

export default Leads
