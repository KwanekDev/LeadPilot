import React, { useState, useEffect } from 'react'
import api from '../lib/api'
import { User } from '../types'

const Admin: React.FC = () => {
  const [users, setUsers] = useState<User[]>([])
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')

  const [newUserEmail, setNewUserEmail] = useState('')
  const [newUserPassword, setNewUserPassword] = useState('')
  const [resetPassword, setResetPassword] = useState('')
  const [resetUserId, setResetUserId] = useState<number | null>(null)

  useEffect(() => {
    fetchUsers()
  }, [])

  const fetchUsers = async () => {
    try {
      const response = await api.get('/admin/users')
      setUsers(response.data)
    } catch (err: any) {
      setError('Błąd podczas pobierania listy użytkowników')
    }
  }

  const handleCreateUser = async (e: React.FormEvent) => {
    e.preventDefault()
    setIsLoading(true)
    setError('')
    setSuccess('')

    try {
      await api.post('/admin/users', {
        email: newUserEmail,
        password: newUserPassword,
      })
      setSuccess('Konto klienta utworzone pomyślnie. Klient może się teraz zalogować.')
      setNewUserEmail('')
      setNewUserPassword('')
      fetchUsers()
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Nie udało się utworzyć użytkownika')
    } finally {
      setIsLoading(false)
    }
  }

  const generatePassword = () => {
    const chars = 'ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz23456789!@#$%*'
    const generated = Array.from({ length: 16 }, () => chars[Math.floor(Math.random() * chars.length)]).join('')
    setNewUserPassword(generated)
  }

  const handleDeleteUser = async (userId: number) => {
    if (!window.confirm('Czy na pewno chcesz usunąć to konto?')) return
    try {
      await api.delete(`/admin/users/${userId}`)
      setSuccess('Użytkownik usunięty')
      fetchUsers()
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Błąd usuwania użytkownika')
    }
  }

  const handleResetPassword = async (userId: number) => {
    if (!resetPassword) {
      setError('Wprowadź nowe hasło przed resetem')
      return
    }
    try {
      await api.put(`/admin/users/${userId}/reset-password`, { password: resetPassword })
      setSuccess('Hasło użytkownika zostało zresetowane')
      setResetPassword('')
      setResetUserId(null)
      fetchUsers()
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Błąd resetowania hasła')
    }
  }

  return (
    <div className="min-h-screen bg-slate-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-6xl mx-auto">
        <div className="bg-white rounded-3xl shadow-sm border border-slate-200 overflow-hidden">
          <div className="bg-slate-900 px-8 py-6">
            <h1 className="text-xl font-bold text-white">Panel Administracyjny</h1>
            <p className="text-slate-400 text-sm">Zarządzanie kontami klientów</p>
          </div>

          <div className="p-8">
            {error && <div className="mb-6 p-4 bg-red-50 border-l-4 border-red-500 text-red-700 rounded-r-md">{error}</div>}
            {success && <div className="mb-6 p-4 bg-green-50 border-l-4 border-green-500 text-green-700 rounded-r-md">{success}</div>}

            <section className="mb-12">
              <h2 className="text-lg font-bold text-slate-900 mb-6 flex items-center gap-2">
                <span className="w-8 h-8 bg-indigo-100 text-indigo-600 rounded-lg flex items-center justify-center text-sm">01</span>
                Dodaj Nowego Klienta
              </h2>
              <form onSubmit={handleCreateUser} className="grid grid-cols-1 md:grid-cols-2 gap-4 bg-slate-50 p-6 rounded-2xl border border-slate-100">
                <input
                  type="email"
                  placeholder="Email klienta"
                  value={newUserEmail}
                  onChange={(e) => setNewUserEmail(e.target.value)}
                  required
                  className="px-4 py-2 border border-slate-200 rounded-xl outline-none focus:ring-2 focus:ring-indigo-500"
                />
                <input
                  type="password"
                  placeholder="Hasło"
                  value={newUserPassword}
                  onChange={(e) => setNewUserPassword(e.target.value)}
                  required
                  className="px-4 py-2 border border-slate-200 rounded-xl outline-none focus:ring-2 focus:ring-indigo-500"
                />
                <button
                  type="button"
                  onClick={generatePassword}
                  className="bg-slate-100 text-slate-700 font-semibold py-2 rounded-xl hover:bg-slate-200 transition-all"
                >
                  Generate Password
                </button>
                <button
                  type="submit"
                  disabled={isLoading}
                  className="md:col-span-2 bg-indigo-600 text-white font-semibold py-3 rounded-xl hover:bg-indigo-700 disabled:opacity-50 transition-all"
                >
                  {isLoading ? 'Tworzenie konta...' : 'Utwórz konto klienta'}
                </button>
              </form>
            </section>

            <section>
              <h2 className="text-lg font-bold text-slate-900 mb-6 flex items-center gap-2">
                <span className="w-8 h-8 bg-indigo-100 text-indigo-600 rounded-lg flex items-center justify-center text-sm">02</span>
                Lista Klientów
              </h2>
              <div className="overflow-x-auto border border-slate-100 rounded-2xl">
                <table className="min-w-full divide-y divide-slate-200">
                  <thead className="bg-slate-50">
                    <tr>
                      <th className="px-6 py-4 text-left text-xs font-bold text-slate-500 uppercase">Użytkownik</th>
                      <th className="px-6 py-4 text-left text-xs font-bold text-slate-500 uppercase">Status</th>
                      <th className="px-6 py-4 text-left text-xs font-bold text-slate-500 uppercase">Akcje</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-100">
                    {users.map((user) => (
                      <tr key={user.id} className="hover:bg-slate-50 transition-colors">
                        <td className="px-6 py-4">
                          <div className="text-sm font-semibold text-slate-900">{user.first_name || 'Client account'}</div>
                          <div className="text-xs text-slate-500">{user.email}</div>
                        </td>
                        <td className="px-6 py-4">
                          <span className={`px-3 py-1 rounded-full text-xs font-bold ${user.is_active ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'}`}>
                            {user.is_active ? 'AKTYWNY' : 'NIEAKTYWNY'}
                          </span>
                        </td>
                        <td className="px-6 py-4">
                          <div className="flex items-center gap-3">
                            <button
                              onClick={() => handleDeleteUser(user.id)}
                              className="text-sm font-bold text-red-600 hover:text-red-800"
                            >
                              Usuń
                            </button>
                            <button
                              onClick={() => setResetUserId(user.id)}
                              className="text-sm font-bold text-indigo-600 hover:text-indigo-800"
                            >
                              Reset hasła
                            </button>
                          </div>
                          {resetUserId === user.id && (
                            <div className="mt-3 flex items-center gap-2">
                              <input
                                type="password"
                                placeholder="Nowe hasło (min. 12 znaków)"
                                value={resetPassword}
                                onChange={(e) => setResetPassword(e.target.value)}
                                className="px-3 py-2 border border-slate-200 rounded-lg outline-none focus:ring-2 focus:ring-indigo-500"
                              />
                              <button
                                onClick={() => handleResetPassword(user.id)}
                                className="px-3 py-2 text-sm rounded-lg bg-indigo-600 text-white hover:bg-indigo-700"
                              >
                                Zapisz
                              </button>
                            </div>
                          )}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </section>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Admin