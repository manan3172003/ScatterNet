import { useState, useEffect } from "react";
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
    

    const [hasMore, setHasMore] = useState(true) // State used to keep track if wether or not there are more posts to get
    const [pageInfo, setPageInfo] = useState({
        next: null,
        count: 0,
        currentPage: 1
    }) // State to keep track of current pageInfo like how many posts are displayed, what p

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
            const response = await fetch("http://localhost:8000/api/posts", {
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


            }
                

        } catch(error){
            console.error("Error fetching more posts", error)
        } finally {
            setLoading(false) // Regardless of what happens set loading to false as we are no longer trying to load new posts.
        }
    }

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
