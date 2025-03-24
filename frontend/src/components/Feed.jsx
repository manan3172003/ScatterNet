import { useState, useEffect, useRef, useCallback } from "react";
import DesktopCommentModal from "../components/DesktopCommentModal";
import MobileCommentModal from "../components/MobileCommentModal";
import Post from "../components/Post";
import InfiniteScroll from "react-infinite-scroll-component";
import getCookie from "../context/Cookie.js";
import "../assets/styles/profile-feed.css";
import { apiCall } from "../utils/utils.js";
export default function Feed(values) {
  async function fetchAuthorPosts() {
    const response = await apiCall(`authors/${values.author_id}/posts`);
    if (response.ok) {
      const posts_object = await response.json();
      const posts = posts_object.src;
      setPosts(posts);
    }
  }

  const [posts, setPosts] = useState([]);
  const csrfToken = getCookie("csrftoken");
  const [selectedPost, setSelectedPost] = useState(null);
  const [showComments, setShowComments] = useState(false);
  const scrollPositionRef = useRef(0);
  const [isMobile, setIsMobile] = useState(false);
  const POSTS_PER_PAGE = 5;
  const [hasMore, setHasMore] = useState(true);
  const [pagination, setPagination] = useState({
    next: null,
    previous: null,
    currentPage: 1,
  });
  const [loading, setLoading] = useState(false);

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

  useEffect(() => {
    fetchAuthorPosts();

    const checkMobile = () => setIsMobile(window.innerWidth < 768);
    checkMobile();
    window.addEventListener("resize", checkMobile);
    return () => window.removeEventListener("resize", checkMobile);
  }, []);

  function handlePostClick(post) {
    setSelectedPost(post);
  }

  function handleCommentClick(post, e) {
    e.stopPropagation();
    setSelectedPost(post);
    setShowComments(true);
  }
  const fetchMorePosts = useCallback(async () => {
    if (loading || !hasMore) return;

    setLoading(true);

    try {
      let url = pagination.next;

      const response = await fetch(url, {
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": csrfToken,
        },
        credentials: "include",
      });

      if (response.ok) {
        const data = await response.json();

        // Avoid duplicate posts
        const newPosts = data.src || [];
        const existingIds = new Set(posts.map((post) => post.id));
        const uniqueNewPosts = newPosts.filter(
          (post) => !existingIds.has(post.id)
        );

        setPosts((prevPosts) => [...prevPosts, ...uniqueNewPosts]);

        setPagination((prev) => ({
          next: data.next,
          previous: data.previous,
          currentPage: prev.currentPage + 1,
        }));

        setHasMore(!!data.next);
      }
    } catch (error) {
      console.error("Error fetching more posts:", error);
    } finally {
      setLoading(false);
    }
  }, [loading, hasMore, pagination, posts, csrfToken]);
  return (
    <div class="feed-wrapper">
      <InfiniteScroll
        dataLength={posts.length}
        next={fetchMorePosts}
        loader={<p className="error-text">Loading more posts...</p>}
        endMessage={<p className="error-text">No more posts to show.</p>}
      >
        <main className="user-feed-container">
          {posts.map((post) => (
            <Post
              key={post.id}
              post={post}
              onPostClick={() => handlePostClick(post)}
              onCommentClick={(e) => handleCommentClick(post, e)}
              hideFollowButton={true}
              isGrid={true}
            />
          ))}
        </main>
      </InfiniteScroll>
      {showComments &&
        (isMobile ? (
          <MobileCommentModal
            post={selectedPost}
            onClose={() => setShowComments(false)}
          />
        ) : (
          <DesktopCommentModal
            post={selectedPost}
            onClose={() => setShowComments(false)}
          />
        ))}
    </div>
  );
}
