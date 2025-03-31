import "../assets/styles/author-card.css";
import { useContext, useState } from "react";
import {AuthContext} from "../context/AuthContext";
import {getAuthorObject} from "../utils/utils.js";
import {sendRemoteFollowRequest} from "../utils/remoteAuthorsApi.js";

export default function AuthorCard({ author }) {
    const [isFollowing, setIsFollowing] = useState(false);
    const { user } = useContext(AuthContext);

    async function handleFollow() {
        const user_author = await getAuthorObject(user);
        const follow_success = await sendRemoteFollowRequest(user_author, author);
        setIsFollowing(follow_success);
    }

    return (
        <div className="author-card">
            <img
                className="author-image"
                src={author.profileImage}
                alt={`${author.displayName}'s profile`}
            />
            <h3 className="author-name">{author.displayName}</h3>
            <p className="author-host">{author.host}</p>
            <button
                className="follow-button"
                onClick={handleFollow}
                disabled={isFollowing}
            >{isFollowing? "Following" : "Follow"}
            </button>
        </div>
    )
}
