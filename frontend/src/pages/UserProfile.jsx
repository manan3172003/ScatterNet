import ProfileHeader from "../components/ProfileHeader";
import "../assets/styles/profile-header.css";
import { useParams } from "react-router-dom";

export default function UserProfile() {
  const { authorId } = useParams();
  return (
    <div className="profile-container">
      <ProfileHeader />
      <div className="feed-container"></div>
    </div>
  );
}
