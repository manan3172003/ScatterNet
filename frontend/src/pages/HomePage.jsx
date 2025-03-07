import { useState, useEffect, useCallback } from "react";
import MobileCommentModal from "../components/MobileCommentModal";
import Post from "../components/Post";
import InfiniteScroll from "react-infinite-scroll-component";
import "../assets/styles/homepage.css";
import getCookie from "../context/Cookie";

export default function HomePage() {
    const [posts, setPosts] = useState([]);
    const csrfToken = getCookie('csrftoken');
    const [selectedPost, setSelectedPost] = useState(null)
    const [showComments, setShowComments] = useState(false)
    
    const POSTS_PER_PAGE = 10
    const [hasMore, setHasMore] = useState(true) // State used to keep track if wether or not there are more posts to get
    const [pagination, setPagination] = useState({
        next: null,
        previous: null,
        currentPage: 1
      })

    const [loading, setLoading] = useState(false) // State to prevent multiple simultaneous API calls
    // Initial Fetch
    useEffect(() => {
        fetchUserPosts();
        // const checkMobile = () => setIsMobile(window.innerWidth < 768);
        // checkMobile();
        // window.addEventListener("resize", checkMobile);
        // return () => window.removeEventListener("resize", checkMobile);
    }, []);

    function handlePostClick(post) {
        setSelectedPost(post);
    }

    

    function handleCommentClick(post, e) {
        e.stopPropagation();
        setSelectedPost(post);
        setShowComments(true);
    }
    
    async function fetchUserPosts() {
        if (loading) return

        setLoading(true) // Let the whole component know that we are currently trying to load some posts

        try {
            const response = await fetch(`http://localhost:8000/api/posts?page=1&size=${POSTS_PER_PAGE}`, {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrfToken
            },
            credentials:"include"
            })
            if (response.ok){
                const data = await response.json()
                setPosts(data.results || [])
                setPagination({
                    next: data.next,
                    previous: data.previous,
                    currentPage: 1
                })
                setHasMore(!!data.next) // Double exclamation mark to cast truthy/falsy value to bool

            }
                

        } catch(error){
            console.error("Error fetching more posts", error)
        } finally {
            setLoading(false) // Regardless of what happens set loading to false as we are no longer trying to load new posts.
        }
    }
    // Using useCallback for performance. Memoizing the function to prevent it from being re-created every render and is only recreated when the dependency list changes
    const fetchMorePosts = useCallback(async () => {
        
        if (loading || !hasMore) return // Early return since we are already trying to fetch results or there isn't even any more posts to get.
        try {
            let url

            if (pagination.next) {
                url = pagination.next
            } else {
                const nextPage = pagination.currentPage + 1
                url = `http://localhost:8000/api/posts?page=${nextPage}&size=${POSTS_PER_PAGE}`
            }


        }
        catch(error){
            console.log(error)
        }
    },[loading, hasMore, pagination, csrfToken])

    return (
        <div className="home-page-wrapper">
            <InfiniteScroll
                dataLength={posts.length}
                next={fetchUserPosts}
                hasMore={false} 
                loader={<p className="loader-message">Loading more posts...</p>}
                endMessage={<p className="end-message">No more posts to show.</p>}
            >
                <main className="feed-container">
                    {posts.length > 0 ? (
                        posts.map((post) => (
                            <Post
                                key={post.id}
                                post={post}
                                onPostClick={() => handlePostClick(post)}
                                onCommentClick={(e) => handleCommentClick(post, e)}
                            />
                        ))
                    ) : (
                        <p className="end-message">No posts available. Follow users to see content.</p>
                    )}
                </main>
            </InfiniteScroll>

            {showComments && <MobileCommentModal post={selectedPost} onClose={() => setShowComments(false)} />}
        </div>
    );
}
