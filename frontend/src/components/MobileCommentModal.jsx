/* eslint-disable react/prop-types */
import { useState, useContext } from "react";

import { X, Send, Heart } from "lucide-react";
import "../assets/styles/mobile-comment-modal.css"
import {motion} from "framer-motion"
import { AuthContext } from "../context/AuthContext";
export default function MobileCommentModal({ post, onClose }) {
    const [newComment, setNewComment] = useState("");
    const [comments, setComments] = useState(post.comments.src);
   
    const {user} = useContext(AuthContext)
    console.log("The mobile comment got renedered")

    const handleLike = async (commentId) => {
        const updated = setComments.map((comment) => {
          if (comment.id === commentId) {
            return { ...comment, likes: { ...comment.likes, count: comment.likes.count + 1 } };
          }
          return comment;
        });
    
    }
    const handleAddComment = (e) => {
        e.preventDefault();
      
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
                <h2>{post.title}</h2>
                <button onClick={onClose} className="close-btn">
                    <X className="icon"/>
                </button>
           </div>
           <div className="comment-list">
            {comments.map((comment) => (
                        <div key={comment.id} className="comment-item">
                            <img 
                                className="comment-pfp"
                                src={comment.author.profileImage}
                                alt={`${comment.author.displayName}'s profile`}
                            />
                            <div className="comment-content">
                                <span className="comment-author">
                                    {comment.author.displayName}
                                </span>
                                <p>{comment.content}</p>
                            </div>
                            <div className="comment-actions">
                                <Heart size={16} className="like-icon" onClick={() => handleLike(comment.id)} />
                                <span className="like-count">{comment.likes.count} likes</span>
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
                        placeholder="Add your comment here....."
                        className="input-field"
                    />
                    <button type="submit" className="send-btn">
                        <Send className="icon"/>
                    </button>

                </form>
           </div>
        </motion.div>
        
    )
}
