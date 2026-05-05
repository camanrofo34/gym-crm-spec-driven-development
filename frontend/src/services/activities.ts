import { api } from "./api";
import { Activity } from "../types";

export interface CreateActivityPayload {
  user_id: number;
  duration_minutes: number;
  activity_type: string;
  date: string;
}

export async function getActivities(userId?: number) {
  const { data } = await api.get<Activity[]>("/activities", {
    params: userId ? { user_id: userId } : undefined
  });
  return data;
}

export async function createActivity(payload: CreateActivityPayload) {
  const { data } = await api.post<Activity>("/activities", payload);
  return data;
}

