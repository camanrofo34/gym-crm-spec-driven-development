import { api } from "./api";
import { Assignment } from "../types";

export interface CreateAssignmentPayload {
  trainee_id: number;
  trainer_id: number;
}

export async function getAssignments() {
  const { data } = await api.get<Assignment[]>("/assignments");
  return data;
}

export async function createAssignment(payload: CreateAssignmentPayload) {
  const { data } = await api.post<Assignment>("/assignments", payload);
  return data;
}

