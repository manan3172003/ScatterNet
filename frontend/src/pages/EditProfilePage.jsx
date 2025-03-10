import HeaderLogo from "../components/HeaderLogo";
import React, { useState, useRef, useEffect } from "react";
import { getCookie, fetchUserData } from "../utils/utils.js";
import "../assets/styles/edit-profile.css";

export default function EditProfilePage() {
  const [formData, setFormData] = useState({
    displayName: "",
    profilePicutre: "",
  });
  function handleChange(e) {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
    console.log(formData);
  }
  return (
    <div className="edit-profile-container">
      <header className="posting-header">{<HeaderLogo />}</header>
      <div className="editing-main">
        <div className="form-content">
          <form className="edit-profile-form" onSubmit={handleEdit}>
            <label className="form-label">Edit Profile</label>
            <label className="form-label">Visibility</label>
          </form>
        </div>
      </div>
    </div>
  );
}
