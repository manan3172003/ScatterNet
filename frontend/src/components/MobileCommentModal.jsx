/* eslint-disable react/prop-types */
import { useState, useContext } from "react";

import { X, Send } from "lucide-react";
import "../assets/styles/mobile-comment-modal.css"
import "../assets/styles/mobile-comment-modal.css"; 
import { AuthContext } from "../context/AuthContext";
export default function MobileCommentModal({ post, onClose }) {
    const [newComment, setNewComment] = useState("");
    const [comments, setComments] = useState(post.comments.src);
    console.log(comments)
    const {user} = useContext(AuthContext)
    console.log("The mobile comment got renedered")
    

    const handleAddComment = (e) => {
        e.preventDefault();
        if (newComment.trim()) {
        const newCommentObj = {
            id: (comments.length + 1).toString(),
            author: user.displayName,
            content: newComment,
            likes: 0,
        };
        setComments([...comments, newCommentObj]);
        setNewComment("");
        }
    };

    if (!post) {
        return null;
    }

    return (
        <div
        
        >
        <div className="modal-header">
            <h2>{post.title}</h2>
            <button onClick={onClose} className="close-btn">
            <X className="icon" />
            </button>
        </div>
        <div className="comment-list">
            {comments.map((comment) => (
            <div key={comment.id} className="comment-item">
                <img
                src="/placeholder.svg"
                alt={comment.author}
                className="comment-avatar"
                />
                <div className="comment-content">
                <span className="comment-author">{comment.author}</span> {comment.content}
                </div>
            </div>
            ))}
        </div>
        <div className="comment-input">
            <form onSubmit={handleAddComment} className="comment-form">
            <input
                type="text"
                value={newComment}
                onChange={(e) => setNewComment(e.target.value)}
                placeholder="Add a comment..."
                className="input-field"
            />
            <button type="submit" className="send-btn">
                <Send className="icon" />
            </button>
            </form>
        </div>
        </div>
    );
    }
