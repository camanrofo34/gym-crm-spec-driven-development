export type UserRole = "TRAINEE" | "TRAINER";

export interface User {
  id: number;
  email: string;
  role: UserRole;
  is_active: boolean;
  created_at: string;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
  user: User;
}

export interface Activity {
  id: number;
  user_id: number;
  duration_minutes: number;
  activity_type: string;
  date: string;
}

export interface Assignment {
  id: number;
  trainee_id: number;
  trainer_id: number;
}

export interface TrainerLoad {
  trainer_id: number;
  trainer_email: string;
  week_start: string;
  week_end: string;
  total_duration_minutes: number;
}

export interface RankingItem {
  rank: number;
  trainer_id: number;
  trainer_email: string;
  total_duration_minutes: number;
}

export interface UserSummary {
  user_id: number;
  user_email: string;
  total_activities: number;
  average_duration_minutes: number;
}

