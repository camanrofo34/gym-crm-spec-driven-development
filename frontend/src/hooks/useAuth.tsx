import { createContext, useContext, useEffect, useMemo, useState } from "react";
import { AuthResponse, User } from "../types";
import { login, register } from "../services/auth";
import { storageKeys } from "../services/api";

interface LoginInput {
  email: string;
  password: string;
}

interface RegisterInput extends LoginInput {
  role: "TRAINEE" | "TRAINER";
}

interface AuthContextValue {
  token: string | null;
  user: User | null;
  isAuthenticated: boolean;
  loginWithCredentials: (input: LoginInput) => Promise<void>;
  registerUser: (input: RegisterInput) => Promise<void>;
  logout: () => void;
}

const AuthContext = createContext<AuthContextValue | undefined>(undefined);

function persistSession(payload: AuthResponse) {
  localStorage.setItem(storageKeys.token, payload.access_token);
  localStorage.setItem(storageKeys.user, JSON.stringify(payload.user));
}

function clearSession() {
  localStorage.removeItem(storageKeys.token);
  localStorage.removeItem(storageKeys.user);
}

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [token, setToken] = useState<string | null>(null);
  const [user, setUser] = useState<User | null>(null);

  useEffect(() => {
    const storedToken = localStorage.getItem(storageKeys.token);
    const rawUser = localStorage.getItem(storageKeys.user);
    if (storedToken && rawUser) {
      setToken(storedToken);
      setUser(JSON.parse(rawUser) as User);
    }
  }, []);

  const loginWithCredentials = async (input: LoginInput) => {
    const payload = await login(input);
    persistSession(payload);
    setToken(payload.access_token);
    setUser(payload.user);
  };

  const registerUser = async (input: RegisterInput) => {
    const payload = await register(input);
    persistSession(payload);
    setToken(payload.access_token);
    setUser(payload.user);
  };

  const logout = () => {
    clearSession();
    setToken(null);
    setUser(null);
  };

  const value = useMemo<AuthContextValue>(
    () => ({
      token,
      user,
      isAuthenticated: Boolean(token),
      loginWithCredentials,
      registerUser,
      logout
    }),
    [token, user]
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used inside AuthProvider");
  }
  return context;
}

