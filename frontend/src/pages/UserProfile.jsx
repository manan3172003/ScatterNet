import ProfileHeader from "../components/ProfileHeader";
import Navbar from "../components/Navbar";
import "../assets/styles/profile-header.css";
import "../assets/styles/user-profile.css";
import { useParams } from "react-router-dom";

export default function UserProfile() {
  const { authorId } = useParams();

  return (
    <div className="profile-page-wrapper">
      <ProfileHeader />
      <div className="feed-container"></div>
    </div>
  );
}
