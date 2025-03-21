/* eslint-disable react/prop-types */
import { useState, useContext, useEffect, useRef } from "react";
import ReactMarkdown from "react-markdown";
import getCookie from "../context/Cookie";
import { X, Send, Heart } from "lucide-react";
import "../assets/styles/mobile-comment-modal.css";
import { motion } from "framer-motion";
import { AuthContext } from "../context/AuthContext";
import {apiCall} from "../utils/utils.js";

export default function MobileCommentModal({ post, onClose }) {
    const [newComment, setNewComment] = useState("");
    const [comments, setComments] = useState(post.comments.src || []);
    const [isMarkdown, setIsMarkdown] = useState(false);
    const commentListRef = useRef(null);
    
    const { user } = useContext(AuthContext);
    
   
    useEffect(() => {
        fetchComments();
    }, []);
    
    // Scrolling to bottom when new comments are added 
    useEffect(() => {
        if (commentListRef.current) {
            commentListRef.current.scrollTop = commentListRef.current.scrollHeight;
        }
    }, [comments]);
    
    async function fetchComments() {
        try {
            const response = await apiCall(`posts/${post.id}/comments`);
            if (response.ok) {
                const data = await response.json();
                setComments(data.src || []);
            }
        } catch (error) {
            console.error("Something went wrong:", error);
        }
    }
    
    async function handleLike(commentId) {
        try {
            const response = await apiCall(`like`,
                "POST",
                {
                    "author_id": `${user.author_id}`,
                    "object": `${commentId}`,
                }
                );
            
            if (response.ok) {
                // Once we like a comment we need to fetch the comments again to  get realtime updates
                fetchComments();
            }
        } catch (error) {
            console.error("Error liking comment:", error);
        }
    }
    
    async function handleAddComment(e) {
        e.preventDefault();
        if (!newComment.trim()) return;
        
        const contentType = isMarkdown ? "text/markdown" : "text/plain";
        
        try {
            const response = await apiCall(`authors/${user.author_id}/commented`,
                "POST",
                {
                    "post": `${post.id}`,
                    "comment": `${newComment}`,
                    "contentType": contentType,
                }
            );
            
            if (response.ok) {
                setNewComment("");
                fetchComments();
            }
        } catch (error) {
            console.error("Error posting comment:", error);
        }
    }
    
    return (
        <motion.div
            initial={{ y: "100%" }}
            animate={{ y: 0 }}
            exit={{ y: "100%" }}
            transition={{ type: "spring", stiffness: 300, damping: 30 }}
            className="comment-modal"
        >
            <div className="modal-header">
                <button onClick={onClose} className="back-btn">
                    <X className="icon" />
                </button>
                <h2>Comments</h2>
                <div className="header-spacer"></div>
            </div>
            
            <div className="comment-list" ref={commentListRef}>
                {comments.length > 0 ? (
                    comments.map((comment) => (
                        <div key={comment.id} className="comment-item">
                            <div className="comment-avatar">
                                <img
                                    className="comment-pfp"
                                    src={comment.author.profileImage || `https://robohash.org/${comment.author.displayName}.png`}
                                    
                                />
                            </div>
                            <div className="comment-body">
                                <div className="comment-content">
                                    <span className="comment-author">
                                        {comment.author.displayName}
                                    </span>
                                    {comment.contentType === "text/markdown" ? (
                                        <ReactMarkdown>
                                            {comment.comment}
                                        </ReactMarkdown>
                                    ) : (
                                        <span className="comment-text">{comment.comment}</span>
                                    )}
                                </div>
                                <div className="comment-meta">
                                    <span className="comment-time">
                                        {new Date(comment.published).toLocaleDateString(undefined, {
                                            hour: '2-digit',
                                            minute: '2-digit'
                                        })}
                                    </span>
                                    <button className="like-btn" onClick={() => handleLike(comment.id)}>
                                        {comment.likes.count > 0 ? `${comment.likes.count} likes` : "0 Likes"}
                                    </button>
                                   
                                </div>
                            </div>
                            <div className="comment-actions">
                                <Heart
                                    size={16}
                                    className={`like-icon ${comment.likes.count > 0 ? 'liked' : ''}`}
                                    onClick={() => handleLike(comment.id)}
                                />
                            </div>
                        </div>
                    ))
                ) : (
                    <div className="no-comments">
                        <p>No comments yet. Be the first to comment!</p>
                    </div>
                )}
            </div>
            
            <div className="comment-input-container">
                <div className="format-toggle">
                    <button
                        type="button"
                        className={`toggle-btn ${!isMarkdown ? 'active' : ''}`}
                        onClick={() => setIsMarkdown(false)}
                    >
                        Plain Text
                    </button>
                    <button
                        type="button"
                        className={`toggle-btn ${isMarkdown ? 'active' : ''}`}
                        onClick={() => setIsMarkdown(true)}
                    >
                        Markdown
                    </button>
                </div>
                <form onSubmit={handleAddComment} className="comment-form">
                    <input
                        type="text"
                        value={newComment}
                        onChange={(e) => setNewComment(e.target.value)}
                        placeholder={`Add a comment for ${post.author.displayName}...`}
                        className="input-field"
                    />
                    <button
                        type="submit"
                        className="send-btn"
                        disabled={!newComment.trim()}
                    >
                        <Send className="icon" />
                    </button>
                </form>
            </div>
        </motion.div>
    );
}
