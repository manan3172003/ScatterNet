import editBtn from "../assets/icons/edit.png";
import { UserContext } from "../pages/UserProfile";
import { useContext, useState, useEffect } from "react";
import { AuthContext } from "../context/AuthContext";
import { useParams } from "react-router-dom";
import { Link } from "react-router";
import {getAuthorRelationship, handleFollowRequest} from "../utils/followApi.js";
import {getAuthorObject} from "../utils/utils.js";

export default function ProfileHeader() {
  const user = useContext(UserContext);
  const [currentUser, setCurrentUser] = useState();
  const [isOwner, setIsOwner] = useState(null);
  const [authorsRelationship, setAuthorsRelationship] = useState("Same Author");
  const { authorId } = useParams();
  //const { currentUser } = useContext(AuthContext);
  const fetchUserData = async () => {
    try {
      const response = await fetch(
        "http://localhost:8000/api/authors/current-user",
        {
          method: "GET",
          credentials: "include",
          headers: {
            "Content-Type": "application/json",
          },
        }
      );

      if (response.ok) {
        const data = await response.json();
        setCurrentUser(data.user);
        // Set isOwner state
        setIsOwner(String(data.user.author_id) === String(authorId));
      } else {
        setCurrentUser(null);
        setIsOwner(false);
      }
    } catch (error) {
      console.error("Error fetching user data:", error);
      setCurrentUser(null);
      setIsOwner(false);
    }
  };

  const fetchFollowStatus = async () => {
    // TODO: otherAuthor is just the author id atm, will need tweaks eventually?
    const relationship = await getAuthorRelationship(authorId);
    setAuthorsRelationship(relationship);
  }

  useEffect(() => {
    fetchUserData();
    fetchFollowStatus();
  }, []);

  async function handleFollow() {
    const currAuthor = await getAuthorObject(currentUser);
    const newRelationship = await handleFollowRequest(currAuthor, authorId, authorsRelationship);
    setAuthorsRelationship(newRelationship);
  }

  // useEffect(() => {
  //   //determine if user is owner of page
  //   if (currentUser && authorId) {
  //     setIsOwner(currentUser.id === authorId);
  //   }
  // }, [currentUser, authorId]);

  return (
    <div className="profile-header">
      <div class="cover-wrapper">
        <div class="info-wrapper">
          <div class="info-subwrapper">
            <img id="profile-image" src={user.profileImageURL || `https://robohash.org/${user.displayName}.png`} />
            <div class="info-names-wrapper">
              <p id="displayname">{user.displayName}</p>
              <div class="info-names-subwrapper">
                <a id="github" href={user.github}>
                  Github
                </a>
              </div>
            </div>
          </div>
          <div class="buttons-wrapper">
            {!isOwner && (
              <button
                  className="button"
                  id="follow-btn"
                  onClick={handleFollow}
                  disabled={authorsRelationship === "Requested"
              }>
                <p>{authorsRelationship === "Not Following" ? "Follow" : authorsRelationship}</p>
              </button>
            )}
            {isOwner && (
              <Link to="/editProfile" id="edit-btn">
                <div class="button" id="edit-btn">
                  <p>edit profile</p>
                </div>
              </Link>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
