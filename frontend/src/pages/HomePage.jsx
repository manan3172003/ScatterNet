import { useState, useEffect, useCallback, useRef } from "react";
import MobileCommentModal from "../components/MobileCommentModal";
import Post from "../components/Post";
import InfiniteScroll from "react-infinite-scroll-component";
import "../assets/styles/homepage.css";
import getCookie from "../context/Cookie";
import DesktopCommentModal from "../components/DesktopCommentModal";
import HeaderLogo from "../components/HeaderLogo";
import {apiCall} from "../utils/utils.js";
export default function HomePage() {
    const [posts, setPosts] = useState([]);
    const csrfToken = getCookie('csrftoken');
    const [selectedPost, setSelectedPost] = useState(null);
    const [showComments, setShowComments] = useState(false);
    const scrollPositionRef = useRef(0);
    const [isMobile, setIsMobile] = useState(false)
    const POSTS_PER_PAGE = 5; 
    const [hasMore, setHasMore] = useState(true);
    const [refreshFlag, setRefreshFlag] = useState(1);
    const [pagination, setPagination] = useState({
        next: null,
        previous: null,
        currentPage: 1
    });
    const [loading, setLoading] = useState(false);
    
    // Save scroll position when opening comments
    useEffect(() => {
        if (showComments) {
            scrollPositionRef.current = window.scrollY;
            document.body.style.overflow = 'hidden';
        } else {
            document.body.style.overflow = '';
            // Restore scroll position when closing comments
            setTimeout(() => {
                window.scrollTo(0, scrollPositionRef.current);
            }, 100);
        }
        
        return () => {
            document.body.style.overflow = '';
        };
    }, [showComments]);
    
    // Initial Fetch
     useEffect(() => {
        fetchUserPosts()
        const checkMobile = () => setIsMobile(window.innerWidth < 768)
        checkMobile()
        window.addEventListener("resize", checkMobile)
        return () => window.removeEventListener("resize", checkMobile)
      }, [])
    
    function handlePostClick(post) {
        setSelectedPost(post);
    }
    
    function handleCommentClick(post, e) {
        e.stopPropagation();
        setSelectedPost(post);
        setShowComments(true);
    }
    
    async function fetchUserPosts() {
        if (loading) return;
        
        setLoading(true);
        
        try {
            const response = await apiCall(`posts?page=1&size=${POSTS_PER_PAGE}`);
            
            if (response.ok) {
                const data = await response.json();
                setPosts(data.src || []);
                setPagination({
                    next: data.next,
                    previous: data.previous,
                    currentPage: 1
                });
                setHasMore(!!data.next);
            }
        } catch (error) {
            console.error("Error fetching posts:", error);
        } finally {
            setLoading(false);
        }
    }
    
    const fetchMorePosts = useCallback(async () => {
        if (loading || !hasMore) return;
        
        setLoading(true);
        
        try {
            let url = pagination.next;

            const response = await fetch(url, {
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": csrfToken
                },
                credentials: "include"
            });
            
            if (response.ok) {
                const data = await response.json();
                
                // Avoid duplicate posts
                const newPosts = data.src || [];
                const existingIds = new Set(posts.map(post => post.id));
                const uniqueNewPosts = newPosts.filter(post => !existingIds.has(post.id));
                
                setPosts(prevPosts => [...prevPosts, ...uniqueNewPosts]);
                
                setPagination(prev => ({
                    next: data.next,
                    previous: data.previous,
                    currentPage: prev.currentPage + 1
                }));
                
                setHasMore(!!data.next);
            }
        } catch (error) {
            console.error("Error fetching more posts:", error);
        } finally {
            setLoading(false);
        }
    }, [loading, hasMore, pagination, posts, csrfToken]);

  // Re-renders all posts if user follows an author on one of the post, so user won't be able
  // to follow them in different post objects after they do in one
  function refreshFeed() {
    const currentScroll = window.scrollY;
    setRefreshFlag((prev) => prev * -1);
    fetchUserPosts().then(() => {
      window.scrollTo(0, currentScroll);
    });
  }

  return (
    <div className="home-page-wrapper">
      <header className="header">{<HeaderLogo />}</header>
      <InfiniteScroll
        dataLength={posts.length}
        next={fetchMorePosts}
        hasMore={hasMore}
        loader={<div className="loader-message">Loading more posts...</div>}
        endMessage={<p className="end-message">No more posts to show.</p>}
        scrollThreshold={0.8}
        className="infinite-scroll-container"
      >
        <main key={refreshFlag} className="feed-container">
          {posts.length > 0
            ? posts.map((post) => (
                <Post
                  key={post.id}
                  post={post}
                  onPostClick={() => handlePostClick(post)}
                  onCommentClick={(e) => handleCommentClick(post, e)}
                  isCommentModalOpen={showComments}
                  onRefresh={refreshFeed}
                />
              ))
            : !loading && (
                <p className="end-message">
                  No posts available. Create a post or follow users to see
                  content.
                </p>
              )}
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
