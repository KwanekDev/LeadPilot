import React from 'react'
import { useQuery } from '@tanstack/react-query'
import api from '../lib/api'
import { Reminder } from '../types'
import GlassCard from '../components/GlassCard'
import GlowBadge from '../components/GlowBadge'

const Reminders: React.FC = () => {
  const { data, isLoading, error } = useQuery<Reminder[]>({
    queryKey: ['reminders'],
    queryFn: async () => {
      const response = await api.get('/reminders')
      return response.data
    },
  })

  if (isLoading) {
    return (
      <GlassCard glow="blue" className="p-12 text-center">
        <div className="mx-auto h-12 w-12 animate-spin rounded-full border-4 border-cyan-500 border-t-transparent"></div>
        <p className="mt-6 text-light-secondary">Loading reminders...</p>
      </GlassCard>
    )
  }

  if (error) {
    return (
      <GlassCard className="p-12 text-center border-red-500/30">
        <p className="text-red-300 font-medium">❌ Unable to load reminders</p>
      </GlassCard>
    )
  }

  return (
    <div className="space-y-6 animate-slide-in-fade">
      <GlassCard glow="blue" className="p-6">
        <div className="flex flex-col gap-4 sm:flex-row sm:items-end sm:justify-between">
          <div>
            <h2 className="text-3xl font-bold text-light-primary">Reminders</h2>
            <p className="mt-2 text-light-secondary">Track and manage your active reminders</p>
          </div>
          <GlowBadge variant="cyan" size="md">
            {data?.length ?? 0} reminders
          </GlowBadge>
        </div>
      </GlassCard>

      <GlassCard glow="blue" className="p-6 overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="border-b border-slate-700/30">
                <th className="px-4 py-3 text-left text-xs font-semibold uppercase tracking-wider text-light-tertiary">Reminder</th>
                <th className="px-4 py-3 text-left text-xs font-semibold uppercase tracking-wider text-light-tertiary">Type</th>
                <th className="px-4 py-3 text-left text-xs font-semibold uppercase tracking-wider text-light-tertiary">Next Date</th>
                <th className="px-4 py-3 text-left text-xs font-semibold uppercase tracking-wider text-light-tertiary">Channel</th>
                <th className="px-4 py-3 text-left text-xs font-semibold uppercase tracking-wider text-light-tertiary">Status</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-700/20">
              {data?.map((reminder) => (
                <tr key={reminder.id} className="hover:bg-slate-700/20 transition-colors group">
                  <td className="px-4 py-4 text-sm text-light-primary font-medium group-hover:text-cyan-300 transition">
                    {reminder.title}
                  </td>
                  <td className="px-4 py-4 text-sm text-light-tertiary">{reminder.reminder_type}</td>
                  <td className="px-4 py-4 text-sm text-light-tertiary">
                    {reminder.next_reminder_date ? new Date(reminder.next_reminder_date).toLocaleDateString() : 'TBD'}
                  </td>
                  <td className="px-4 py-4 text-sm text-light-tertiary">{reminder.channel}</td>
                  <td className="px-4 py-4 text-sm">
                    <GlowBadge variant={reminder.is_active ? 'green' : 'red'} size="sm">
                      {reminder.is_active ? 'Active' : 'Inactive'}
                    </GlowBadge>
                  </td>
                </tr>
              ))}
              {data?.length === 0 && (
                <tr>
                  <td colSpan={5} className="px-4 py-8 text-center text-light-tertiary">
                    <div className="flex flex-col items-center gap-2">
                      <p className="text-lg">🔔</p>
                      <p>No reminders available yet</p>
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

export default Reminders

