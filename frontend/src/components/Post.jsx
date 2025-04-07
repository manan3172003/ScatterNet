/* eslint-disable react/prop-types */

import { useContext, useEffect, useRef, useState } from "react";
import { AuthContext } from "../context/AuthContext";
import "../assets/styles/post.css";
import ContentRenderer from "../components/ContentRenderer";
import { useNavigate } from "react-router-dom";
import {
  Calendar,
  Globe,
  Heart,
  Trash,
  Link,
  Lock,
  MessageCircle,
  Share2,
} from "lucide-react";
import {
  getAuthorRelationship,
  handleFollowRequest,
} from "../utils/followApi.js";
import { apiCall, getAuthorObject, getPostHostname } from "../utils/utils.js";
import {fetchAllComments, fetchAllLikes} from "../utils/commentsAndLikesApi.js";

export default function Post({
  post,
  onPostClick,
  onCommentClick,
  hideCommentsButton = false,
  hideFollowButton = false,
  onRefresh,
  isInModal = false,
  isGrid = false,
  isCommentModalOpen
}) {
  const { user } = useContext(AuthContext);
  const [likeCount, setLikeCount] = useState(0);
  const [commentCount, setCommentCount] = useState(0);
  const [hasLiked, setLikes] = useState(false); // Default to false
  const [authorsRelationship, setAuthorsRelationship] = useState("Follow");
  const [needsGradient, setNeedsGradient] = useState(false)
  // This state is going keep track of whether the post has been expanded since by default we truncate excess text

  const [isExpanded, setIsExpanded] = useState(false);
  const [isTruncated, setIsTruncated] = useState(false);
  const contentRef = useRef(null);
  const navigate = useNavigate();
 
  const maxHeight = 400; // Max Height in pixels
  
 
  const formattedDate = new Date(post.published).toLocaleDateString("en-US", {
    year: "numeric",
    month: "short",
    day: "numeric",
  });

  useEffect(() => {
    async function fetchLikeAndFollowStatus() {
      const liked = await getLikeStatus(user);
      const relationship = await getAuthorRelationship(post.author);
      setLikes(liked);
      setAuthorsRelationship(relationship);
    }
    if (user) {
      fetchLikeAndFollowStatus();

      if (!isCommentModalOpen) fetchCommentAndLikesCount();
    }
    function checkTruncation(){
      if (!contentRef.current){
        return
      }
      const contentHeight = contentRef.current.scrollHeight
      
      const hasOverflow = contentHeight > maxHeight
      setIsTruncated(hasOverflow)
      if (hasOverflow){
        setNeedsGradient(true)
      }
    }
    checkTruncation()
   
    }, [isCommentModalOpen]);

 
  const toggleExpand = (e) => {

    e.stopPropagation();
    setIsExpanded(!isExpanded);

  }
  async function handleLike() {
    if (user === null) {
      // Not logged in so do nothing
      return;
    }

    try {
      const response = await apiCall(`like`, "POST", {
        author_id: `${user.author_id}`,
        object: `${post.id}`,
      });

      if (response.ok) {
        setLikes(true);
        setLikeCount((prevCount) => prevCount + 1);
      }
    } catch (error) {
      console.error("Error liking post:", error);
    }
  }

  // WE DON'T HAVE A WAY TO CANCEL FOLLOW REQS, not in spec either
  async function handleFollow() {
    const userAuthor = await getAuthorObject(user);
    const newRelationship = await handleFollowRequest(userAuthor, post.author.serial, authorsRelationship);
    setAuthorsRelationship(newRelationship);

    if (onRefresh) {
      onRefresh();
    }
  }

  async function fetchCommentAndLikesCount() {
    const allComments = await fetchAllComments(post);
    const fetchedCommentsCount = allComments.length;
    setCommentCount(fetchedCommentsCount);

    const allLikes = await fetchAllLikes(post);
    const fetchedLikesCount = allLikes.length;
    setLikeCount(fetchedLikesCount);
  }

  function handleShare() {
    if (navigator.clipboard) {
      navigator.clipboard
        .writeText(post.page)
        .then(() => alert("Post URL copied to clipboard!"))
        .catch((err) => console.error("Failed to copy URL", err));
    }
  }
  function handleEdit() {
    navigate("/editPost", {
      state: {
        formData: {
          title: post.title,
          description: post.description,
          contentType: post.contentType,
          content: post.content,
          visibility: post.visibility,
        },
        postId: post.id,
      },
    });
  }

  function handleDelete() {
    const userConfirmed = window.confirm(
      "Are you sure you want to delete this post?"
    );
    if (userConfirmed) {
      deletePost();
      console.log("User confirmed!");
    } else {
      console.log("User canceled.");
    }
  }

  async function deletePost() {
    try {
      let USER_ID = user.author_id;
      let POST_URL_ID = post.id;
      let post_object = null;

      const get_post_response = await apiCall(`posts/${POST_URL_ID}`);

      if (get_post_response.ok) {
        post_object = await get_post_response.json();
      } else {
        throw new Error("Failed to delete post");
      }

      const response = await apiCall(
        `authors/${USER_ID}/posts/${post_object.serial}`,
        "DELETE"
      );

      if (response.ok) {
        if (onRefresh) {
          onRefresh();
        }
              
        alert(
          "Deleted Post! If you'd like to undelete your post, please contact a node admin for assistance."
        );
      } else {
        throw new Error("Failed to delete post");
      }
    } catch (error) {
      alert("Something went wrong. Please try again.");
      console.log(error);
    }
  }

  async function getLikeStatus(user) {
    const targetObject = post.id;
    let currentUrl = `authors/${user.author_id}/liked`;

    while (currentUrl) {
      const response = await apiCall(currentUrl);
      if (!response.ok) {
        console.error("Error fetching likes:", response.statusText);
        return false;
      }

      const liked = await response.json();

      if (liked.src.some((like) => like.object === targetObject)) {
        return true;
      }

      if (liked.next) {
        try {
          const nextUrl = new URL(liked.next);

          let path = nextUrl.pathname;
          const apiPrefix = "/api/";

          if (path.includes(apiPrefix)) {
            path = path.substring(path.indexOf(apiPrefix) + apiPrefix.length);
          } else if (path.startsWith("/")) {
            path = path.substring(1);
          }

          currentUrl = path + nextUrl.search;
        } catch (error) {
          console.error("Error parsing next URL:", error);
          currentUrl = null;
        }
      } else {
        currentUrl = null;
      }
    }

    return false;
  }
  
  const postHostname = getPostHostname(post)
  return (
    <div
      className={`post-container ${
        isInModal ? "post-in-modal" : isGrid ? "profile-post-container" : ""
      }`}
      onClick={onPostClick}
    >
      <div className="post-header">
        <div className="post-header-top">
          <h2 className="post-title">{post.title}</h2>
          <div className="post-visibility">
            {/* Displays different icons for public, private, and unlisted posts */}
            {post.visibility === "PUBLIC" ? (
              <Globe
                size={16}
                className="visibility-icon public"
                title="Public"
              />
            ) : post.visibility === "FRIENDS" ? (
              <Lock
                size={16}
                className="visibility-icon private"
                title="Private"
              />
            ) : post.visibility === "UNLISTED" ? (
              <Link
                size={16}
                className="visibility-icon unlisted"
                title="Unlisted"
              />
            ) : post.visibility === "DELETED" ? (
              <Trash
                size={16}
                className="visibility-icon deleted"
                title="Deleted"
              />
            ) : null}
          </div>
        </div>

        <div className="post-author">
          <img
            src={
              post.author.profileImage ||
              `https://robohash.org/${post.author.displayName}.png`
            }
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
          {authorsRelationship !== "Same Author" && !hideFollowButton && (
            <button
              className="post-follow-button"
              onClick={handleFollow}
              disabled={authorsRelationship === "Requested"}
            >
              {authorsRelationship === "Not Following"
                ? "Follow"
                : authorsRelationship}
            </button>
          )}
          {/* edit and delete post button */}
          {authorsRelationship === "Same Author" && (
            <div className="button-container">
              <button className="edit-post-button" onClick={handleEdit}>
                Edit
              </button>
              <button className="delete-post-button" onClick={handleDelete}>
                Delete
              </button>
            </div>
          )}
        </div>

        {post.description && (
          <p className="post-description">{post.description}</p>
        )}
      </div>

      <div className="post-content" onClick={onPostClick}>
        
        <div
          ref={contentRef}
          className={`post-content-text ${isExpanded ? "expanded" : "truncated"} ${needsGradient ? "needs-gradient" : ""}`}
        >
          <ContentRenderer
            contentType={post.contentType}
            content={post.content}
            postHostname={postHostname}
              postId={post.id}
          />


        </div>
        
        {isTruncated && (
          <button
            className="read-more-button"
            onClick={toggleExpand}
          >
              {isExpanded ? "Show less" : "Read more"}
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
            <Heart
              size={20}
              className={`action-icon ${hasLiked ? "liked" : ""}`}
            />
              <span className="action-count">{likeCount}</span>
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

          {(post.visibility === "PUBLIC" || post.visibility === "UNLISTED") && (
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