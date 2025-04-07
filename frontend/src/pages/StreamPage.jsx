import { useState, useEffect, useRef } from "react";
import HeaderLogo from "../components/HeaderLogo";
import { Calendar, Eye, Heart } from 'lucide-react';
import { getReelsFeed, viewReel, addReelComment, getReelComments, likeComment, unlikeComment } from "../utils/reelsApi";
import "../assets/styles/stream-page.css";
import Notification from "../components/Notification";
import VideoPlayer from "../components/VideoPlayer";
import LikeButton from "../components/ReelLikeButton";
import ContentRenderer from "../components/ContentRenderer";
/**
 * Implementation details:
 * - Uses the backend endpoint (/api/reels/{id}/stream/) for video streaming
 * - Uses HTTP range requests for proper seeking functionality
 * - Maintains video position during interactions (likes, comments)
 * - Automatically plays the next video when current one ends
 */
export default function StreamPage() {
  const [reels, setReels] = useState([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [isPlaying, setIsPlaying] = useState(false);
  const [comment, setComment] = useState("");
  const [contentType, setContentType] = useState("text/plain");
  const [isLoading, setIsLoading] = useState(true);
  const [comments, setComments] = useState([]);
  const [commentLikes, setCommentLikes] = useState({});
  const [loadingComments, setLoadingComments] = useState(false);
  
  const videoRef = useRef(null);
  
  // State for notifications
  const [notification, setNotification] = useState({
    show: false,
    type: "success",
    title: "",
    message: "",
  });
  const showNotification = (type, title, message) => {
    setNotification({
      show: true,
      type,
      title,
      message,
    });
  };

  const hideNotification = () => {
    setNotification((prev) => ({ ...prev, show: false }));
  };

  // Initial fetch of reels
  useEffect(() => {
    fetchReels();
    const handleVisibilityChange = () => {
      if (document.visibilityState === 'visible') {
        fetchReels();
      }
    };
    document.addEventListener('visibilitychange', handleVisibilityChange);
    
    return () => {
      document.removeEventListener('visibilitychange', handleVisibilityChange);
    };
  }, []);

  // Fetching reels from the backend
  async function fetchReels(){
    try {
      setIsLoading(true);
      const response = await getReelsFeed();
      
      if (response.ok) {
        try {
          const responseText = await response.text();
          
          let data;
          if (responseText.trim()) {
            try {
              data = JSON.parse(responseText);
            } catch (jsonError) {
              console.error("JSON parse error:", jsonError);
              setIsLoading(false);
              return;
            }
          } else {
            data = { results: [] };
          }
          const reelsArray = Array.isArray(data) ? data : 
                            data.results ? data.results : 
                            [];
          
          /**
           * Process reels array to change video URL to use the streaming endpoint for seeking
           */
          const processedReels = reelsArray.map(reel => {
            const videoId = reel.id;
            const streamUrl = `/api/reels/${videoId}/stream/`;
            // Keeping the original URL as a fallback
            let originalUrl = reel.video_url || reel.video;
            if (originalUrl && !originalUrl.startsWith('http')) {
              originalUrl = window.location.origin + originalUrl;
            }
            
            return {
              ...reel,
              video: streamUrl,
              originalVideoUrl: originalUrl,
              likes_count: reel.likes_count,
              comments_count: reel.comments_count,
              is_liked: !!reel.is_liked,
              caption: reel.caption,
              author: reel.author 
            };
          });
          setReels(processedReels);
        } catch (textError) {
          showNotification("error", "Response Error", "Could not read server response");
        }
      } else {
        showNotification("error", "Failed to load", "Could not retrieve videos");
      }
    } catch (error) {
      showNotification("error", "Error", "Something went wrong while fetching videos");
    } finally {
      setIsLoading(false);
    }
  };

  async function fetchComments(reelId){
    if (!reelId) return;
    
    setLoadingComments(true);
    try {
      const response = await getReelComments(reelId);
      if (response.ok) {
        try {
          const data = await response.json();
          
          const commentsArray = Array.isArray(data) ? data : 
                                data.results ? data.results : [];
          
          setComments(commentsArray);
        } catch (error) {
          console.error("Error parsing comments:", error);
          setComments([]);
        }
      } else {
        console.warn("Failed to load comments, using empty array");
        setComments([]);
      }
    } catch (error) {
      console.error("Error fetching comments:", error);
      setComments([]);
    } finally {
      setLoadingComments(false);
    }
  };
  
  // When current reel changes, fetch its comments
  useEffect(() => {
    if (reels.length > 0) {
      fetchComments(reels[currentIndex].id);
      // Reset comment likes for new reel
      setCommentLikes({});
    }
  }, [currentIndex, reels.length]);
  
  // Initialize comment likes from fetched comments
  useEffect(() => {
    const likeStatus = {};
    comments.forEach(comment => {
      likeStatus[comment.id] = comment.is_liked || false;
    });
    setCommentLikes(likeStatus);
  }, [comments]);
  
  // Handle liking/unliking comments
  const handleCommentLike = async (commentId) => {
    const currentReelId = reels[currentIndex]?.id;
    if (!currentReelId) return;
    
    try {
      const isCurrentlyLiked = commentLikes[commentId];
      
      // Update UI optimistically
      setCommentLikes(prev => ({...prev, [commentId]: !isCurrentlyLiked}));
      
      // Update the comment's like count optimistically
      setComments(prevComments => 
        prevComments.map(comment => {
          if (comment.id === commentId) {
            const currentLikes = comment.likes_count || 0;
            return {
              ...comment,
              likes_count: isCurrentlyLiked ? Math.max(0, currentLikes - 1) : currentLikes + 1,
              is_liked: !isCurrentlyLiked
            };
          }
          return comment;
        })
      );

      const response = isCurrentlyLiked 
        ? await unlikeComment(currentReelId, commentId)
        : await likeComment(currentReelId, commentId);

      if (!response.ok) {
        // Reverting the UI if the unliking/liking action fails
        setCommentLikes(prev => ({...prev, [commentId]: isCurrentlyLiked}));
        setComments(prevComments => 
          prevComments.map(comment => {
            if (comment.id === commentId) {
              const currentLikes = comment.likes_count || 0;
              return {
                ...comment,
                likes_count: isCurrentlyLiked ? currentLikes : Math.max(0, currentLikes - 1),
                is_liked: isCurrentlyLiked
              };
            }
            return comment;
          })
        );
        console.error("API error:", await response.text());
      }
    } catch (error) {
      console.error("Error toggling comment like:", error);
    }
  };

  const handleVideoPlay = () => {
    setIsPlaying(true);
    // Record a view when video starts playing
    if (reels.length > 0) {
      viewReel(reels[currentIndex].id).catch(err => {
        console.warn("Failed to record view:", err);
      });
    }
  };

  const handleVideoEnd = () => {
    setIsPlaying(false);
    if (currentIndex < reels.length - 1) {
      setCurrentIndex(currentIndex + 1);
    }
  };
  const handleNext = () => {
    if (currentIndex < reels.length - 1) {
      setCurrentIndex(currentIndex + 1);
    }
  };

  // Handle navigation to previous video
  const handlePrevious = () => {
    if (currentIndex > 0) {
      setCurrentIndex(currentIndex - 1);
    }
  };  
  // Handle comment submission
  const handleCommentSubmit = async (e) => {
    e.preventDefault();
    if (!comment.trim() || reels.length === 0) return;
    
    // Get current video state
    const videoElement = videoRef.current;
    let currentTime = 0;
    let isPlaying = false;
    
    if (videoElement) {
      try {
        currentTime = videoElement.currentTime || 0;
        isPlaying = !videoElement.paused;
      } catch (err) {
        console.warn(err);
      }
    }
    
    const commentText = comment.trim();
    
    try {
      // Clear input immediately for better UX
      setComment("");
      
      // Temporary Comment that assumes the api call is going to go through
      const tempComment = {
        id: 'temp-' + Date.now(),
        author: { displayName: 'You' },
        content: commentText,
        contentType: contentType,
        created_at: new Date().toISOString()
      };
      setComments(prevComments => [tempComment, ...prevComments]);
  
      const response = await addReelComment(reels[currentIndex].id, commentText, contentType);
      
      if (response.ok) {
        try {
          // Get the real comment data
          const newComment = await response.json();
          // Replacing the temp comment with real one
          setComments(prevComments => 
            prevComments.map(c => c.id === tempComment.id ? newComment : c)
          );
          
          const updatedReels = [...reels];
          updatedReels[currentIndex] = {
            ...updatedReels[currentIndex],
            comments_count: (updatedReels[currentIndex].comments_count || 0) + 1
          };
          setReels(updatedReels);
          
        } catch (error) {
          console.error("Error parsing comment response:", error);
          
        }
      } else {
        // Comment failed so we remove temp comment
        console.error("Comment failed:", response.status);
        setComments(prevComments => 
          prevComments.filter(c => c.id !== tempComment.id)
        );
        showNotification("error", "Comment Failed", "Could not post your comment");
      }
    } catch (error) {
      console.error("Error adding comment:", error);
      
    } finally {
      // Check if we need to restore video state
      requestAnimationFrame(() => {
        const videoEl = videoRef.current;
        if (videoEl && typeof currentTime === 'number') {
          const currentPos = videoEl.currentTime || 0;
          if (Math.abs(currentPos - currentTime) > 0.5) {
            if (typeof videoEl.seekTo === 'function') {
              videoEl.seekTo(currentTime);
            } else {
              videoEl.currentTime = currentTime;
            }
          }
          if (isPlaying && videoEl.paused) {
            const playPromise = videoEl.play();
            if (playPromise !== undefined) {
              playPromise.catch(e => console.warn("Couldn't resume video:", e));
            }
          }
        }
      });
    }
  };

  // Format date for display
  function formatDate (dateString){
    if (!dateString) return 'Unknown date';
    
    try {
      const date = new Date(dateString);
      return new Intl.DateTimeFormat('en-US', {
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      }).format(date);
    } catch (e) {
      return 'Invalid date';
    }
  };

  return (
    <div className="stream-container">
      <Notification
        show={notification.show}
        type={notification.type}
        title={notification.title}
        message={notification.message}
        onClose={hideNotification}
      />
      
      <header className="header">
        <HeaderLogo />
      </header>
      
      <main className="stream-main">
        {isLoading ? (
          <div className="loading-container">
            <div className="loading-spinner"></div>
            <p>Loading videos...</p>
          </div>
        ) : reels.length === 0 ? (
          <div className="no-reels">
            <h2>No videos found</h2>
            <p>Be the first to upload a video!</p>
          </div>
        ) : (
          <div className="reel-player">
            <div className="video-container">
              <div className="video-player">
                {/* 
                  Video player with proper seeking support
                  - Video source comes from the /api/reels/{id}/stream/ endpoint
                */}
                <VideoPlayer
                  ref={videoRef}
                  src={reels[currentIndex]?.video}
                  onPlay={handleVideoPlay}
                  onEnded={handleVideoEnd}
                  controls={true}
                  autoPlay={true}
                  className="reel-video"
                />
                
              </div>
              <div className="reel-info">
                <div className="author-caption-row">
                    <img
                      src={
                        reels[currentIndex]?.author?.profileImage ||
                        `https://robohash.org/${reels[currentIndex]?.author?.displayName}.png`
                      }
                      alt="Author"
                      className="author-avatar"
                    />
                    <div className="caption-meta">
                      <span className="author-name">{reels[currentIndex]?.author?.displayName}</span>
                      <p className="reel-caption">{reels[currentIndex]?.caption}</p>
                    </div>
                  </div>
                  <div className="meta-info">
                        <span className="views"><Eye /> {reels[currentIndex]?.view_count || 0} views</span>
                        <span className="created-at">
                          <Calendar/> {new Date(reels[currentIndex]?.created_at).toLocaleDateString()}
                        </span>
                  </div>
               </div>

              
              <div className="reel-controls">
                <button 
                  onClick={handlePrevious} 
                  disabled={currentIndex === 0}
                  className="control-btn prev-btn"
                >
                  Previous
                </button>
                <LikeButton 
                  reel={reels[currentIndex]} 
                  onLikeToggle={(newIsLiked, newLikesCount) => {
                   
                    const updatedReels = [...reels];
                    updatedReels[currentIndex] = {
                      ...reels[currentIndex],
                      is_liked: newIsLiked,
                      likes_count: newLikesCount
                    };
                    setReels(updatedReels);
                  }}
                />
                <button 
                  onClick={handleNext} 
                  disabled={currentIndex === reels.length - 1}
                  className="control-btn next-btn"
                >
                  Next
                </button>
              </div>
            </div>
            
            <div className="comment-section">
              <h3>Comments ({reels[currentIndex]?.comments_count || 0})</h3>
              <div className="desktop-comment-input">
              <div className="desktop-format-toggle">
                <button
                  type="button"
                  className={`desktop-toggle-btn ${contentType != "text/markdown" ? "active" : ""}`}
                  onClick={() =>  setContentType(prev => prev === 'text/plain' ? 'text/markdown' : 'text/plain')}
                >
                  Plain Text
                </button>
                <button
                  type="button"
                  className={`desktop-toggle-btn ${contentType === "text/markdown" ? "active" : ""}`}
                  onClick={() =>  setContentType(prev => prev === 'text/plain' ? 'text/markdown' : 'text/plain')}
                >
                  Markdown
                </button>
              </div>
              <form onSubmit={handleCommentSubmit} className="desktop-comment-form">
                <input
                  type="text"
                  value={comment}
                  placeholder="Add a comment..."
                  onChange={(e) => setComment(e.target.value)}
                  className="desktop-input-field"
                />
                <button
                  type="submit"
                  className="desktop-post-btn"
                  disabled={!comment.trim()}
                >
                  Post
                </button>
              </form>
            </div>
              {loadingComments ? (
                <div className="comments-loading">
                  <div className="loading-spinner" style={{ width: '20px', height: '20px' }}></div>
                  <p>Loading comments...</p>
                </div>
              ) : comments.length > 0 ? (
                <div className="comments-list">
                  {comments.map(comment => (
                    <div key={comment.id} className="comment-item">
                      <div className="comment-header">
                        <img className="comment-avatar" src={comment.author?.profileImage || `https://robohash.org/${comment.author?.displayName || 'anonymous'}.png`}/>
                        <span className="comment-author">
                          {comment.author?.displayName || 'Anonymous'}
                        </span>
                        <span className="comment-date">{formatDate(comment.created_at)}</span>
                      </div>
                      <div className="comment-content">
                        <ContentRenderer 
                          content={comment.content} 
                          contentType={comment.contentType || 'text/plain'} 
                        />
                      </div>
                      <div className="comment-actions">
                        <div 
                          className={`comment-like-button ${commentLikes[comment.id] ? 'liked' : ''}`}
                          onClick={() => handleCommentLike(comment.id)}
                        >
                          <Heart size={16} fill={commentLikes[comment.id] ? "#f00" : "none"} color={commentLikes[comment.id] ? "#f00" : "#777"} />
                          <span>{comment.likes_count || 0}</span>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              ) : (
                <div className="no-comments">
                  <p>No comments yet. Be the first to comment!</p>
                </div>
              )}
            </div>
          </div>
        )}
      </main>
    </div>
  );
}