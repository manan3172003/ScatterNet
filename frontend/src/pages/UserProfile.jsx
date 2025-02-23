import ProfileHeader from "../components/ProfileHeader";
import profilePic from "../assets/sample-images/party.jpg";
import "../assets/styles/profile-header.css";
import "../assets/styles/user-profile.css";
import { useParams } from "react-router-dom";
import { useState, createContext, useContext } from "react";

export const UserContext = createContext();

export default function UserProfile() {
  const { authorId } = useParams();
  console.log(authorId);

  const [user, setUser] = useState({
    displayname: "John Doe",
    username: "johnDoe",
    github: "github/jdoe",
    profilepic: profilePic,
  });

  return (
    <UserContext.Provider value={user}>
      <div className="profile-page-wrapper">
        <ProfileHeader />
        <div className="feed-container"></div>
      </div>
    </UserContext.Provider>
  );
}
