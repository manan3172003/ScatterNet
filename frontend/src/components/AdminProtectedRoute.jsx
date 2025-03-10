import React from "react";
import { Navigate } from "react-router-dom";
import { getCookie } from "../utils/utils.js";

export default function AdminProtectedRoute({ element }) {
  const isAdmin = getCookie("isAdmin") === "true";

  if (!isAdmin) {
    return <Navigate to="/home" replace />;
  }

  return element;
}