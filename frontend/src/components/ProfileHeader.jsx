import editBtn from "../assets/icons/edit.png";
import { UserContext } from "../pages/UserProfile";
import { useContext, useState, useEffect } from "react";
import { AuthContext } from "../context/AuthContext";
import { useParams } from "react-router-dom";
import { Link } from "react-router";

export default function ProfileHeader() {
  const user = useContext(UserContext);
  const [currentUser, setCurrentUser] = useState();
  const [isOwner, setIsOwner] = useState(null);
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
  useEffect(() => {
    fetchUserData();
  }, [user]);

  useEffect(() => {
    console.log(
      `cur: ${
        currentUser?.author_id
      }  viewing: ${authorId}   owner?${isOwner},${
        currentUser?.author_id === authorId
      }`
    );
  }, [currentUser]); // Re-run when currentUser updates

  // useEffect(() => {
  //   //determine if user is owner of page
  //   if (currentUser && authorId) {
  //     setIsOwner(currentUser.id === authorId);
  //   }
  // }, [currentUser, authorId]);

  async function getRelationship() {
    //check if current user is following profile page's user
    const response = await fetch(
      `http://localhost:8000/api/authors/${currentUser.id}/following/${user.id}`
    );

    return !!response.ok;
  }
  async function followUser() {
    //TODO
    console.log("follow user");
  }
  return (
    <div className="profile-header">
      <div class="cover-wrapper">
        <div class="info-wrapper">
          <div class="info-subwrapper">
            <img id="profile-image" src={user.profileImageURL} />
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
              <div class="button" id="follow-btn" onClick={() => followUser()}>
                <p>follow</p>
              </div>
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
