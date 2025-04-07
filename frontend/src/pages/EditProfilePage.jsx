import HeaderLogo from "../components/HeaderLogo";
import React, {useState, useContext, useEffect} from "react";
import {getCookie, fetchUserData, apiCall} from "../utils/utils.js";
import "../assets/styles/edit-profile.css";
import { AuthContext } from "../context/AuthContext";
import Notification from "../components/Notification";
import {useNavigate} from "react-router-dom";

export default function EditProfilePage() {
  const { user } = useContext(AuthContext);
  const [loading, setLoading] = useState(true);
  const [ author, setAuthor ] = useState(null);
  const [formData, setFormData] = useState({
    displayName: "",
    profilePicture: "",
  });
  const [notification, setNotification] = useState({
    show: false,
    type: "success",
    title: "",
    message: "",
  });
  const csrfToken = getCookie("csrftoken");
  const navigate = useNavigate();

  // Helper to show notifications
  const showNotification = (type, title, message) => {
    setNotification({
      show: true,
      type,
      title,
      message,
    });
  };
  // Helper to hide notifications
  const hideNotification = () => {
    setNotification((prev) => ({ ...prev, show: false }));
  };

  useEffect(() => {
    fetchAuthor();
  }, []);

  const fetchAuthor = async () => {
    setLoading(true);
    let resp = await fetchUserData();
    let AUTHOR_SERIAL = resp.user.author_id;

    try {
      const response = await apiCall(`authors/${AUTHOR_SERIAL}`);
      if (!response.ok) {
        throw new Error("Failed to fetch authors");
      }
      const data = await response.json();
      setAuthor(data);
      setFormData({
        displayName: data.displayName,
        profilePicture: data.profileImageURL
      })
    } catch (err) {
      console.error("Error fetching authors:", err);
      showNotification("error", "Load Error", "Failed to load author");
    }
    setLoading(false);
  };

  function handleChange(e) {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
    console.log(formData);
  }
  async function handleEdit(e) {
    e.preventDefault();
    let resp = await fetchUserData();
    let AUTHOR_SERIAL = resp.user.author_id;

    try {
      const response = await apiCall(
          `authors/${AUTHOR_SERIAL}`,
          'PUT',
          {
              displayName: formData.displayName || author.displayName,
              profileImageURL: formData.profilePicture || author.profileImageURL
          }
      )

      const data = await response.json();

      if (response.ok) {
        showNotification(
                "success",
                "Update Successful",
                "Redirecting to your profile..."
            );
            setTimeout(() => {navigate(`/authors/${AUTHOR_SERIAL}`)}, 1500);
      } else {
        console.error("Error updating profile");
        showNotification("error", "Update Failed", data.message || "Something went wrong. Please try again.");
      }

    } catch (error) {
      console.error("Error updating profile: ", error);
    }
  }

  if (loading) {
    return <div>Loading author...</div>
  }

  return (
    <div className="edit-profile-container">
      <Notification
        show={notification.show}
        type={notification.type}
        title={notification.title}
        message={notification.message}
        onClose={hideNotification}
      />
      <header className="posting-header">{<HeaderLogo />}</header>
      <div className="editing-main">
        <div className="form-content">
          <form className="edit-profile-form" onSubmit={handleEdit}>
            <label className="edit-title">Edit Profile</label>
            <label className="form-label">Display Name</label>
            <input
              type="text"
              name="displayName"
              placeholder="display name"
              onChange={handleChange}
              value={formData.displayName}
            />
            <label className="form-label">Profile Picture URL</label>
            <input
              type="text"
              name="profilePicture"
              placeholder="profile url"
              onChange={handleChange}
              value={formData.profilePicture}
            />
            <button id="post-button">Confirm</button>
          </form>
        </div>
      </div>
    </div>
  );
}
