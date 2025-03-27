import React, { useState, useEffect } from "react";
import { AuthContext } from "./AuthContext";
import { apiCall } from "../utils/ApiCall.tsx";
import { AuthProviderProps, LoginResponse, User } from "@/types/AuthTypes.tsx";

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);

  const fetchUserData = async () => {
    try {
      const response = await apiCall("authors/current-user");

      if (response.ok) {
        const data = await response.json();
        setUser(data.user);
      } else {
        setUser(null);
      }
    } catch (error) {
      console.error("Error fetching user data:", error);
      setUser(null);
    }
  };

  useEffect(() => {
      fetchUserData();
  }, []);

  const login = async (username: string, password: string): Promise<LoginResponse> => {
    try {
      await fetchUserData();
      console.log("sending login request....");
      
      const response = await apiCall("authors/login", "POST", {
        username,
        password
      });

      const data = await response.json();
      
      if (response.ok) {
        await fetchUserData();
        
        // Set admin cookie
        document.cookie = data.user.is_node_admin 
          ? "isAdmin=true; path=/;" 
          : "isAdmin=false; path=/;";
        
        setUser(data.user);
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
    <AuthContext.Provider value={{ user, login }}>
      {children}
    </AuthContext.Provider>
  );
};
