import profilePic from "../assets/sample-images/party.jpg";
import backBtn from "../assets/icons/back.png";
import editBtn from "../assets/icons/edit.png";

import { useContext, useEffect } from "react";
import { AuthContext } from "../context/AuthContext";

export default function ProfileHeader() {
  const { user } = useContext(AuthContext);

  async function getAuthorObject(user) {
    //get author
    try {
      console.log(user);
      const response = await fetch(
        `http://localhost/api/authors/${user.author_id}`
      );

      if (!response.ok) {
        throw new Error(`Error fetching author: ${response.status}`);
      }

      const authorObject = await response.json();
      return authorObject;
    } catch (error) {
      console.error("Failed to fetch author:", error);
      return null;
    }
  }
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
            <img id="profile-image" src={profilePic} />
            <div class="info-names-wrapper">
              <p id="displayname">Meghan</p>
              <div class="info-names-subwrapper">
                <p id="username">meghanmarie</p>
                <p>|</p>
                <p id="github">meghanwickstrand</p>
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
