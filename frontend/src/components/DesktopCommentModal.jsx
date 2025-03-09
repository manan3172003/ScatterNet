/* eslint-disable react/prop-types */
import { useState, useContext, useEffect, useRef } from "react";
import ReactMarkdown from "react-markdown";
import getCookie from "../context/Cookie";
import { X, Heart } from "lucide-react";
import "../assets/styles/desktop-comment-modal.css";
import { AuthContext } from "../context/AuthContext";
import Post from "./Post"; 

export default function DesktopCommentModal({ post, onClose }) {
    const [newComment, setNewComment] = useState("");
    const [comments, setComments] = useState(post.comments.src || []);
    const [isMarkdown, setIsMarkdown] = useState(false);
    const commentListRef = useRef(null);
    
    const { user } = useContext(AuthContext);
    
    useEffect(() => {
        fetchComments();
        
        // Prevent scrolling on the body when modal is open
        document.body.style.overflow = 'hidden';
        return () => {
            document.body.style.overflow = '';
        };
    }, []);
    
    const csrfToken = getCookie('csrftoken');
    
    async function fetchComments() {
        try {
            const response = await fetch(`http://localhost:8000/api/posts/${post.id}`);
            if (response.ok) {
                const data = await response.json();
                setComments(data.comments.src || []);
            }
        } catch (error) {
            console.error("Error fetching comments:", error);
        }
    }
    
    async function handleLike(commentId) {
        try {
            const response = await fetch(`http://localhost:8000/api/like`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": csrfToken,
                },
                body: JSON.stringify({
                    "author_id": `${user.author_id}`,
                    "object": `${commentId}`,
                }),
                credentials: "include"
            });
            
            if (response.ok) {
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
            const response = await fetch(`http://localhost:8000/api/authors/${user.author_id}/commented`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": csrfToken
                },
                body: JSON.stringify({
                    "post": `${post.id}`,
                    "comment": `${newComment}`,
                    "contentType": contentType,
                }),
                credentials: "include",
            });
            
            if (response.ok) {
                setNewComment("");
                fetchComments();
            }
        } catch (error) {
            console.error("Error posting comment:", error);
        }
    }
    
    
    const dummyClick = (e) => {
        e.stopPropagation();
    };
    
    return (
        <div className="desktop-modal-overlay" onClick={onClose}>
            <div className="desktop-modal-container" onClick={(e) => e.stopPropagation()}>
                <button className="desktop-close-btn" onClick={onClose}>
                    <X size={24} />
                </button>
                
                <div className="desktop-modal-content">
                    <div className="desktop-post-wrapper">
                        <Post 
                            post={post} 
                            onPostClick={dummyClick} 
                            onCommentClick={dummyClick}
                            hideCommentsButton={true}
                        />
                    </div>
                    
                    <div className="desktop-comments-container">
                        <div className="desktop-comments-header">
                            <h3>Comments</h3>
                        </div>
                        
                        <div className="desktop-comments-list" ref={commentListRef}>
                            {comments.length > 0 ? (
                                comments.map((comment) => (
                                    <div key={comment.id} className="desktop-comment-item">
                                        <img
                                            className="desktop-comment-avatar"
                                            src={comment.author.profileImageURL}
                                            
                                        />
                                        <div className="desktop-comment-content">
                                            <div>
                                                <span className="desktop-comment-author">
                                                    {comment.author.displayName}
                                                </span>
                                                {comment.contentType === "text/markdown" ? (
                                                    <ReactMarkdown>
                                                        {comment.comment}
                                                    </ReactMarkdown>
                                                ) : (
                                                    <span className="desktop-comment-text">{comment.comment}</span>
                                                )}
                                            </div>
                                            <div className="desktop-comment-meta">
                                                <span className="desktop-comment-time">
                                                    {new Date(comment.published).toLocaleDateString(undefined, {
                                                        hour: '2-digit',
                                                        minute: '2-digit'
                                                    })}
                                                </span>
                                                {comment.likes.count > 0 && (
                                                    <span className="desktop-like-count">{comment.likes.count} likes</span>
                                                )}
                                               
                                            </div>
                                        </div>
                                        <button 
                                            className="desktop-like-btn"
                                            onClick={() => handleLike(comment.id)}
                                        >
                                            <Heart size={12} />
                                        </button>
                                    </div>
                                ))
                            ) : (
                                <div className="desktop-no-comments">
                                    <p>No comments yet. Be the first to comment!</p>
                                </div>
                            )}
                        </div>
                        
                        <div className="desktop-comment-input">
                            <div className="desktop-format-toggle">
                                <button
                                    type="button"
                                    className={`desktop-toggle-btn ${!isMarkdown ? 'active' : ''}`}
                                    onClick={() => setIsMarkdown(false)}
                                >
                                    Plain Text
                                </button>
                                <button
                                    type="button"
                                    className={`desktop-toggle-btn ${isMarkdown ? 'active' : ''}`}
                                    onClick={() => setIsMarkdown(true)}
                                >
                                    Markdown
                                </button>
                            </div>
                            <form onSubmit={handleAddComment} className="desktop-comment-form">
                                <input
                                    type="text"
                                    value={newComment}
                                    onChange={(e) => setNewComment(e.target.value)}
                                    placeholder="Add a comment..."
                                    className="desktop-input-field"
                                />
                                <button
                                    type="submit"
                                    className="desktop-post-btn"
                                    disabled={!newComment.trim()}
                                >
                                    Post
                                </button>
                            </form>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}
