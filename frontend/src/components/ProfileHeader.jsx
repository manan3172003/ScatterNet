import editBtn from "../assets/icons/edit.png";
import { UserContext } from "../pages/UserProfile";
import { useContext, useState, useEffect } from "react";
import { AuthContext } from "../context/AuthContext";
import {useNavigate, useParams} from "react-router-dom";
import { Link } from "react-router";
import {getAuthorRelationship, getFollowers, getFollowing, handleFollowRequest} from "../utils/followApi.js";
import {getAuthorObject} from "../utils/utils.js";

export default function ProfileHeader() {
  const user = useContext(UserContext);
  const [currentUser, setCurrentUser] = useState();
  const [isOwner, setIsOwner] = useState(null);
  const [authorsRelationship, setAuthorsRelationship] = useState("");
  const [followerCount, setFollowerCount] = useState(null);
  const [followingCount, setFollowingCount] = useState(null);
  const { authorId } = useParams();
  const navigate = useNavigate();

  async function fetchUserData() {
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
        await fetchFollowCounts(data.user);
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

  async function fetchFollowStatus() {
    // TODO: otherAuthor is just the author id atm, will need tweaks eventually?
    const relationship = await getAuthorRelationship(authorId);
    setAuthorsRelationship(relationship);
  }

  async function fetchFollowCounts(){
    console.log(user, "h");
    try {
      const followerResponse = await getFollowers(user);
      const followingResponse = await getFollowing(user);

      if (followerResponse && followerResponse.followers) {
        setFollowerCount(followerResponse.followers.length);
      } else {
        setFollowerCount(0);
      }

      if (followingResponse && followingResponse.following) {
        setFollowingCount(followingResponse.following.length);
      } else {
        setFollowingCount(0);
      }
    }
    catch (error) {
        console.error("Error fetching follow counts: ", error);
    }
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

  async function handleNavigation(mode) {
    navigate(`/${mode}`);
  }

  return (
    <div className="profile-header">
      <div class="cover-wrapper">
        <div class="info-wrapper">
          <div className="info-subwrapper">
            <img id="profile-image" src={user.profileImage || `https://robohash.org/${user.displayName}.png`}/>

            <div className="name-follow-container">
              <div className="info-names-wrapper">
                <p id="displayname">{user.displayName}</p>
                {!isOwner && (
                  <button
                      className="button"
                      onClick={handleFollow}
                      disabled={authorsRelationship === "Requested"
                      }>
                    <p>{authorsRelationship === "Not Following" ? "Follow" : authorsRelationship}</p>
                  </button>
              )}
              {isOwner && (
                  <Link to="/editProfile" className="link-button">
                      <p>Edit Profile</p>
                  </Link>
              )}
              </div>

              <div id="follow-info">
                <div className="follow-data">
                  <span>{followerCount}</span>
                  <button onClick={() => handleNavigation("followers")}>Followers</button>
                </div>
                <div className="follow-data">
                  <span>{followingCount}</span>
                  <button onClick={() => handleNavigation("following")}>Following</button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
