import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import api from '../lib/api';
import { User, Token, LoginRequest } from '../types';

interface AuthContextType {
  user: User | null;
  adminEmail: string | null;
  login: (credentials: LoginRequest) => Promise<void>;
  adminLogin: (credentials: LoginRequest) => Promise<void>;
  logout: () => void;
  isLoading: boolean;
  isAdmin: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

interface AuthProviderProps {
  children: ReactNode;
}

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [adminEmail, setAdminEmail] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const token = localStorage.getItem('access_token');
    const authMode = localStorage.getItem('auth_mode');

    if (token) {
      const meEndpoint = authMode === 'admin' ? '/auth/admin/me' : '/auth/me';
      api.get(meEndpoint)
        .then((response) => {
          if (authMode === 'admin') {
            setAdminEmail(response.data.email);
            setUser(null);
          } else {
            setUser(response.data);
            setAdminEmail(null);
          }
        })
        .catch(() => {
          localStorage.removeItem('access_token');
          localStorage.removeItem('refresh_token');
          localStorage.removeItem('auth_mode');
        })
        .finally(() => setIsLoading(false));
    } else {
      setIsLoading(false);
    }
  }, []);

  const login = async (credentials: LoginRequest) => {
    const params = new URLSearchParams();
    params.append('username', credentials.username);
    params.append('password', credentials.password);

    const response = await api.post<Token>('/auth/access-token', params, {
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    });

    const { access_token, refresh_token } = response.data;
    localStorage.setItem('access_token', access_token);
    localStorage.setItem('refresh_token', refresh_token);
    localStorage.setItem('auth_mode', 'user');

    const userResponse = await api.get('/auth/me');
    setUser(userResponse.data);
    setAdminEmail(null);
  };

  const adminLogin = async (credentials: LoginRequest) => {
    const params = new URLSearchParams();
    params.append('username', credentials.username);
    params.append('password', credentials.password);

    const response = await api.post<Token>('/auth/admin-access-token', params, {
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    });

    const { access_token, refresh_token } = response.data;
    localStorage.setItem('access_token', access_token);
    localStorage.setItem('refresh_token', refresh_token);
    localStorage.setItem('auth_mode', 'admin');

    const adminResponse = await api.get('/auth/admin/me');
    setAdminEmail(adminResponse.data.email);
    setUser(null);
  };

  const logout = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('auth_mode');
    setUser(null);
    setAdminEmail(null);
  };

  const isAdmin = !!adminEmail;

  const value = {
    user,
    adminEmail,
    login,
    adminLogin,
    logout,
    isLoading,
    isAdmin,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export default AuthContext;