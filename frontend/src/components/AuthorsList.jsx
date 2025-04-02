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
import {getAuthorObject, getAuthorObjectById} from "../utils/utils.js";
import {useNavigate, useParams} from "react-router-dom";

export default function AuthorsList({ chosenMode }) {
    const { user } = useContext(AuthContext);
    const [authors, setAuthors] = useState([]);
    const [sameAuthor, setSameAuthor] = useState(false);
    const navigate = useNavigate();
    const { authorId } = useParams();

  async function fetchAuthors() {
    try {
      const currAuthor = authorId
        ? await getAuthorObjectById(authorId)
        : await getAuthorObject(user);

    const relationship = await getAuthorRelationship(currAuthor);
    setSameAuthor(relationship === "Same Author");

    let fetchedAuthors = [];
    if (chosenMode === "Requests") {
      fetchedAuthors = (await getFollowRequests(currAuthor)).followers || [];
    }
    else if (chosenMode === "Following") {
      fetchedAuthors = (await getFollowing(currAuthor)).following || [];
    }
    else if (chosenMode === "Followers") {
      fetchedAuthors = (await getFollowers(currAuthor)).followers || [];
    }

    setAuthors(fetchedAuthors);
    }
    catch (error) {
      console.error("Error fetching authors:", error);
      setAuthors([]);
    }
  }

  useEffect(() => {
      fetchAuthors();
  }, [authorId, chosenMode]);

  async function handleUnfollow(otherAuthor){
    const currAuthor = await getAuthorObject(user);
    await handleFollowRequest(currAuthor, otherAuthor, "Following");

    // Fetch latest data when an unfollow happens
    await fetchAuthors();
  }

  async function handleResponseToFollowRequest(otherAuthor, authorResponse) {
    let currAuthor = await getAuthorObject(user);
    await handleRespondingToFollowRequest(currAuthor, otherAuthor, authorResponse);

    // Make the component re-render
    await fetchAuthors();
  }

  // When we are in the followers/following mode
  async function handleModeChange(newMode) {
    navigate(`/authors/${authorId}/${newMode.toLowerCase()}`);
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
                  <td>{author.displayName}</td>
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
                      ) : chosenMode === "Following" && sameAuthor ? (
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