export default function ProfileHeader() {
  return (
    <header>
      <div class="cover-wrapper">
        <img id="cover-image" src="assets/stadium.jpg" />
        <div class="cover-buttons-wrapper">
          <div id="back-btn">
            <img src="assets/back.png" />
          </div>
          <div id="edit-btn">
            <img src="assets/edit.png" />
          </div>
        </div>
        <div class="info-wrapper">
          <img id="profile-image" src="assets/party.jpg" />
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
