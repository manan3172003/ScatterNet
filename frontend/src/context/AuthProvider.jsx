/* Credit: https://dev.to/miracool/how-to-manage-user-authentication-with-react-js-3ic5 */


import { useState,useEffect } from "react";
import PropTypes from "prop-types";
import { AuthContext } from "./AuthContext";

export const AuthProvider = ({ children }) => {
    AuthProvider.propTypes = {
        children: PropTypes.node.isRequired, // Ensures 'children' is required
      };  
      
    const [user, setUser] = useState(null);
    const fetchUserData = async () => {
        try {
            const response = await fetch("http://localhost:8000/api/authors/current-user", {
                method: "GET",
                credentials: "include", 
                headers: {
                    "Content-Type": "application/json",
                },
            });

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
            const response = await fetch("http://localhost:8000/api/authors/login", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                credentials: "include",
                body : JSON.stringify({
                    "username": username,
                    "password":password
                }),
                
            });

            const data = await response.json();
            
            if (response.ok) {
                setUser(data.user);
            } else {
                setUser(null);
                throw new Error(response.status); // Throw an error with the response status
            }
            return { success: true };
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