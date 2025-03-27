import React, { useState, useEffect } from "react";
import { AuthContext } from "./AuthContext";
import { apiCall } from "../utils/ApiCall.tsx";
import { AuthProviderProps, LoginResponse, User } from "@/types/AuthTypes.tsx";

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  const fetchUserData = async () => {
    try {
      setIsLoading(true);
      const response = await apiCall("authors/current-user");

      if (response.ok) {
        const data = await response.json();

        if (data && data.user) {
          setUser(data.user);
        } else {
          console.warn("No user data found in response");
          setUser(null);
        }
      } else {
        console.warn("Response not OK. Status:", response.status);
        setUser(null);
      }
    } catch (error) {
      console.error("Error fetching user data:", error);
      setUser(null);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchUserData();
  }, []);

  const login = async (username: string, password: string): Promise<LoginResponse> => {
    try {
      const response = await apiCall("authors/login", "POST", {
        username,
        password
      });

      const data = await response.json();

      if (response.ok) {
        // Immediately fetch user data after successful login
        await fetchUserData();

        // Set admin cookie
        document.cookie = data.user.is_node_admin
          ? "isAdmin=true; path=/;"
          : "isAdmin=false; path=/;";

        return { success: true };
      } else {
        setUser(null);
        throw new Error(response.status.toString());
      }

    } catch (error) {
      return {
        success: false,
        status: error instanceof Error ? error.message : 'Unknown error'
      };
    }
  };

  return (
    <AuthContext.Provider value={{ user, login, isLoading }}>
      {children}
    </AuthContext.Provider>
  );
};