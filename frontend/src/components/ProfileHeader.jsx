import backBtn from "../assets/icons/back.png";
import editBtn from "../assets/icons/edit.png";

export default function ProfileHeader(user_properties) {
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
            <img id="profile-image" src={user_properties.profilepic} />
            <div class="info-names-wrapper">
              <p id="displayname">{user_properties.displayname}</p>
              <div class="info-names-subwrapper">
                <p id="username">{user_properties.username}</p>
                <p>|</p>
                <p id="github">{user_properties.github}</p>
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
