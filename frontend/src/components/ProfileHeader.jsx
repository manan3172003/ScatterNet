import backBtn from "../assets/icons/back.png";
import editBtn from "../assets/icons/edit.png";
import { UserContext } from "../pages/UserProfile";
import { useContext } from "react";

export default function ProfileHeader() {
  const user = useContext(UserContext);
  return (
    <div className="profile-header">
      <div class="cover-wrapper">
        <div class="cover-buttons-wrapper">
          <div>
            <img id="back-btn" src={backBtn} />
          </div>
          <div>
            <img id="edit-btn" src={editBtn} />
          </div>
        </div>
        <div class="info-wrapper">
          <div class="info-subwrapper">
            <img id="profile-image" src={user.profileImageURL} />
            <div class="info-names-wrapper">
              <p id="displayname">{user.displayName}</p>
              <div class="info-names-subwrapper">
                <p id="username">{user.username}</p>
                <p>|</p>
                <p id="github">{user.github}</p>
              </div>
            </div>
          </div>
          <div class="button" id="follow-btn">
            <p>follow</p>
          </div>
        </div>
      </div>
    </div>
  );
}
