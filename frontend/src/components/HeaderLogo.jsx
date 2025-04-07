import { useNavigate } from "react-router-dom";
import "../assets/styles/header-logo.css";
import { apiCall } from "../utils/utils.js";
import getCookie from "../context/Cookie";
import { AuthContext } from "../context/AuthContext";
import { useContext } from "react";

export default function HeaderLogo() {
  const navigate = useNavigate();
  const {user} = useContext(AuthContext)

  const handleLogout = async () => {
    try {
      const response = await apiCall('authors/logout',"POST");
      
      if (response.ok) {
        
        window.location.reload();
      } else {
        console.error("Logout failed");
      }
    } catch (error) {
      console.error("Logout error:", error);
    }
  };

  return (
    <div className="header-container"> 
      <h1 className="logo">OnlyNodes</h1>
      { user ? <button 
        className="logout-button" 
        onClick={handleLogout}
        aria-label="Logout"
      >
        Logout
      </button>: <></>}
    </div>
  );
}
