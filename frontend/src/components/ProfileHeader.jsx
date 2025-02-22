import profilePic from "../assets/sample-images/party.jpg";
import profileCover from "../assets/sample-images/stadium.jpg";
import backBtn from "../assets/icons/back.png";
import editBtn from "../assets/icons/edit.png";
export default function ProfileHeader() {
  return (
    <header>
      <div class="cover-wrapper">
        <img id="cover-image" src={profileCover} />
        <div class="cover-buttons-wrapper">
          <div id="back-btn">
            <img src={backBtn} />
          </div>
          <div id="edit-btn">
            <img src={editBtn} />
          </div>
        </div>
        <div class="info-wrapper">
          <img id="profile-image" src={profilePic} />
          <div class="info-names-wrapper">
            <p id="displayname">Meghan</p>
            <div class="info-names-subwrapper">
              <p id="username">meghanmarie</p>
              <p>|</p>
              <p id="github">meghanwickstrand</p>
            </div>
          </div>
          <div class="button" id="follow-btn">
            <p>follow</p>
          </div>
        </div>
      </div>
    </header>
  );
}
