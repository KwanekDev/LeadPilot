import React, { useMemo } from 'react'
import { useQuery } from '@tanstack/react-query'
import api from '../lib/api'
import { Job, Reminder } from '../types'

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
      <div className="rounded-3xl border border-slate-200 bg-white p-8 shadow-sm text-center">
        <div className="mx-auto h-12 w-12 animate-spin rounded-full border-4 border-indigo-500 border-t-transparent"></div>
        <p className="mt-4 text-sm text-slate-600">Loading calendar events...</p>
      </div>
    )
  }

  if (error) {
    return (
      <div className="rounded-3xl border border-red-200 bg-red-50 p-8 shadow-sm text-center">
        <p className="text-sm font-medium text-red-700">Unable to load calendar events.</p>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
        <div className="flex flex-col gap-2 sm:flex-row sm:items-end sm:justify-between">
          <div>
            <h2 className="text-xl font-semibold text-slate-900">Calendar</h2>
            <p className="mt-1 text-sm text-slate-500">See upcoming jobs and reminders for this month.</p>
          </div>
          <div className="rounded-2xl bg-slate-50 px-4 py-3 text-sm text-slate-600">
            {today.toLocaleDateString(undefined, { month: 'long', year: 'numeric' })}
          </div>
        </div>

        <div className="mt-6 overflow-hidden rounded-3xl border border-slate-200">
          <div className="grid grid-cols-7 gap-px bg-slate-200 text-center text-xs uppercase tracking-wide text-slate-500">
            {dayNames.map((day) => (
              <div key={day} className="bg-white py-3">
                {day}
              </div>
            ))}
          </div>
          <div className="grid grid-cols-7 gap-px bg-slate-200">
            {calendarDays.map((date) => {
              const isCurrentMonth = date.getMonth() === month
              const dayKey = date.toISOString().slice(0, 10)
              const dayEvents = eventsByDate[dayKey] || []
              const isToday = date.toDateString() === today.toDateString()

              return (
                <div key={date.toISOString()} className="bg-white min-h-[120px] p-3">
                  <div className="flex items-start justify-between gap-2">
                    <p className={`text-sm font-semibold ${isCurrentMonth ? 'text-slate-900' : 'text-slate-400'}`}>
                      {date.getDate()}
                    </p>
                    {isToday && <span className="rounded-full bg-indigo-600 px-2 py-0.5 text-[11px] font-semibold text-white">Today</span>}
                  </div>
                  <div className="mt-3 space-y-1">
                    {dayEvents.slice(0, 2).map((event) => (
                      <div
                        key={event.id}
                        className={`rounded-2xl px-2 py-1 text-[11px] font-medium ${
                          event.type === 'Job' ? 'bg-emerald-100 text-emerald-800' : 'bg-amber-100 text-amber-900'
                        }`}
                      >
                        {event.type}: {event.title}
                      </div>
                    ))}
                    {dayEvents.length > 2 && (
                      <p className="text-[11px] text-slate-500">+{dayEvents.length - 2} more</p>
                    )}
                  </div>
                </div>
              )
            })}
          </div>
        </div>
      </div>

      <div className="grid gap-6 lg:grid-cols-[1fr_340px]">
        <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
          <h3 className="text-lg font-semibold text-slate-900">Upcoming events</h3>
          <div className="mt-5 space-y-4">
            {upcomingEvents.length === 0 ? (
              <p className="text-sm text-slate-500">No upcoming jobs or reminders scheduled.</p>
            ) : (
              upcomingEvents.map((event) => (
                <div key={event.id} className="rounded-3xl border border-slate-200 bg-slate-50 p-4">
                  <div className="flex items-center justify-between gap-4">
                    <div>
                      <p className="text-sm font-semibold text-slate-900">{event.title}</p>
                      <p className="text-sm text-slate-500">{event.subtitle}</p>
                    </div>
                    <span className="rounded-full bg-slate-100 px-3 py-1 text-xs font-semibold text-slate-700">
                      {formatDate(event.date)}
                    </span>
                  </div>
                  <p className="mt-3 text-xs uppercase tracking-wider text-slate-500">{event.type}</p>
                </div>
              ))
            )}
          </div>
        </div>

        <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
          <h3 className="text-lg font-semibold text-slate-900">Event summary</h3>
          <div className="mt-4 space-y-3 text-sm text-slate-600">
            <p>Total scheduled jobs: {jobsQuery.data?.filter((job) => job.scheduled_date).length || 0}</p>
            <p>Total active reminders: {remindersQuery.data?.filter((reminder) => reminder.is_active).length || 0}</p>
            <p>Events this month: {events.filter((event) => event.date.getMonth() === month).length}</p>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Calendar
