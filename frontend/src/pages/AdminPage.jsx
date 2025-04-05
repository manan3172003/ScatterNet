import React from "react";
import AdminDashboard from "../components/AdminDashboard";
import "../assets/styles/admin-page.css";

const AdminPage = () => {
  return (
    <div className="admin-page">
      <h2 className="admin-page-title">Admin Management Dashboard</h2>
      <AdminDashboard />
    </div>
  );
};

export default AdminPage;
