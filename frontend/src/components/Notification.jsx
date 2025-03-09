/* eslint-disable react/prop-types */
import { useEffect, useState } from "react";
import "../assets/styles/notifications.css";

export default function Notification({
  type = "success",
  title,
  message,
  duration = 5000,
  onClose,
  show,
}) {
  const [visible, setVisible] = useState(show);

  useEffect(() => {
    setVisible(show);
    
    if (show && duration) {
      const timer = setTimeout(() => {
        setVisible(false);
        if (onClose) setTimeout(onClose, 500); 
      }, duration);
      
      return () => clearTimeout(timer);
    }
  }, [show, duration, onClose]);

  const handleClose = () => {
    setVisible(false);
    if (onClose) setTimeout(onClose, 500);
  };

  // Icon is based on notification type TODO: change the error icon to something better 
  const getIcon = () => {
    switch (type) {
      case "success":
        return "✓";
      case "warning":
        return "⚠";
      case "error":
        return "error";
      default:
        return "ℹ";
    }
  };

  return (
    <div className={`notification ${type} ${visible ? "show" : ""}`}>
      <div className="notification-icon">{getIcon()}</div>
      <div className="notification-content">
        {title && <div className="notification-title">{title}</div>}
        {message && <div className="notification-message">{message}</div>}
      </div>
      <button className="notification-close" onClick={handleClose}>
        ×
      </button>
    </div>
  );
}
