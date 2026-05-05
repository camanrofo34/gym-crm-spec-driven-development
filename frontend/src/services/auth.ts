import { api } from "./api";
import { AuthResponse, UserRole } from "../types";

export interface LoginPayload {
  email: string;
  password: string;
}

export interface RegisterPayload extends LoginPayload {
  role: UserRole;
}

export async function login(payload: LoginPayload) {
  const { data } = await api.post<AuthResponse>("/auth/login", payload);
  return data;
}

export async function register(payload: RegisterPayload) {
  const { data } = await api.post<AuthResponse>("/auth/register", payload);
  return data;
}

