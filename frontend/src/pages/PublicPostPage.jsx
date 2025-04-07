import { useEffect, useState, useRef } from "react";
import Post from "../components/Post";
import { useParams } from "react-router-dom";
import "../assets/styles/public-post-page.css";
import { apiCall } from "../utils/utils.js";
import DesktopCommentModal from "../components/DesktopCommentModal";
import MobileCommentModal from "../components/MobileCommentModal";

export default function PublicPostPage() {
  const { authorId, postId } = useParams();
  const [post, setPost] = useState(null);
  const [loading, setLoading] = useState(true);
  const [showComments, setShowComments] = useState(false);
  const [selectedPost, setSelectedPost] = useState(null);
  const [isMobile, setIsMobile] = useState(false);
  const scrollPositionRef = useRef(0);

  useEffect(() => {
    async function fetchPost() {
      try {
        const response = await apiCall(`authors/${authorId}/posts/${postId}`);
        if (!response.ok) throw new Error("Post not found");
        const data = await response.json();
        setPost(data);
      } catch (error) {
        console.error("Error fetching post:", error);
      } finally {
        setLoading(false);
      }
    }

    fetchPost();
    
    // Check for mobile device
    const checkMobile = () => setIsMobile(window.innerWidth < 768);
    checkMobile();
    window.addEventListener("resize", checkMobile);
    return () => window.removeEventListener("resize", checkMobile);
  }, [authorId, postId]);

  // Save scroll position when opening comments
  useEffect(() => {
    if (showComments) {
      scrollPositionRef.current = window.scrollY;
      document.body.style.overflow = "hidden";
    } else {
      document.body.style.overflow = "";
      // Restore scroll position when closing comments
      setTimeout(() => {
        window.scrollTo(0, scrollPositionRef.current);
      }, 100);
    }

    return () => {
      document.body.style.overflow = "";
    };
  }, [showComments]);

  function handlePostClick(post) {
    setSelectedPost(post);
  }

  function handleCommentClick(post, e) {
    if (e) e.stopPropagation();
    setSelectedPost(post);
    setShowComments(true);
  }

  function refreshPost() {
    // Re-fetch post if needed after a comment is added
    async function fetchPost() {
      try {
        const response = await apiCall(`authors/${authorId}/posts/${postId}`);
        if (response.ok) {
          const data = await response.json();
          setPost(data);
        }
      } catch (error) {
        console.error("Error refreshing post:", error);
      }
    }
    
    fetchPost();
  }

  return (
    <div className="public-post-page-container">
      <div className="wrapper">

      
        {loading ? (
          <p className="debug-text">Loading...</p>
        ) : post ? (
          <Post 
            post={post} 
            onCommentClick={(e) => handleCommentClick(post, e)} 
            onPostClick={() => handlePostClick(post)}
            isCommentModalOpen={showComments}
            onRefresh={refreshPost}
          />
        ) : (
          <p className="error-text">Post not found</p>
        )}
      </div>
      {showComments && (
        isMobile ? (
          <MobileCommentModal
            post={selectedPost}
            onClose={() => setShowComments(false)}
          />
        ) : (
          <DesktopCommentModal
            post={selectedPost}
            onClose={() => setShowComments(false)}
          />
        )
      )}
    </div>
  );
}
