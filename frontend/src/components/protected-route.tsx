import {ProtectedRouteProps} from "@/types/RouteTypes.tsx";
import React, {useContext} from "react";
import {AuthContext} from "@/context/AuthContext.tsx";
import {Navigate} from "react-router-dom";


export const ProtectedRoute: React.FC<ProtectedRouteProps> = ({
  children
}) => {
  const {user, isLoading} = useContext(AuthContext);

  if (isLoading){
    return <div>Loading...</div>
  }

  if (user === null) {
    return <Navigate to="/" replace/>;
  }

  return <>{children}</>;
};