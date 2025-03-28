import {ProtectedRouteProps} from "@/types/RouteTypes.tsx";
import React from "react";
import {Navigate} from "react-router-dom";
import {getCookie} from "@/utils/ApiCall.tsx";


export const AdminProtectedRoute: React.FC<ProtectedRouteProps> = ({
    children
    }) => {
  const isAdmin = getCookie("isAdmin") === "true";

  if (isAdmin) {
      return <>{children}</>
  } else {
      return <Navigate to="/" replace/>;
  }
};