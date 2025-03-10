import "../assets/styles/authors-list.css";
import {useContext, useEffect, useState} from "react";
import {
  getFollowing,
  getFollowRequests,
  handleFollowRequest,
  handleRespondingToFollowRequest
} from "../utils/followApi.js";
import {AuthContext} from "../context/AuthContext.jsx";
import {getAuthorObject} from "../utils/utils.js";

export default function AuthorsList() {
    const { user } = useContext(AuthContext);
    const [mode, setMode] = useState("Requests");
    const [authors, setAuthors] = useState([]);

  async function fetchAuthors() {
      if (mode === "Requests") {
        const fetchedAuthors = await getFollowRequests(user);
        setAuthors(fetchedAuthors.followers || []);
      }
      else if (mode === "Following") {
        const fetchedAuthors = await getFollowing(user);
        setAuthors(fetchedAuthors.following || []);
      }
  }

  useEffect(() => {
    fetchAuthors();
  }, [mode]);

  async function handleUnfollow(otherAuthor){
    // TODO: remove this someday
    const parts = otherAuthor.id.split("/");
    const otherAuthorId = parts[parts.length - 1];

    const currAuthor = await getAuthorObject(user);
    await handleFollowRequest(currAuthor, otherAuthorId, "Following");

    // Fetch latest data when an unfollow happens
    await fetchAuthors();
  }

  async function handleResponseToFollowRequest(otherAuthor, authorResponse) {
    console.log(user);
    await handleRespondingToFollowRequest(user, otherAuthor, authorResponse);

    // Make the component re-render
    await fetchAuthors();
  }

  return (
    <div className="table-container">
      <div className="table-content">
        <div className="table-header">
          <h2>{mode}</h2>
          <div className="header-buttons">
            <button
                onClick={() => setMode("Requests")}
                className={`btn ${mode === "Requests" ? "selected" : ""}`}
                disabled={mode === "Requests"}
            >
              Requests
            </button>
            <button
                onClick={() => setMode("Following")}
                className={`btn ${mode === "Following" ? "selected" : ""}`}
                disabled={mode === "Following"}
            >
              Following
            </button>
          </div>
        </div>
        <div className="table-scroll">
          <table>
            <thead>
              <tr>
                <th className="name-column">Name</th>
                <th className="actions-column">Actions</th>
              </tr>
            </thead>
            <tbody>
              {authors.map((author) => (
                <tr key={author.id}>
                  <td>{author.displayName}</td>
                  <td className="actions-cell">
                    {mode === "Requests" ? (
                        <>
                          <button
                              onClick={() => handleResponseToFollowRequest(author, "Accept")}
                              className="btn-action btn-accept"
                          >
                            Accept
                          </button>
                          <button
                              onClick={() => handleResponseToFollowRequest(author, "Reject")}
                              className="btn-action btn-reject"
                          >
                            Reject
                          </button>
                        </>
                      ) : (
                          <button
                              className="btn-action btn-unfollow"
                              onClick={() => handleUnfollow(author)}
                          >
                            Unfollow
                          </button>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}