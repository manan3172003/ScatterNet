/* eslint-disable react/prop-types */
import { useState, useContext, useEffect, useRef } from "react";
import ReactMarkdown from "react-markdown";
import { X, Heart } from "lucide-react";
import "../assets/styles/desktop-comment-modal.css";
import { AuthContext } from "../context/AuthContext";
import Post from "./Post";
import { apiCall } from "../utils/utils.js";
import {fetchAllComments} from "../utils/commentsAndLikesApi.js";

export default function DesktopCommentModal({ post: initialPost, onClose }) {
  const [newComment, setNewComment] = useState("");
  const [comments, setComments] = useState(initialPost.comments?.src || []);
  const [isMarkdown, setIsMarkdown] = useState(false);
  const commentListRef = useRef(null);
  const [post, setPost] = useState(initialPost);
  const [likedComments, setLikedComments] = useState({});

  const { user } = useContext(AuthContext);

  useEffect(() => {
    fetchComments();
    fetchPost();
    if (user) {
      fetchUserLikes();
    }
    // Prevent scrolling on the body when modal is open
    document.body.style.overflow = "hidden";
    return () => {
      document.body.style.overflow = "";
    };
  }, []);

  async function fetchUserLikes() {
    if (!user) return;
    
    const likedMap = {};
    let currentUrl = `authors/${user.author_id}/liked`;
    
    while (currentUrl) {
      try {
        const response = await apiCall(currentUrl);
        if (!response.ok) break;
        
        const liked = await response.json();
        
        if (liked.src && Array.isArray(liked.src)) {
          liked.src.forEach(like => {
            if (like && like.object) {
              likedMap[like.object] = true;
            }
          });
        }
        
        if (liked.next) {
          const nextUrl = new URL(liked.next);
          let path = nextUrl.pathname;
          const apiPrefix = '/api/';
          
          if (path.includes(apiPrefix)) {
            path = path.substring(path.indexOf(apiPrefix) + apiPrefix.length);
          } else if (path.startsWith('/')) {
            path = path.substring(1);
          }
          
          currentUrl = path + nextUrl.search;
        } else {
          currentUrl = null;
        }
      } catch (error) {
        console.error("Error fetching user likes:", error);
        currentUrl = null;
      }
    }
    
    setLikedComments(likedMap);
  }

  async function fetchPost() {
    try {
      const response = await fetch(`${post.id}`);
      if (!response.ok) {
        throw new Error(`Failed to fetch post: ${response.status}`);
      }
      const updatedPost = await response.json();
      setPost(updatedPost);
    } catch (error) {
      console.error("Error fetching post:", error);
    }
  }

  async function fetchComments() {
    const allComments = await fetchAllComments(post);
    setComments(allComments);
  }
  
  async function handleLike(commentId) {
    if (!user) return;
    if (likedComments[commentId]) return;
    
    try {
      const response = await apiCall(`like`, "POST", {
        author_id: `${user.author_id}`,
        object: `${commentId}`,
      });

      if (response.ok) {
        setLikedComments(prev => ({
          ...prev,
          [commentId]: true
        }));
        
        const updatedComments = comments.map(comment => {
          if (comment.id === commentId) {
            const currentLikes = comment.likes || { count: 0 };
            return {
              ...comment,
              likes: {
                ...currentLikes,
                count: (currentLikes.count || 0) + 1
              }
            };
          }
          return comment;
        });
        setComments(updatedComments);
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
      const response = await apiCall(`authors/${user.author_id}/commented`, "POST", {
        post: `${post.id}`,
        comment: `${newComment}`,
        contentType: contentType,
      });

      if (response.ok) {
        setNewComment("");
        // Refresh the comments to show the new comment
        await fetchComments();
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
              isInModal={true}
            />
          </div>

          <div className="desktop-comments-container">
            <div className="desktop-comments-header">
              <h3>Comments</h3>
            </div>

            <div 
              id="desktop-comments-list" 
              className="desktop-comments-list" 
              ref={commentListRef}
            >
              {comments.length > 0 ? (
                  comments.map((comment) => (
                    <div key={comment.id} className="desktop-comment-item">
                      <img
                        className="desktop-comment-avatar"
                        src={
                          comment.author?.profileImageURL ||
                          `https://robohash.org/${comment.author?.displayName}.png`
                        }
                        alt={`${comment.author?.displayName || 'User'}'s avatar`}
                      />
                      <div className="desktop-comment-content">
                        <div>
                          <span className="desktop-comment-author">
                            {comment.author?.displayName}
                          </span>
                          {comment.contentType === "text/markdown" ? (
                            <ReactMarkdown>{comment.comment}</ReactMarkdown>
                          ) : (
                            <span className="desktop-comment-text">{comment.comment}</span>
                          )}
                        </div>
                        <div className="desktop-comment-meta">
                          <span className="desktop-comment-time">
                            {new Date(comment.published).toLocaleDateString(undefined, {
                              hour: "2-digit",
                              minute: "2-digit",
                            })}
                          </span>
                          {(comment.likes?.count > 0) && (
                            <span className="desktop-like-count">{comment.likes.count} likes</span>
                          )}
                        </div>
                      </div>
                      <button
                        className={`desktop-like-btn ${likedComments[comment.id] ? "liked" : ""}`}
                        onClick={() => handleLike(comment.id)}
                      >
                        <Heart size={12} className={likedComments[comment.id] ? "heart-filled" : ""} />
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
                  className={`desktop-toggle-btn ${!isMarkdown ? "active" : ""}`}
                  onClick={() => setIsMarkdown(false)}
                >
                  Plain Text
                </button>
                <button
                  type="button"
                  className={`desktop-toggle-btn ${isMarkdown ? "active" : ""}`}
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
