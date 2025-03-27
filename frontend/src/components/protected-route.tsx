import {ProtectedRouteProps} from "@/types/RouteTypes.tsx";
import {useContext} from "react";
import {AuthContext} from "@/context/AuthContext.tsx";
import {Navigate} from "react-router-dom";


export const ProtectedRoute: React.FC<ProtectedRouteProps> = ({
  children
}) => {
  const authContext = useContext(AuthContext);
  console.log(authContext);
  const user = authContext?.user
  // console.log(user)
  if (!user) {
    return <Navigate to="/" />;
  }
  return children;
};