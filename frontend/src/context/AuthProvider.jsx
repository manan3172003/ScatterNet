/* Credit: https://dev.to/miracool/how-to-manage-user-authentication-with-react-js-3ic5 */


import { useState,useEffect } from "react";
import PropTypes from "prop-types";
import { AuthContext } from "./AuthContext";
import { apiCall } from "../utils/utils.js"

export const AuthProvider = ({ children }) => {
    AuthProvider.propTypes = {
        children: PropTypes.node.isRequired,
      };
    const [user, setUser] = useState(null);
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

    const login = async (username, password) => {
        try {
            fetchUserData()
            console.log("sending login request....")
            const response = await apiCall("authors/login",
                "POST",
                {
                    "username": username,
                    "password":password
                }
                );

            const data = await response.json();
            
            if (response.ok) {
                fetchUserData();
                if (data.user.is_node_admin) {
                     document.cookie = "isAdmin=true; path=/;";
                } else {
                    document.cookie = "isAdmin=false; path=/;";
                }
                setUser(data.user);
            } else {
                setUser(null);
                throw new Error(response.status); 
            }
            
            return { success: true }

        } catch (error) {
            return { success: false, status: error.message}
        }
    };
    

    return (
        <AuthContext.Provider value={{ user, login}}>
        {children}
        </AuthContext.Provider>
    );

};