import HeaderLogo from "../components/HeaderLogo";
import React, { useState, useRef, useEffect } from "react";
import { getCookie, fetchUserData } from "../utils/utils.js";
import "../assets/styles/edit-profile.css";
import { AuthContext } from "../context/AuthContext";

export default function EditProfilePage() {
  const { user } = useContext(AuthContext);
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
            <label className="form-label">Display Name</label>
            <input
              type="text"
              name="displayName"
              placeholder={user?.displayName}
              required
              onChange={handleChange}
              value={formData.displayName}
            />
            <label className="form-label">Profile Picture URL</label>
            <input
              type="text"
              name="profilePicutre"
              placeholder={user?.profilePicutre}
              required
              onChange={handleChange}
              value={formData.profilePicutre}
            />
            <button id="post-button">Post</button>
          </form>
        </div>
      </div>
    </div>
  );
}
