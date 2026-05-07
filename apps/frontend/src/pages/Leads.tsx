import React from 'react'
import { useQuery } from '@tanstack/react-query'
import api from '../lib/api'
import { Lead } from '../types'
import GlassCard from '../components/GlassCard'
import GlowBadge from '../components/GlowBadge'

const statusColors = {
  'new': 'blue',
  'contacted': 'cyan',
  'in-conversation': 'purple',
  'waiting-reply': 'yellow',
  'converted': 'green',
  'lost': 'red',
} as Record<string, 'blue' | 'cyan' | 'purple' | 'yellow' | 'green' | 'red'>

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
      <GlassCard glow="blue" className="p-12 text-center">
        <div className="mx-auto h-12 w-12 animate-spin rounded-full border-4 border-cyan-500 border-t-transparent"></div>
        <p className="mt-6 text-light-secondary">Loading your leads...</p>
      </GlassCard>
    )
  }

  if (error) {
    return (
      <GlassCard className="p-12 text-center border-red-500/30">
        <p className="text-red-300 font-medium">❌ Unable to load leads</p>
      </GlassCard>
    )
  }

  return (
    <div className="space-y-6 animate-slide-in-fade">
      {/* Header */}
      <GlassCard glow="blue" className="p-6">
        <div className="flex flex-col gap-4 sm:flex-row sm:items-end sm:justify-between">
          <div>
            <h2 className="text-3xl font-bold text-light-primary">Leads Pipeline</h2>
            <p className="mt-2 text-light-secondary">Manage and track your lead pipeline in real-time</p>
          </div>
          <GlowBadge variant="cyan" size="md">
            {data?.length ?? 0} leads
          </GlowBadge>
        </div>
      </GlassCard>

      {/* Leads Table */}
      <GlassCard glow="blue" className="p-6 overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="border-b border-slate-700/30">
                <th className="px-4 py-3 text-left text-xs font-semibold uppercase tracking-wider text-light-tertiary">Lead Name</th>
                <th className="px-4 py-3 text-left text-xs font-semibold uppercase tracking-wider text-light-tertiary">Contact</th>
                <th className="px-4 py-3 text-left text-xs font-semibold uppercase tracking-wider text-light-tertiary">Status</th>
                <th className="px-4 py-3 text-left text-xs font-semibold uppercase tracking-wider text-light-tertiary">Source</th>
                <th className="px-4 py-3 text-left text-xs font-semibold uppercase tracking-wider text-light-tertiary">Created</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-700/20">
              {data?.map((lead) => (
                <tr
                  key={lead.id}
                  className="hover:bg-slate-700/20 transition-colors group cursor-pointer"
                >
                  <td className="px-4 py-4 text-sm text-light-primary font-medium group-hover:text-cyan-300 transition">
                    {lead.first_name || ''} {lead.last_name || ''}
                  </td>
                  <td className="px-4 py-4 text-sm text-light-tertiary">
                    {lead.email ?? '—'} · {lead.phone ?? '—'}
                  </td>
                  <td className="px-4 py-4 text-sm">
                    <GlowBadge
                      variant={statusColors[lead.status?.toLowerCase().replace(/ /g, '-')] || 'blue'}
                      size="sm"
                    >
                      {lead.status}
                    </GlowBadge>
                  </td>
                  <td className="px-4 py-4 text-sm text-light-tertiary">{lead.source ?? 'Unknown'}</td>
                  <td className="px-4 py-4 text-sm text-light-tertiary">
                    {new Date(lead.created_at).toLocaleDateString()}
                  </td>
                </tr>
              ))}
              {data?.length === 0 && (
                <tr>
                  <td colSpan={5} className="px-4 py-8 text-center text-light-tertiary">
                    <div className="flex flex-col items-center gap-2">
                      <p className="text-lg">👥</p>
                      <p>No leads available yet</p>
                      <p className="text-xs">Start adding leads to see them here</p>
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

export default Leads
