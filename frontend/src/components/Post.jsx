/* eslint-disable react/prop-types */

import {useState} from "react"
import { AuthContext } from "../context/AuthContext";
import "../assets/styles/post.css"
import ContentRenderer from "../components/ContentRenderer"
import {useContext,useEffect} from "react"
import {Heart,MessageCircle,Share2, Globe, Lock, Calendar, Link} from "lucide-react"
import getCookie from "../context/Cookie"

export default function Post({post, onPostClick,onCommentClick, hideCommentsButton = false}){
    const {user} = useContext(AuthContext)
    const csrfToken = getCookie('csrftoken')
    const [likeCount,setLikeCount] = useState(post.likes.count)
    const [commentCount,setCommentCount] = useState(post.comments.count)
    const [hasLiked, setLikes] = useState(false) // Default to false

    // This state is going keep track of whether or not the post has been expanded since by default we truncate excess text 
    const [expanded, setExpanded] = useState(false) 

    console.log(hasLiked)
    const formattedDate = new Date(post.published).toLocaleDateString("en-US", {
        year: "numeric",
        month: "short",
        day: "numeric"
    })

    useEffect(() => {
        async function fetchLikeStatus() {
            const liked = await getLikeStatus(user);
            setLikes(liked);
        }
        if (user) {
            fetchLikeStatus();
        }
    }, []);
    async function handleLike() {
        if (user === null){
            // Not logged in so do nothing
            return
        }

        try {
            const response = await fetch(`http://localhost:8000/api/like`, {
              method: "POST",
              credentials: "include",
              headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrfToken,
              },
              body: JSON.stringify({
                "author_id": `${user.author_id}`,
                "object": `${post.id}`
              }),
            })
      
            if (response.ok) {
              setLikes(true)
              setLikeCount(prevCount => prevCount + 1)
            }
          } catch (error) {
            console.error("Error liking post:", error)
          }
    }


    
    function handleShare(){
        if (navigator.clipboard) {
            navigator.clipboard.writeText(post.page)
                .then(() => alert("Post URL copied to clipboard!"))
                .catch(err => console.error("Failed to copy URL", err));
          }
    }
    
    async function getLikeStatus(user) {

        const response = await fetch(`http://localhost:8000/api/authors/${user.author_id}/liked`)
        if (response.ok){
            const liked = await response.json()
            const targetObject = post.id
            const exists = liked.src.some(like => like.object === targetObject)

            return exists;
        }
    }
    const hasLongContent = post.content && post.content.length > 300
    const displayContent = !expanded && hasLongContent 
      ? post.content.substring(0,300) + "....."
      : post.content

      return (
        <div className="post-container"  onClick={onPostClick}>
          <div className="post-header">
            <div className="post-header-top">
              <h2 className="post-title">{post.title}</h2>
              <div className="post-visibility">
                {/* Displays different icons for public, private, and unlisted posts */}
                {post.visibility === "PUBLIC" ? (
                  <Globe size={16} className="visibility-icon public" title="Public" />
                ) : post.visibility === "FRIENDS" ? (
                  <Lock size={16} className="visibility-icon private" title="Private" />
                ) : (
                  <Link size={16} className="visibility-icon unlisted" title="Unlisted" /> )}
              </div>
            </div>
            
            <div className="post-author">
              <img
                src={post.author.profileImage} 
                alt={post.author.displayName}
                className="post-avatar"
                onError={(e) => {
                  e.target.src = `${post.author.profileImage}`;
                }}
              />
              <div className="author-info">
                <span className="post-author-name">{post.author.displayName}</span>
                <div className="post-meta">
                  <Calendar size={14} className="meta-icon" />
                  <span className="post-date">{formattedDate}</span>
                </div>
              </div>
            </div>
            
            {post.description && (
              <p className="post-description">{post.description}</p>
            )}
          </div>
    
          <div className="post-content" onClick={onPostClick}>
            <ContentRenderer contentType={post.contentType} content={displayContent} />
            
            {hasLongContent && (
              <button 
                className="read-more-button" 
                onClick={(e) => {
                  e.stopPropagation();
                  setExpanded(!expanded);
                }}
              >
                {expanded ? "Show less" : "Read more"}
              </button>
            )}
          </div>
    
          <div className="post-footer">
            <div className="post-actions">
              <button 
                className={`action-button ${hasLiked ? "liked" : ""}`}
                onClick={(e) => {
                  e.stopPropagation();
                  handleLike();
                }}
              >
                <Heart size={20} className={`action-icon ${hasLiked ? "liked" : ""}`} />
                {post.visibility != "FRIENDS" && <span className="action-count">{likeCount}</span>}
              </button>
              
              <button 
                className="action-button"
                onClick={(e) => {
                  e.stopPropagation();
                  onCommentClick(e);
                }}
              >
                <MessageCircle size={20} className="action-icon" />
                <span className="action-count">{commentCount}</span>
              </button>
              
              {(post.visibility === "PUBLIC"  || post.visibility === "UNLISTED" ) && (
                <button 
                  className="action-button"
                  onClick={(e) => {
                    e.stopPropagation();
                    handleShare();
                  }}
                >
                  <Share2 size={20} className="action-icon" />
                </button>
              )}
            </div>
            
            {!hideCommentsButton && commentCount > 0 && (
              <button 
                className="view-comments-button"
                onClick={(e) => {
                  e.stopPropagation();
                  onCommentClick(e);
                }}
              >
                View all {commentCount} comments
              </button>
            )}
          </div>
        </div>
      );
}