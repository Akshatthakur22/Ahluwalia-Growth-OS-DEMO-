import { create } from 'zustand';
import api from './api';

export interface User {
  id: string;
  employee_code: string;
  full_name: string;
  mobile_number: string;
  email?: string;
  role: string;
  department?: string;
  assigned_region?: string;
  status: string;
}

interface AuthState {
  user: User | null;
  isLoading: boolean;
  login: (mobile: string, password: string) => Promise<void>;
  logout: () => void;
  fetchUser: () => Promise<void>;
}

export const useAuthStore = create<AuthState>((set, get) => ({
  user: null,
  isLoading: false,

  login: async (mobile, password) => {
    const { data } = await api.post('/auth/login', {
      mobile_number: mobile,
      password,
    });
    localStorage.setItem('access_token', data.access_token);
    set({ user: data.user });
  },

  logout: () => {
    localStorage.removeItem('access_token');
    set({ user: null });
  },

  fetchUser: async () => {
    const token = localStorage.getItem('access_token');
    if (!token) {
      set({ user: null, isLoading: false });
      return;
    }
    const hadUser = get().user;
    if (!hadUser) set({ isLoading: true });
    try {
      const { data } = await api.get('/auth/me');
      set({ user: data });
    } catch {
      localStorage.removeItem('access_token');
      set({ user: null });
    } finally {
      set({ isLoading: false });
    }
  },
}));
