import "../assets/styles/authors-list.css";
import {useContext, useEffect, useState} from "react";
import {
  getAuthorRelationship, getFollowers,
  getFollowing,
  getFollowRequests,
  handleFollowRequest,
  handleRespondingToFollowRequest
} from "../utils/followApi.js";
import {AuthContext} from "../context/AuthContext.jsx";
import {getAuthorObject} from "../utils/utils.js";
import {useNavigate} from "react-router-dom";

export default function AuthorsList({ chosenMode }) {
    const { user } = useContext(AuthContext);
    const [authors, setAuthors] = useState([]);
    const navigate = useNavigate();

  async function fetchAuthors() {
    const currAuthor = await getAuthorObject(user);

      if (chosenMode === "Requests") {
        const fetchedAuthors = await getFollowRequests(currAuthor);
        setAuthors(fetchedAuthors.followers || []);
      }
      else if (chosenMode === "Following") {
        const fetchedAuthors = await getFollowing(currAuthor);
        setAuthors(fetchedAuthors.following || []);
      }
      else if (chosenMode === "Followers") {
        const fetchedAuthors = await getFollowers(currAuthor);
        setAuthors(fetchedAuthors.followers || []);
      }
  }

  // When we are in the followers/following mode
  async function handleModeChange(newMode) {
    navigate(`/${newMode.toLowerCase()}`);
  }

  useEffect(() => {
      fetchAuthors();
  }, [chosenMode]);

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
    await handleRespondingToFollowRequest(user, otherAuthor, authorResponse);

    // Make the component re-render
    await fetchAuthors();
  }

  return (
    <div className="table-container">
      <div className="table-content">
        <div className="table-header">
          <h2>{chosenMode}</h2>
          {chosenMode !== "Requests" &&
            <div className="header-buttons">
              <button
                  onClick={() => handleModeChange("Followers")}
                  className={`btn ${chosenMode === "Followers" ? "selected" : ""}`}
                  disabled={chosenMode === "Followers"}
              >
                Followers
              </button>
              <button
                  onClick={() => handleModeChange("Following")}
                  className={`btn ${chosenMode === "Following" ? "selected" : ""}`}
                  disabled={chosenMode === "Following"}
              >
                Following
              </button>
            </div>
          }
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
                  <td className="author-name">{author.displayName}</td>
                  <td className="actions-cell">
                    {chosenMode === "Requests" ? (
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
                      ) : chosenMode === "Following" ? (
                          <button
                              className="btn-action btn-unfollow"
                              onClick={() => handleUnfollow(author)}
                          >
                            Unfollow
                          </button>
                    ) : null}
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