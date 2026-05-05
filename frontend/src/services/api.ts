import axios, { AxiosError } from "axios";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "/api";
const AUTH_TOKEN_KEY = "gym_auth_token";

export const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 12000
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem(AUTH_TOKEN_KEY);
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

api.interceptors.response.use(
  (response) => response,
  (error: AxiosError<{ detail?: string }>) => {
    const message = error.response?.data?.detail ?? error.message ?? "Unexpected API error";
    return Promise.reject(new Error(message));
  }
);

export const storageKeys = {
  token: AUTH_TOKEN_KEY,
  user: "gym_auth_user"
};

