import ProfileHeader from "../components/ProfileHeader";
import "../assets/styles/profile-header.css";

export default function UserProfile() {
  return (
    <div className="profile-container">
      <ProfileHeader />
      <div className="feed-container"></div>
    </div>
  );
}
