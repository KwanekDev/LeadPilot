// API Types
export interface User {
  id: number;
  email: string;
  first_name?: string;
  last_name?: string;
  is_active: boolean;
  role: string;
  tenant_id?: number;
}

export interface Lead {
  id: number;
  tenant_id: number;
  first_name?: string;
  last_name?: string;
  email?: string;
  phone?: string;
  address?: string;
  status: string;
  source?: string;
  notes?: string;
  estimated_value?: number;
  assigned_to_id?: number;
  created_at: string;
  updated_at?: string;
}

export interface Customer {
  id: number;
  tenant_id: number;
  first_name?: string;
  last_name?: string;
  email?: string;
  phone?: string;
  address?: string;
  equipment_installed?: string;
  warranty_expiration?: string;
  service_history?: string;
  is_active: boolean;
  created_at: string;
  updated_at?: string;
}

export interface Job {
  id: number;
  tenant_id: number;
  customer_id: number;
  title: string;
  description?: string;
  status: string;
  priority: string;
  scheduled_date?: string;
  completed_date?: string;
  estimated_hours?: number;
  actual_hours?: number;
  labor_cost?: number;
  parts_cost?: number;
  total_cost?: number;
  assigned_to_id?: number;
  photos?: string;
  completion_notes?: string;
  created_at: string;
  updated_at?: string;
}

export interface Reminder {
  id: number;
  tenant_id: number;
  customer_id: number;
  title: string;
  description?: string;
  reminder_type: string;
  interval_months: number;
  next_reminder_date?: string;
  last_reminder_date?: string;
  is_active: boolean;
  channel: string;
  template?: string;
  sent_count: number;
  created_at: string;
  updated_at?: string;
}

export interface Token {
  access_token: string;
  refresh_token: string;
  token_type: string;
}

export interface LoginRequest {
  username: string;
  password: string;
}

export interface RegisterRequest {
  email: string;
  password: string;
  first_name?: string;
  last_name?: string;
}

export interface AnalyticsData {
  total_leads: number;
  total_customers: number;
  active_jobs: number;
  active_reminders: number;
  leads_this_month: number;
  customers_this_month: number;
  jobs_completed_this_month: number;
  revenue_this_month: number;
  conversion_rate: number;
  average_job_value: number;
}