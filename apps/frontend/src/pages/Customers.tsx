import React from 'react'
import { useQuery } from '@tanstack/react-query'
import api from '../lib/api'
import { Customer } from '../types'

const Customers: React.FC = () => {
  const { data, isLoading, error } = useQuery<Customer[]>({
    queryKey: ['customers'],
    queryFn: async () => {
      const response = await api.get('/customers')
      return response.data
    },
  })

  if (isLoading) {
    return (
      <div className="rounded-3xl border border-slate-200 bg-white p-8 shadow-sm text-center">
        <div className="mx-auto h-12 w-12 animate-spin rounded-full border-4 border-indigo-500 border-t-transparent"></div>
        <p className="mt-4 text-sm text-slate-600">Loading customers...</p>
      </div>
    )
  }

  if (error) {
    return (
      <div className="rounded-3xl border border-red-200 bg-red-50 p-8 shadow-sm text-center">
        <p className="text-sm font-medium text-red-700">Unable to load customers.</p>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
        <div className="flex flex-col gap-2 sm:flex-row sm:items-end sm:justify-between">
          <div>
            <h2 className="text-xl font-semibold text-slate-900">Customers</h2>
            <p className="mt-1 text-sm text-slate-500">Customer information for your services and warranty records.</p>
          </div>
          <div className="rounded-2xl bg-slate-50 px-4 py-3 text-sm text-slate-600">
            {data?.length ?? 0} customers loaded
          </div>
        </div>
      </div>

      <div className="overflow-hidden rounded-3xl border border-slate-200 bg-white shadow-sm">
        <table className="min-w-full divide-y divide-slate-200">
          <thead className="bg-slate-50">
            <tr>
              <th className="px-4 py-3 text-left text-xs font-semibold uppercase tracking-wider text-slate-500">Customer</th>
              <th className="px-4 py-3 text-left text-xs font-semibold uppercase tracking-wider text-slate-500">Contact</th>
              <th className="px-4 py-3 text-left text-xs font-semibold uppercase tracking-wider text-slate-500">Installed</th>
              <th className="px-4 py-3 text-left text-xs font-semibold uppercase tracking-wider text-slate-500">Warranty</th>
              <th className="px-4 py-3 text-left text-xs font-semibold uppercase tracking-wider text-slate-500">Status</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-200 bg-white">
            {data?.map((customer) => (
              <tr key={customer.id}>
                <td className="whitespace-nowrap px-4 py-4 text-sm text-slate-900">
                  {customer.first_name || ''} {customer.last_name || ''}
                </td>
                <td className="whitespace-nowrap px-4 py-4 text-sm text-slate-500">
                  {customer.email ?? '—'} · {customer.phone ?? '—'}
                </td>
                <td className="whitespace-nowrap px-4 py-4 text-sm text-slate-900">{customer.equipment_installed ?? 'N/A'}</td>
                <td className="whitespace-nowrap px-4 py-4 text-sm text-slate-500">{customer.warranty_expiration ? new Date(customer.warranty_expiration).toLocaleDateString() : 'N/A'}</td>
                <td className="whitespace-nowrap px-4 py-4 text-sm text-slate-500">{customer.is_active ? 'Active' : 'Inactive'}</td>
              </tr>
            ))}
            {data?.length === 0 && (
              <tr>
                <td colSpan={5} className="px-4 py-6 text-center text-sm text-slate-500">
                  No customers available yet.
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  )
}

export default Customers
