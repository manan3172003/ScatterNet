import { Navigate } from "react-router-dom";
import { useContext } from "react";
import { AuthContext } from "../context/AuthContext";

// eslint-disable-next-line react/prop-types
const ProtectedRoute = ({ element }) => {
    const { user } = useContext(AuthContext); 
    
    return user ? element : <Navigate to="/" replace />;
};

export default ProtectedRoute;