import { createContext } from "react";
import { User, LoginResponse } from "@/context/AuthProvider.tsx"

export const AuthContext = createContext<AuthContextType | null>(null);

interface AuthContextType {
  user: User | null;
  login: (username: string, password: string) => Promise<LoginResponse>;
}