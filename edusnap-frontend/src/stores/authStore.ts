import { create } from 'zustand';
import { persist } from 'zustand/middleware';

interface AuthState {
  isAuthenticated: boolean;
  role: string | null;
  user: any;
  token: string | null;
  login: (email: string, password: string, role: string) => Promise<void>;
  logout: () => void;
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      isAuthenticated: false,
      role: null,
      user: null,
      token: null,
      login: async (email, password, role) => {
        const response = await import('../services/api').then(api => api.login(email, password));  // Removed 'role' from API call
        set({ isAuthenticated: true, role, user: response.user, token: response.token });
      },
      logout: () => {
        import('../services/api').then(api => api.logout());
        set({ isAuthenticated: false, role: null, user: null, token: null });
      },
    }),
    {
      name: 'auth-storage',
    }
  )
);