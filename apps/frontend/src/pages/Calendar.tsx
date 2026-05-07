import React, { useMemo } from 'react'
import { useQuery } from '@tanstack/react-query'
import api from '../lib/api'
import { Job, Reminder } from '../types'
import GlassCard from '../components/GlassCard'
import GlowBadge from '../components/GlowBadge'

interface CalendarEvent {
  id: string
  title: string
  type: 'Job' | 'Reminder'
  date: Date
  subtitle: string
}

const dayNames = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']

const formatDate = (date: Date) => date.toLocaleDateString(undefined, { month: 'short', day: 'numeric' })

const Calendar: React.FC = () => {
  const jobsQuery = useQuery<Job[]>({
    queryKey: ['jobs'],
    queryFn: async () => {
      const response = await api.get('/jobs')
      return response.data
    },
  })

  const remindersQuery = useQuery<Reminder[]>({
    queryKey: ['reminders'],
    queryFn: async () => {
      const response = await api.get('/reminders')
      return response.data
    },
  })

  const loading = jobsQuery.isLoading || remindersQuery.isLoading
  const error = jobsQuery.error || remindersQuery.error

  const events = useMemo(() => {
    const items: CalendarEvent[] = []

    jobsQuery.data?.forEach((job) => {
      if (!job.scheduled_date) return
      items.push({
        id: `job-${job.id}`,
        title: job.title,
        type: 'Job',
        date: new Date(job.scheduled_date),
        subtitle: job.status,
      })
    })

    remindersQuery.data?.forEach((reminder) => {
      if (!reminder.next_reminder_date) return
      items.push({
        id: `reminder-${reminder.id}`,
        title: reminder.title,
        type: 'Reminder',
        date: new Date(reminder.next_reminder_date),
        subtitle: reminder.reminder_type,
      })
    })

    return items.sort((a, b) => a.date.getTime() - b.date.getTime())
  }, [jobsQuery.data, remindersQuery.data])

  const today = new Date()
  const year = today.getFullYear()
  const month = today.getMonth()
  const firstOfMonth = new Date(year, month, 1)
  const startDate = new Date(firstOfMonth)
  startDate.setDate(firstOfMonth.getDate() - firstOfMonth.getDay())

  const calendarDays = useMemo(() => {
    return Array.from({ length: 42 }).map((_, index) => {
      const date = new Date(startDate)
      date.setDate(startDate.getDate() + index)
      return date
    })
  }, [startDate])

  const eventsByDate = useMemo(() => {
    return events.reduce<Record<string, CalendarEvent[]>>((acc, event) => {
      const key = event.date.toISOString().slice(0, 10)
      acc[key] = acc[key] ? [...acc[key], event] : [event]
      return acc
    }, {})
  }, [events])

  const upcomingEvents = events.filter((event) => event.date >= today).slice(0, 12)

  if (loading) {
    return (
      <GlassCard glow="blue" className="p-12 text-center">
        <div className="mx-auto h-12 w-12 animate-spin rounded-full border-4 border-cyan-500 border-t-transparent"></div>
        <p className="mt-6 text-light-secondary">Loading calendar events...</p>
      </GlassCard>
    )
  }

  if (error) {
    return (
      <GlassCard className="p-12 text-center border-red-500/30">
        <p className="text-red-300 font-medium">❌ Unable to load calendar events</p>
      </GlassCard>
    )
  }

  return (
    <div className="space-y-6 animate-slide-in-fade">
      {/* Header */}
      <GlassCard glow="blue" className="p-6">
        <div className="flex flex-col gap-4 sm:flex-row sm:items-end sm:justify-between">
          <div>
            <h2 className="text-3xl font-bold text-light-primary">Calendar</h2>
            <p className="mt-2 text-light-secondary">View your scheduled jobs and reminders</p>
          </div>
          <GlowBadge variant="cyan">
            {today.toLocaleDateString(undefined, { month: 'short', year: 'numeric' })}
          </GlowBadge>
        </div>
      </GlassCard>

      {/* Calendar Grid */}
      <GlassCard glow="blue" className="p-6">
        <div className="grid grid-cols-7 gap-px bg-slate-700/20 rounded-lg overflow-hidden">
          {dayNames.map((day) => (
            <div key={day} className="glass-panel bg-slate-700/10 py-3 px-2 text-center">
              <p className="text-xs font-bold uppercase text-light-tertiary">{day}</p>
            </div>
          ))}
        </div>
        <div className="grid grid-cols-7 gap-1 mt-4">
          {calendarDays.map((date) => {
            const isCurrentMonth = date.getMonth() === month
            const dayKey = date.toISOString().slice(0, 10)
            const dayEvents = eventsByDate[dayKey] || []
            const isToday = date.toDateString() === today.toDateString()

            return (
              <div key={date.toISOString()} className="glass-panel p-2 min-h-24">
                <div className="flex items-start justify-between gap-1">
                  <p className={`text-xs font-bold ${isCurrentMonth ? 'text-light-primary' : 'text-light-tertiary/50'}`}>
                    {date.getDate()}
                  </p>
                  {isToday && (
                    <GlowBadge variant="cyan" size="sm">
                      Today
                    </GlowBadge>
                  )}
                </div>
                <div className="mt-2 space-y-1">
                  {dayEvents.slice(0, 2).map((event) => (
                    <div
                      key={event.id}
                      className={`rounded px-1.5 py-0.5 text-[10px] font-medium ${
                        event.type === 'Job'
                          ? 'bg-green-500/20 text-green-300'
                          : 'bg-amber-500/20 text-amber-300'
                      }`}
                    >
                      {event.title.substring(0, 12)}...
                    </div>
                  ))}
                  {dayEvents.length > 2 && (
                    <p className="text-[10px] text-light-tertiary">+{dayEvents.length - 2}</p>
                  )}
                </div>
              </div>
            )
          })}
        </div>
      </GlassCard>

      {/* Upcoming Events */}
      <div className="grid gap-6 lg:grid-cols-[1fr_340px]">
        <GlassCard glow="cyan" className="p-6">
          <h3 className="text-xl font-bold text-light-primary mb-4">Upcoming Events</h3>
          <div className="space-y-3">
            {upcomingEvents.length === 0 ? (
              <p className="text-light-tertiary text-sm">No upcoming jobs or reminders</p>
            ) : (
              upcomingEvents.map((event) => (
                <div key={event.id} className="glass-panel p-4">
                  <div className="flex items-center justify-between gap-4">
                    <div>
                      <p className="font-semibold text-light-primary text-sm">{event.title}</p>
                      <p className="text-light-tertiary text-xs mt-1">{event.subtitle}</p>
                    </div>
                    <GlowBadge variant={event.type === 'Job' ? 'green' : 'yellow'} size="sm">
                      {formatDate(event.date)}
                    </GlowBadge>
                  </div>
                </div>
              ))
            )}
          </div>
        </GlassCard>

        <GlassCard glow="purple" className="p-6 h-fit">
          <h3 className="text-lg font-bold text-light-primary mb-4">Summary</h3>
          <div className="space-y-3 text-sm">
            <div className="glass-panel p-3">
              <p className="text-light-tertiary text-xs">Jobs Scheduled</p>
              <p className="text-2xl font-bold text-light-primary mt-1">
                {jobsQuery.data?.filter((job) => job.scheduled_date).length || 0}
              </p>
            </div>
            <div className="glass-panel p-3">
              <p className="text-light-tertiary text-xs">Active Reminders</p>
              <p className="text-2xl font-bold text-light-primary mt-1">
                {remindersQuery.data?.filter((reminder) => reminder.is_active).length || 0}
              </p>
            </div>
            <div className="glass-panel p-3">
              <p className="text-light-tertiary text-xs">Events This Month</p>
              <p className="text-2xl font-bold text-light-primary mt-1">
                {events.filter((event) => event.date.getMonth() === month).length}
              </p>
            </div>
          </div>
        </GlassCard>
      </div>
    </div>
  )
}

export default Calendar

