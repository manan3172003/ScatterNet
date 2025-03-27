import { createContext } from "react";
import { AuthContextType } from "@/types/AuthTypes.tsx";

export const AuthContext = createContext<AuthContextType>({} as AuthContextType);
