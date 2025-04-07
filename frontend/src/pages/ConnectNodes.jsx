import React, { useState } from "react";
import "../assets/styles/connect-nodes.css";
import { apiCall } from "../utils/utils/";
import Notification from "../components/Notification";

const NodeRegistration = () => {
  const [loading, setLoading] = useState(false);
  const [notification, setNotification] = useState({
    show: false,
    type: "success",
    title: "",
    message: "",
  });

  const [homeCredentials, setHomeCredentials] = useState({
    homeUsername: "",
    homePassword: "",
    host: "",
  });

  const [remoteNodeCredentials, setRemoteNodeCredentials] = useState({
    remoteUsername: "",
    remotePassword: "",
    displayName: "",
    remoteHost: "",
  });

  const handleHomeCredentialsChange = (e) => {
    setHomeCredentials({
      ...homeCredentials,
      [e.target.name]: e.target.value,
    });
  };

  const handleRemoteCredentialsChange = (e) => {
    setRemoteNodeCredentials({
      ...remoteNodeCredentials,
      [e.target.name]: e.target.value,
    });
  };

  const showNotification = (type, title, message) => {
    setNotification({ show: true, type, title, message });
  };

  const hideNotification = () => {
    setNotification((prev) => ({ ...prev, show: false }));
  };

  const registerRemoteNode = async (e) => {
    e.preventDefault();
    try {
      setLoading(true);
      const registerResponse = await apiCall("authors/signup", "POST", {
        username: remoteNodeCredentials.remoteUsername,
        password: remoteNodeCredentials.remotePassword,
        displayName: remoteNodeCredentials.displayName,
        is_node: true,
        host: remoteNodeCredentials.host,
      });

      if (!registerResponse.ok) {
        console.error("Failed to register remote node");
      }

      const registerResponseData = await registerResponse.json();

      const activateResponse = await apiCall(`authors/${registerResponseData.user.author_id}`, "PUT", {
        state: "ACTIVE",
      });

      if (!activateResponse.ok) {
        console.error("Failed to activate remote node");
      }

      setRemoteNodeCredentials({
        remoteUsername: "",
        remotePassword: "",
        displayName: "",
        remoteHost: "",
      });
      if (activateResponse.ok && registerResponse.ok){
        showNotification("success", "Success", "Remote node registered successfully!");
      }
    } catch (error) {
      showNotification("error", "Something went wrong", "Failed to register node");
    } finally {
      setLoading(false);
    }
  };

  const createHomeNodeCredentials = async (e) => {
    e.preventDefault();
    try {
      setLoading(true);
      const response = await apiCall("register/", "POST", {
        host: homeCredentials.host,
        username: homeCredentials.homeUsername,
        password: homeCredentials.homePassword,
      });

      if (response.ok) {
        const responseIsActive = await apiCall("register/", "PUT", {
          host: homeCredentials.host,
          is_active: "true",
        });

        if (responseIsActive) {
          showNotification(
            "success",
            "Successfully Created Credentials!",
            "Credentials ready to send to remote node!"
          );
          setHomeCredentials({
            homeUsername: "",
            homePassword: "",
            host: "",
          });
        }
      }
    } catch (error) {
      showNotification("error", "Something Went Wrong", error.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="node-registration">
      <Notification
        show={notification.show}
        type={notification.type}
        title={notification.title}
        message={notification.message}
        onClose={hideNotification}
      />
      <h1 className="page-title">Register Node</h1>
      <div className="registration-container">
        <form className="registration-card" onSubmit={createHomeNodeCredentials}>
          <h2 className="card-title">Send Remote</h2>
          <p className="card-description">
            Credentials for this node to send to remote node
          </p>

          <div className="form-group">
            <label htmlFor="home-username">Username</label>
            <input
              id="home-username"
              type="text"
              name="homeUsername"
              autoComplete="off"
              value={homeCredentials.homeUsername}
              onChange={handleHomeCredentialsChange}
              placeholder="Username for this node"
              className="input-field"
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="home-password">Password</label>
            <input
              id="home-password"
              type="password"
              name="homePassword"
              autoComplete="new-password"
              value={homeCredentials.homePassword}
              onChange={handleHomeCredentialsChange}
              placeholder="Password for this node"
              className="input-field"
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="home-host">Host URL</label>
            <input
              id="home-host"
              type="text"
              name="host"
              value={homeCredentials.host}
              onChange={handleHomeCredentialsChange}
              placeholder="http://yourdomain.com/api/"
              className="input-field"
              required
            />
          </div>

          <div className="form-group button-row">
            <button
              className="submit-button"
              type="submit"
              disabled={loading}
            >
              Submit
            </button>
          </div>
        </form>

        <form className="registration-card" onSubmit={registerRemoteNode}>
          <h2 className="card-title">Creating Credentials For Remote Node</h2>
          <p className="card-description">
            Register a remote node on this server
          </p>

          <div className="form-group">
            <label htmlFor="remote-username">Username</label>
            <input
              id="remote-username"
              type="text"
              name="remoteUsername"
              value={remoteNodeCredentials.remoteUsername}
              onChange={handleRemoteCredentialsChange}
              placeholder="Remote node username"
              className="input-field"
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="remote-password">Password</label>
            <input
              id="remote-password"
              type="password"
              name="remotePassword"
              autoComplete="new-password"
              value={remoteNodeCredentials.remotePassword}
              onChange={handleRemoteCredentialsChange}
              placeholder="Remote node password"
              className="input-field"
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="remote-displayName">Display Name</label>
            <input
              id="remote-displayName"
              type="text"
              name="displayName"
              value={remoteNodeCredentials.displayName}
              onChange={handleRemoteCredentialsChange}
              placeholder="Display name for remote node"
              className="input-field"
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="remote-host">Host</label>
            <input
              id="remote-host"
              type="text"
              name="remoteHost"
              value={remoteNodeCredentials.remoteHost}
              onChange={handleRemoteCredentialsChange}
              placeholder="http://remotenode.com/api/"
              className="input-field"
              required
            />
          </div>

          <div className="form-group button-row">
            <button
              className="submit-button"
              type="submit"
              disabled={loading}
            >
              Submit
            </button>
          </div>
        </form>
      </div>

      <div className="setup-process">
        <h3 className="process-title">Setup Process:</h3>
        <ol className="process-steps">
          <li>Create your credentials to send to the remote node (left panel)</li>
          <li>The remote node will use these to register your node on their server</li>
          <li>Enter the remote node's credentials on your server (right panel)</li>
        </ol>
      </div>
    </div>
  );
};

export default NodeRegistration;