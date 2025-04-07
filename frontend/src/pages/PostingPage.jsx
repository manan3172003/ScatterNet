// PostingPage.jsx
import HeaderLogo from "../components/HeaderLogo";
import Notification from "../components/Notification.jsx";
import VideoPlayer from "../components/VideoPlayer.jsx"; // New component for video
import "../assets/styles/posting-page.css";

import { useState, useEffect } from "react";
import { useNavigate } from 'react-router-dom';
import {
  fetchUserData,
  apiCall,
  handleFile,
  validExtensions,
  handleVideoFile,
  autoResize
} from "../utils/utils.js";

export default function PostingPage() {
  const [base64Data, setBase64] = useState("");
  const [base64ContentType, setBase64ContentType] = useState("");
  const [fileName, setFileName] = useState("");
  const navigate = useNavigate();

  const [videoPreview, setVideoPreview] = useState(null);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [isUploading, setIsUploading] = useState(false);

  const [notification, setNotification] = useState({
    show: false,
    type: "success",
    title: "",
    message: "",
  });

  const [formData, setFormData] = useState({
    title: "",
    description: "",
    contentType: "text/markdown",
    content: "",
    visibility: "PUBLIC",
  });

  const { textareaRef: descriptionRef, resizeTextarea: resizeDescription } = autoResize(200, 100);
  const { textareaRef: contentRef, resizeTextarea: resizeContent } = autoResize(300, 100);

  // resize text areas when form data changes
  useEffect(() => {
    if (formData.description) {
      setTimeout(resizeDescription, 100);
    }
    if (formData.content) {
      setTimeout(resizeContent, 100);
    }
  }, [formData.description, formData.content]);

  const showNotification = (type, title, message) => {
    setNotification({ show: true, type, title, message });
  };

  const hideNotification = () => {
    setNotification((prev) => ({ ...prev, show: false }));
  };

  function handleChange(e) {
    setFormData({ ...formData, [e.target.name]: e.target.value });
    
    // resize text areas when content changes
    if (e.target.name === 'description') {
      setTimeout(resizeDescription, 0);
    } else if (e.target.name === 'content') {
      setTimeout(resizeContent, 0);
    }
  }

  function handleDropdownChange(e) {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
      content: ""
    });
    if (!e.target.value.includes("video")) {
      setVideoPreview(null);
    }
  }

  function handleVideoUpload(e) {
    handleVideoFile(
      e,
      setFileName,
      setBase64,
      setBase64ContentType,
      setVideoPreview,
      setUploadProgress,
      setIsUploading,
      showNotification
    );
  }

  async function handlePost(e) {
    e.preventDefault();

    if (!formData.visibility || !formData.contentType) {
      showNotification("error", "Incorrect Option Selected", "Please select a valid option!");
      return;
    }

    try {
      let content = "";
      let contentType = "";

      if (formData.contentType.includes("base64")) {
        content = base64Data;
        contentType = base64ContentType;

        if (contentType.includes("video/")) {
          try {
            const videoBlob = await fetch(`data:${contentType},${content}`).then(r => r.blob());
            const videoFile = new File([videoBlob], fileName, { type: contentType.split(';')[0] });
            showNotification("info", "Processing Video", "Your video is being uploaded. This may take a moment...");

            const { uploadReel } = await import('../utils/reelsApi.js');
            const response = await uploadReel(videoFile, formData.description, formData.visibility);

            if (response.ok) {
              showNotification("success", "Reel Created!", "Redirecting to stream...");
              setTimeout(() => { navigate('/reels'); }, 1500);
            } else {
              const errorText = await response.text();
              let errorMessage = "Failed to upload video";
              try {
                const errorData = JSON.parse(errorText);
                errorMessage = errorData.error || errorMessage;
              } catch {
                errorMessage = errorText.substring(0, 100) || errorMessage;
              }
              showNotification("error", "Upload Failed", errorMessage);
            }
          } catch (err) {
            showNotification("error", "Upload Failed", `An error occurred: ${err.message}`);
          }
          return;
        }

        const extension = contentType.split("/")[1].split(";")[0];
        if (!validExtensions.includes(extension)) {
          contentType = 'application/base64';
        }
      } else {
        content = formData.content;
        contentType = formData.contentType;
      }

      const resp = await fetchUserData();
      const AUTHOR_SERIAL = resp.user.author_id;

      const response = await apiCall(`authors/${AUTHOR_SERIAL}/posts`, "POST", {
        title: formData.title,
        description: formData.description,
        contentType,
        content,
        visibility: formData.visibility,
      });

      const data = await response.json();

      if (response.ok) {
        showNotification("success", "Created Post!", "Redirecting to your home feed...");
        setTimeout(() => { navigate(`/home`); }, 1500);
      } else {
        showNotification("error", "Update Failed", data.message || "Something went wrong. Please try again.");
      }
    } catch (error) {
      showNotification("error", "Post Creation Failed", "Something went wrong. Please try again.");
      console.log(error);
    }
  }

  return (
    <div className="posting-container">
      <Notification {...notification} onClose={hideNotification} />
      <header className="header"><HeaderLogo /></header>
      <main className="posting-main">
        <div className="form-content">
          <form className="post-form" onSubmit={handlePost}>
            <label className="form-title">Create Post</label>

            <label className="form-label">Visibility</label>
            <select className="dropdown" name="visibility" value={formData.visibility} onChange={handleChange} required>
              <option value="PUBLIC">Public</option>
              <option value="FRIENDS">Friends-Only</option>
              <option value="UNLISTED">Unlisted</option>
            </select>

            <label className="form-label">Title</label>
            <input type="text" name="title" placeholder="Enter a title" value={formData.title} onChange={handleChange} required />

            <label className="form-label">Description</label>
            <textarea name="description" placeholder="Enter description" value={formData.description} onChange={handleChange} required ref={descriptionRef} />

            <label className="form-label">Content Type</label>
            <select className="dropdown" name="contentType" value={formData.contentType} onChange={handleDropdownChange} required>
              <option value="text/markdown">Markdown</option>
              <option value="text/plain">Plain</option>
              <option value="application/base64">Image</option>
              <option value="video/mp4;base64">Video</option>
            </select>

            {(formData.contentType === 'text/plain' || formData.contentType === 'text/markdown') && (
              <>
                <label className="form-label">Content</label>
                <textarea name="content" placeholder="Enter content" value={formData.content} onChange={handleChange} required ref={contentRef} />
              </>
            )}

            {formData.contentType === 'application/base64' && (
              <>
                <label className="form-label">Image</label>
                <input type="file" accept="image/*" onChange={(e) => handleFile(e, setFileName, setBase64, setBase64ContentType)} />
                {fileName && <p>Selected File: {fileName}</p>}
              </>
            )}

            {formData.contentType === 'video/mp4;base64' && (
              <>
                <label className="form-label">Video</label>
                <div className="file-input-container">
                  <label className="file-input-label">
                    <span className="upload-button">Select Video</span>
                    <input type="file" className="file-input-hidden" accept="video/mp4,video/webm,video/quicktime" onChange={handleVideoUpload} />
                  </label>
                  {fileName && <p className="selected-file">Selected: {fileName}</p>}
                  {isUploading && (
                    <div className="upload-progress">
                      <div className="upload-progress-bar" style={{ width: `${uploadProgress}%` }}></div>
                    </div>
                  )}
                </div>
                {videoPreview && (
                  <div className="video-preview">
                    <label className="form-label">Preview</label>
                    <VideoPlayer src={videoPreview} />
                  </div>
                )}
              </>
            )}

            <button id="post-button">Post</button>
          </form>
        </div>
      </main>
    </div>
  );
}