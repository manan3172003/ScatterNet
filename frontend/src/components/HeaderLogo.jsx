import { useNavigate } from "react-router-dom";
import { useContext } from "react"; // Import useContext
import "../assets/styles/header-logo.css";
import { apiCall } from "../utils/utils.js";
import { AuthContext } from "../context/AuthContext";

export default function HeaderLogo() {
  const navigate = useNavigate();
  const { logout } = useContext(AuthContext); 

  const handleLogout = async () => {
    try {
    
      const result = await logout();
      
      if (result.success) {
        navigate('/login'); 
      } else {
        console.error("Logout failed:", result.status);
      }
    } catch (error) {
      console.error("Logout error:", error);
    }
  };

  return (
    <div className="header-container"> 
      <h1 className="logo">OnlyNodes</h1>
      <button 
        className="logout-button" 
        onClick={handleLogout}
        aria-label="Logout"
      >
        Logout
      </button>
    </div>
  );
}
