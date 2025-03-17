/* Credit: https://dev.to/miracool/how-to-manage-user-authentication-with-react-js-3ic5 */


import { useState,useEffect } from "react";
import PropTypes from "prop-types";
import { AuthContext } from "./AuthContext";
import getCookie from "../context/Cookie";
export const AuthProvider = ({ children }) => {
    AuthProvider.propTypes = {
        children: PropTypes.node.isRequired, 
      };  
    const [csrfToken, setToken] = useState(getCookie('csrftoken'));
    const [user, setUser] = useState(null);
    const fetchUserData = async () => {
        try {
            const response = await fetch("http://localhost:8000/api/authors/current-user", {
                method: "GET",
                credentials: "include", 
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": csrfToken
                },
            });
            

            if (response.ok) {
                const data = await response.json();
                setUser(data.user);
                setToken(getCookie('csrftoken'));
            } else {
                setUser(null);
                setToken(getCookie('csrftoken'));
            }
        } catch (error) {
            console.error("Error fetching user data:", error);
            setUser(null);
            setToken(getCookie('csrftoken'));
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
                    "X-CSRFToken": csrfToken
                },
                credentials: "include",
                body : JSON.stringify({
                    "username": username,
                    "password":password
                }),
                
            });

            const data = await response.json();
            
            if (response.ok) {
                fetchUserData();
                if (data.user.is_node_admin) {
                     document.cookie = "isAdmin=true; path=/;";
                } else {
                    document.cookie = "isAdmin=false; path=/;";
                }
                setUser(data.user);
                setToken(getCookie('csrftoken'));
            } else {
                setUser(null);
                setToken(getCookie('csrftoken'));
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