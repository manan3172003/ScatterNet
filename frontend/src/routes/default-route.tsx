import {ProtectedRouteProps} from "@/types/RouteTypes.tsx";
import React, {useContext} from "react";
import {AuthContext} from "@/context/AuthContext.tsx";
import {Navigate} from "react-router-dom";


export const DefaultRoute: React.FC<ProtectedRouteProps> = ({}) => {
  const {user, isLoading} = useContext(AuthContext);

  if (isLoading){
    return <div>Loading...</div>
  }

  if (user === null) {
    return <Navigate to="/" replace/>;
  } else {
      return <Navigate to="/home" replace/>;
  }
};