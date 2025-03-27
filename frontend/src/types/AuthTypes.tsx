import React from "react";

export type User = {
  username: string;
  displayname: string;
  author_id: string;
  is_node_admin: boolean | null;
}

export type LoginResponse = {
  success: boolean;
  status?: string;
}

export type AuthContextType = {
  user: User | null;
  login: (username: string, password: string) => Promise<LoginResponse>;
}

export type AuthProviderProps = {
  children: React.ReactNode;
}
