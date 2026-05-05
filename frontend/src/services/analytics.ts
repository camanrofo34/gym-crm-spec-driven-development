import { api } from "./api";
import { RankingItem, TrainerLoad, UserSummary } from "../types";

export async function getTrainerRanking() {
  const { data } = await api.get<RankingItem[]>("/analytics/trainer-ranking");
  return data;
}

export async function getTrainerLoad() {
  const { data } = await api.get<TrainerLoad[]>("/analytics/trainer-load");
  return data;
}

export async function getUserSummary() {
  const { data } = await api.get<UserSummary[]>("/analytics/user-summary");
  return data;
}

