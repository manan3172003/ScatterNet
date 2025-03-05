import { useState, useEffect } from "react";
import MobileCommentModal from "../components/MobileCommentModal";
import Post from "../components/Post";
import InfiniteScroll from "react-infinite-scroll-component";
import "../assets/styles/homepage.css";
import getCookie from "../context/Cookie";

export default function HomePage() {
    const [posts, setPosts] = useState([]);
    const csrfToken = getCookie('csrftoken');
    const [selectedPost, setSelectedPost] = useState(null);
    const [showComments, setShowComments] = useState(false);
    const [isMobile, setIsMobile] = useState(false);
    
    useEffect(() => {
        fetchUserPosts();
        const checkMobile = () => setIsMobile(window.innerWidth < 768);
        checkMobile();
        window.addEventListener("resize", checkMobile);
        return () => window.removeEventListener("resize", checkMobile);
    }, []);

    function handlePostClick(post) {
        setSelectedPost(post);
    }

    async function fetchUserPosts() {
        const response = await fetch("http://localhost:8000/api/posts",
            {
                method: "GET",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": csrfToken
                },
                credentials: "include"
            });
            
        if (response.ok) {
            const posts_object = await response.json();
            const posts = posts_object.src;
            setPosts(posts);
        }
    }

    function handleCommentClick(post, e) {
        e.stopPropagation();
        setSelectedPost(post);
        setShowComments(true);
    }
    
    async function fetchMorePosts() {
        try {
            const response = await fetch(`http://localhost:8000/api/posts?page=${1}`);
            const data = await response.json();
            console.log(data);
            
        } catch (error) {
            console.error("Error fetching posts:", error);
        }
    }

    return (
        <div className="home-page-wrapper">
            <InfiniteScroll
                dataLength={posts.length}
                next={fetchMorePosts}
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
