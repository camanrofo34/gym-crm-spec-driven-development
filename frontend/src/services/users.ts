import { api } from "./api";
import { User } from "../types";

export async function getUsers() {
  const { data } = await api.get<User[]>("/users");
  return data;
}

