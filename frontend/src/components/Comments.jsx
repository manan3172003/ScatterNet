/* eslint-disable react/prop-types */
import { useState } from "react";

export default function Comments({ comments }) {
    const [showAll, setShowAll] = useState(false);
    const displayedComments = showAll ? comments : comments.slice(0, 5);

    return (
        <div className="comments-section">
            {displayedComments.map((comment, index) => (
                <div key={index} className="comment">
                    <img 
                        src={comment.author.profileImage} 
                        alt={`${comment.author.displayName}'s profile`} 
                        className="comment-profile-pic"
                    />
                    <div className="comment-content">
                        <span className="comment-author">{comment.author.displayName}</span>
                        <p className="comment-text">{comment.comment}</p>
                    </div>
                </div>
            ))}
            {comments.length > 5 && !showAll && (
                <button className="view-all-btn" onClick={() => setShowAll(true)}>
                    View all comments
                </button>
            )}
        </div>
    );
}
