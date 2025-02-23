import ProfileHeader from "../components/ProfileHeader";
import profilePic from "../assets/sample-images/party.jpg";
import "../assets/styles/profile-header.css";
import "../assets/styles/user-profile.css";
import { useParams } from "react-router-dom";

export default function UserProfile() {
  const { authorId } = useParams();

  return (
    <div className="profile-page-wrapper">
      <ProfileHeader
        displayname="John Doe"
        username="johnDoe"
        github="github"
        profilepic={profilePic}
      />
      <div className="feed-container"></div>
    </div>
  );
}
