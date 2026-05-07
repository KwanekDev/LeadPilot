import { useEffect, useState } from 'react'
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import api from '../lib/api'
import { TenantSettings } from '../types'

const Settings: React.FC = () => {
  const queryClient = useQueryClient()
  const { data: currentSettings, isLoading, error } = useQuery<TenantSettings>({
    queryKey: ['tenantSettings'],
    queryFn: async () => {
      const response = await api.get('/tenants/settings/me')
      return response.data
    },
  })

  const [form, setForm] = useState<Partial<TenantSettings>>({})
  const [successMessage, setSuccessMessage] = useState<string>('')

  useEffect(() => {
    if (currentSettings) {
      setForm(currentSettings)
    }
  }, [currentSettings])

  const updateSettings = useMutation<TenantSettings, Error, Partial<TenantSettings>>({
    mutationFn: async (values: Partial<TenantSettings>) => {
      const response = await api.put('/tenants/settings/me', values)
      return response.data
    },
    onSuccess: (data: TenantSettings) => {
      queryClient.setQueryData(['tenantSettings'], data)
      setForm(data)
      setSuccessMessage('Tenant settings saved successfully.')
    },
  })

  const handleChange = (field: keyof Partial<TenantSettings>, value: string | boolean | number | undefined) => {
    setForm((prev) => ({ ...prev, [field]: value }))
  }

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault()
    setSuccessMessage('')

    const payload: Partial<TenantSettings> = {
      name: form.name,
      domain: form.domain,
      logo_url: form.logo_url,
      timezone: form.timezone,
      business_hours_start: form.business_hours_start,
      business_hours_end: form.business_hours_end,
      smtp_server: form.smtp_server,
      smtp_port: form.smtp_port,
      smtp_username: form.smtp_username,
      smtp_password: form.smtp_password,
      smtp_from_email: form.smtp_from_email,
      smtp_tls: form.smtp_tls,
      lead_capture_slug: form.lead_capture_slug,
      lead_capture_enabled: form.lead_capture_enabled,
    }

    updateSettings.mutate(payload)
  }

  if (isLoading) {
    return (
      <div className="rounded-3xl border border-slate-200 bg-white p-8 shadow-sm text-center">
        <div className="mx-auto h-12 w-12 animate-spin rounded-full border-4 border-indigo-500 border-t-transparent"></div>
        <p className="mt-4 text-sm text-slate-600">Loading tenant settings...</p>
      </div>
    )
  }

  if (error) {
    return (
      <div className="rounded-3xl border border-red-200 bg-red-50 p-8 shadow-sm text-center">
        <p className="text-sm font-medium text-red-700">Unable to load tenant settings.</p>
      </div>
    )
  }

  const publicFormUrl = form.lead_capture_slug
    ? `${import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1'}/public/form/${form.lead_capture_slug}`
    : ''

  return (
    <div className="space-y-6">
      <div className="rounded-3xl border border-slate-200 bg-white p-8 shadow-sm">
        <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
          <div>
            <h2 className="text-2xl font-semibold text-slate-900">Tenant Settings</h2>
            <p className="mt-2 text-sm text-slate-500">Manage company-wide settings, SMTP, and public lead capture.</p>
          </div>
          <div className="rounded-2xl bg-slate-50 px-4 py-3 text-sm text-slate-600">
            Tenant ID: {currentSettings?.id}
          </div>
        </div>
      </div>

      <form onSubmit={handleSubmit} className="grid gap-6">
        <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
          <h3 className="text-lg font-semibold text-slate-900">Basic tenant details</h3>
          <div className="mt-6 grid gap-6 lg:grid-cols-2">
            <label className="space-y-2">
              <span className="text-sm font-medium text-slate-700">Company Name</span>
              <input
                value={form.name || ''}
                onChange={(event) => handleChange('name', event.target.value)}
                className="w-full rounded-3xl border border-slate-200 bg-slate-50 px-4 py-3 text-sm text-slate-900 focus:border-indigo-500 focus:outline-none"
                placeholder="Your company name"
                required
              />
            </label>
            <label className="space-y-2">
              <span className="text-sm font-medium text-slate-700">Domain</span>
              <input
                value={form.domain || ''}
                onChange={(event) => handleChange('domain', event.target.value)}
                className="w-full rounded-3xl border border-slate-200 bg-slate-50 px-4 py-3 text-sm text-slate-900 focus:border-indigo-500 focus:outline-none"
                placeholder="example.com"
              />
            </label>
            <label className="space-y-2">
              <span className="text-sm font-medium text-slate-700">Timezone</span>
              <input
                value={form.timezone || ''}
                onChange={(event) => handleChange('timezone', event.target.value)}
                className="w-full rounded-3xl border border-slate-200 bg-slate-50 px-4 py-3 text-sm text-slate-900 focus:border-indigo-500 focus:outline-none"
                placeholder="UTC"
              />
            </label>
            <div className="grid gap-6 sm:grid-cols-2">
              <label className="space-y-2">
                <span className="text-sm font-medium text-slate-700">Business hours start</span>
                <input
                  type="time"
                  value={form.business_hours_start || '09:00'}
                  onChange={(event) => handleChange('business_hours_start', event.target.value)}
                  className="w-full rounded-3xl border border-slate-200 bg-slate-50 px-4 py-3 text-sm text-slate-900 focus:border-indigo-500 focus:outline-none"
                />
              </label>
              <label className="space-y-2">
                <span className="text-sm font-medium text-slate-700">Business hours end</span>
                <input
                  type="time"
                  value={form.business_hours_end || '17:00'}
                  onChange={(event) => handleChange('business_hours_end', event.target.value)}
                  className="w-full rounded-3xl border border-slate-200 bg-slate-50 px-4 py-3 text-sm text-slate-900 focus:border-indigo-500 focus:outline-none"
                />
              </label>
            </div>
          </div>
        </div>

        <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
          <h3 className="text-lg font-semibold text-slate-900">SMTP settings</h3>
          <p className="mt-2 text-sm text-slate-500">Optional mail server configuration for tenant email sending.</p>
          <div className="mt-6 grid gap-6 lg:grid-cols-2">
            <label className="space-y-2">
              <span className="text-sm font-medium text-slate-700">SMTP Server</span>
              <input
                value={form.smtp_server || ''}
                onChange={(event) => handleChange('smtp_server', event.target.value)}
                className="w-full rounded-3xl border border-slate-200 bg-slate-50 px-4 py-3 text-sm text-slate-900 focus:border-indigo-500 focus:outline-none"
                placeholder="smtp.mailserver.com"
              />
            </label>
            <label className="space-y-2">
              <span className="text-sm font-medium text-slate-700">SMTP Port</span>
              <input
                type="number"
                value={form.smtp_port ?? ''}
                onChange={(event) => handleChange('smtp_port', event.target.value ? Number(event.target.value) : undefined)}
                className="w-full rounded-3xl border border-slate-200 bg-slate-50 px-4 py-3 text-sm text-slate-900 focus:border-indigo-500 focus:outline-none"
                placeholder="587"
              />
            </label>
            <label className="space-y-2">
              <span className="text-sm font-medium text-slate-700">SMTP Username</span>
              <input
                value={form.smtp_username || ''}
                onChange={(event) => handleChange('smtp_username', event.target.value)}
                className="w-full rounded-3xl border border-slate-200 bg-slate-50 px-4 py-3 text-sm text-slate-900 focus:border-indigo-500 focus:outline-none"
                placeholder="username"
              />
            </label>
            <label className="space-y-2">
              <span className="text-sm font-medium text-slate-700">SMTP Password</span>
              <input
                type="password"
                value={form.smtp_password || ''}
                onChange={(event) => handleChange('smtp_password', event.target.value)}
                className="w-full rounded-3xl border border-slate-200 bg-slate-50 px-4 py-3 text-sm text-slate-900 focus:border-indigo-500 focus:outline-none"
                placeholder="••••••••"
              />
            </label>
            <label className="space-y-2 lg:col-span-2">
              <span className="text-sm font-medium text-slate-700">From email</span>
              <input
                type="email"
                value={form.smtp_from_email || ''}
                onChange={(event) => handleChange('smtp_from_email', event.target.value)}
                className="w-full rounded-3xl border border-slate-200 bg-slate-50 px-4 py-3 text-sm text-slate-900 focus:border-indigo-500 focus:outline-none"
                placeholder="no-reply@example.com"
              />
            </label>
            <label className="inline-flex items-center gap-3 rounded-3xl border border-slate-200 bg-slate-50 px-4 py-3 text-sm text-slate-700">
              <input
                type="checkbox"
                checked={Boolean(form.smtp_tls)}
                onChange={(event) => handleChange('smtp_tls', event.target.checked)}
                className="h-4 w-4 rounded border-slate-300 text-indigo-600 focus:ring-indigo-500"
              />
              Use TLS for SMTP
            </label>
          </div>
        </div>

        <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
          <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
            <div>
              <h3 className="text-lg font-semibold text-slate-900">Public lead capture</h3>
              <p className="mt-2 text-sm text-slate-500">Enable a tenant-specific public lead capture form with a custom slug.</p>
            </div>
            <div className="rounded-2xl bg-slate-50 px-4 py-3 text-sm text-slate-600">
              {form.lead_capture_enabled ? 'Enabled' : 'Disabled'}
            </div>
          </div>
          <div className="mt-6 grid gap-6 lg:grid-cols-2">
            <label className="space-y-2">
              <span className="text-sm font-medium text-slate-700">Form slug</span>
              <input
                value={form.lead_capture_slug || ''}
                onChange={(event) => handleChange('lead_capture_slug', event.target.value)}
                className="w-full rounded-3xl border border-slate-200 bg-slate-50 px-4 py-3 text-sm text-slate-900 focus:border-indigo-500 focus:outline-none"
                placeholder="my-business-leads"
              />
            </label>
            <label className="inline-flex items-center gap-3 rounded-3xl border border-slate-200 bg-slate-50 px-4 py-3 text-sm text-slate-700">
              <input
                type="checkbox"
                checked={Boolean(form.lead_capture_enabled)}
                onChange={(event) => handleChange('lead_capture_enabled', event.target.checked)}
                className="h-4 w-4 rounded border-slate-300 text-indigo-600 focus:ring-indigo-500"
              />
              Enable public lead capture
            </label>
          </div>
          {form.lead_capture_enabled && form.lead_capture_slug && (
            <div className="mt-6 rounded-3xl bg-slate-50 p-4 text-sm text-slate-700">
              <p className="font-medium text-slate-900">Public endpoint</p>
              <p className="mt-2 break-all text-indigo-700">{publicFormUrl}</p>
              <p className="mt-3 text-slate-500">Use this endpoint to submit captured leads from an external form.</p>
            </div>
          )}
        </div>

        <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
          <div>
            {successMessage && <p className="text-sm font-medium text-emerald-700">{successMessage}</p>}
            {updateSettings.isError && (
              <p className="text-sm font-medium text-red-700">Failed to save tenant settings. Please try again.</p>
            )}
          </div>
          <button
            type="submit"
            disabled={updateSettings.isPending}
            className="inline-flex items-center justify-center rounded-3xl bg-indigo-600 px-6 py-3 text-sm font-semibold text-white shadow-sm transition hover:bg-indigo-700 disabled:cursor-not-allowed disabled:bg-slate-400"
          >
            {updateSettings.isPending ? 'Saving...' : 'Save changes'}
          </button>
        </div>
      </form>
    </div>
  )
}

export default Settings
