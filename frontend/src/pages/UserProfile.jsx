import ProfileHeader from "../components/ProfileHeader";
import Feed from "../components/Feed";
import "../assets/styles/profile-header.css";
import "../assets/styles/user-profile.css";
import { useParams } from "react-router-dom";
import { useState, createContext, useContext, useEffect } from "react";
import { AuthContext } from "../context/AuthContext";

export const UserContext = createContext();

export default function UserProfile() {
  const { authorId } = useParams();

  const [loading, setLoading] = useState(true);
  const [user, setUser] = useState();

  useEffect(() => {
    async function fetchUser() {
      try {
        const response = await fetch(
          `http://localhost:8000/api/authors/${authorId}`
        );
        if (!response.ok) throw new Error("User not found");
        const data = await response.json();
        setUser(data);
      } catch (error) {
        console.error("Error fetching user:", error);
      } finally {
        setLoading(false);
      }
    }

    fetchUser();
  }, [authorId]);

  return (
    <UserContext.Provider value={user}>
      {loading ? (
        <p>loading...</p>
      ) : user ? (
        <div className="profile-page-wrapper">
          <ProfileHeader />
          <div className="feed-container">
            <Feed />
          </div>
        </div>
      ) : (
        <p>User not found</p>
      )}
    </UserContext.Provider>
  );
}
