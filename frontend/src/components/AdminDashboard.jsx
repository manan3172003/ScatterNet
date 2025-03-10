import React, { useState, useEffect } from "react";
import "../assets/styles/admin-dashboard.css";
import getCookie from "../context/Cookie.js";
import Notification from "../components/Notification";

const AdminDashboard = () => {
  const [authors, setAuthors] = useState([]);
  const [loading, setLoading] = useState(true);
  const [updating, setUpdating] = useState({});
  const [error, setError] = useState(null);
  const csrfToken = getCookie("csrftoken");

  // Notification state
  const [notification, setNotification] = useState({
    show: false,
    type: "success",
    title: "",
    message: "",
  });

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

  // Fetch authors on component mount
  useEffect(() => {
    fetchAuthors();
  }, []);

  const fetchAuthors = async () => {
    setLoading(true);
    try {
      const response = await fetch("http://localhost:8000/api/authors", {
        credentials: "include",
      });
      if (!response.ok) {
        throw new Error("Failed to fetch authors");
      }
      const data = await response.json();
      setAuthors(data.authors);
    } catch (err) {
      console.error("Error fetching authors:", err);
      showNotification("error", "Load Error", "Failed to load authors");
    }
    setLoading(false);
  };

  const handleInputChange = (index, field, value) => {
    const updatedAuthors = [...authors];
    updatedAuthors[index][field] = value;
    setAuthors(updatedAuthors);
  };

  const handleSave = async (index) => {
    const author = authors[index];
    // Extract the author_id from the author's id URL.
    const urlParts = author.id.split("/").filter(Boolean);
    const authorId = urlParts[urlParts.length - 1];

    // Set updating state for this author
    setUpdating((prev) => ({ ...prev, [authorId]: true }));

    const payload = {
      displayName: author.displayName,
      github: author.github,
      profileImage: author.profileImage,
      state: author.state,
    };

    try {
      const response = await fetch(`/api/authors/${authorId}`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": csrfToken,
        },
        body: JSON.stringify(payload),
        credentials: "include",
      });
      if (!response.ok) {
        throw new Error("Failed to update author");
      }
      showNotification("success", "Update Successful", "Author updated successfully!");
      // Re-fetch the authors list after a successful update
      fetchAuthors();
    } catch (err) {
      console.error("Error updating author:", err);
      showNotification("error", "Update Failed", "Failed to update author");
    }
    setUpdating((prev) => ({ ...prev, [authorId]: false }));
  };

  if (loading) {
    return <div>Loading authors...</div>;
  }

  return (
    <div className="admin-dashboard">
      <Notification
        show={notification.show}
        type={notification.type}
        title={notification.title}
        message={notification.message}
        onClose={hideNotification}
      />
      <h1>Node Authors List</h1>
      <div className="authors-list">
        {authors.map((author, index) => (
          <div key={author.id} className="post-container">
            <div className="post-header">
              <div className="post-header-top">
                <h2 className="post-title">{author.username}</h2>
                <div className="form-group">
                  <label>Display Name:</label>
                  <input
                    type="text"
                    value={author.displayName || ""}
                    onChange={(e) =>
                      handleInputChange(index, "displayName", e.target.value)
                    }
                    placeholder="Display Name"
                    className="desktop-input-field"
                  />
                </div>
              </div>
              <div className="post-author">
                {author.profileImage && (
                  <img
                    src={author.profileImage}
                    alt={author.displayName}
                    className="post-avatar"
                  />
                )}
                <div className="author-info">
                  <div className="form-group">
                    <label>GitHub URL:</label>
                    <input
                      type="text"
                      value={author.github || ""}
                      onChange={(e) =>
                        handleInputChange(index, "github", e.target.value)
                      }
                      placeholder="GitHub URL"
                      className="desktop-input-field"
                    />
                  </div>
                </div>
              </div>
            </div>
            <div className="post-content">
              <div className="form-group">
                <label>Profile Image URL:</label>
                <input
                  type="text"
                  value={author.profileImage || ""}
                  onChange={(e) =>
                    handleInputChange(index, "profileImage", e.target.value)
                  }
                  placeholder="Profile Image URL"
                  className="desktop-input-field"
                />
              </div>
              <div className="form-group">
                <label>Page URL:</label>
                <input
                  type="text"
                  value={author.page || ""}
                  className="desktop-input-field"
                  disabled
                />
              </div>
              <div className="form-group">
                <label>State:</label>
                <select
                  value={author.state || "PENDING"}
                  onChange={(e) =>
                    handleInputChange(index, "state", e.target.value)
                  }
                  className="desktop-input-field"
                >
                  <option value="ACTIVE">ACTIVE</option>
                  <option value="PENDING">PENDING</option>
                  <option value="DELETED">DELETED</option>
                </select>
              </div>
              <button
                className="download-button"
                onClick={() => handleSave(index)}
                disabled={updating[author.id]}
              >
                {updating[author.id] ? "Saving..." : "Save"}
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default AdminDashboard;
