import React from "react";
import AdminDashboard from "../components/AdminDashboard";
import "../assets/styles/admin-page.css";

const AdminPage = () => {
  return (
    <div className="admin-page">
      <h1>Admin Management Dashboard</h1>
      <AdminDashboard />
    </div>
  );
};

export default AdminPage;
