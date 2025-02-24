import { useState, useEffect } from "react"

import MobileCommentModal from "../components/MobileCommentModal"
import Post from "../components/Post"
import InfiniteScroll from "react-infinite-scroll-component";
import "../assets/styles/homepage.css"
import getCookie from "../context/Cookie";
export default function HomePage(){
    const [posts,setPosts] = useState([])
    const csrfToken = getCookie('csrftoken')
    const [selectedPost, setSelectedPost] = useState(null)
    const [showComments, setShowComments] = useState(false)
    const [isMobile, setIsMobile] = useState(false)
    useEffect(() => {
        fetchUserPosts()

        const checkMobile = () => setIsMobile(window.innerWidth < 768)
        checkMobile()
        window.addEventListener("resize", checkMobile)
        return () => window.removeEventListener("resize", checkMobile)
      }, [])

    function handlePostClick(post){
        if(!isMobile){
            selectedPost(post)
        }

    }

    async function fetchUserPosts(){
        const response = await fetch("http://localhost:8000/api/posts",
            {
                method: "GET",
                headers: {
                    "Content-Type": "application/json",
                },
                credentials: "include",
                "X-CSRFToken": csrfToken,
        })
        if (response.ok){
            const posts_object = await response.json()
            const posts = posts_object.src
            setPosts(posts)
        }
    }

    function handleCommentClick(post,e){
        
        e.stopPropagation()
       
        setSelectedPost(post)
        setShowComments(true)
    
    }
    async function fetchMorePosts(){
        try {
            const response = await fetch(`http://localhost:8000/api/posts?page=${1}`); // to be added
            /*Replace fakePosts with a state called "posts" Use a useEffect to make a initial fetch to get the
            first batch/page of posts. Then in the infinite scroll component call fetchMorePosts until "next" is null */
            const data = await response.json();
            console.log(data) // to be added
            
        } catch (error) {
            console.error("Error fetching posts:", error);
        }
    }

    
    return (
        <InfiniteScroll
            dataLength={posts.length}
            next={fetchMorePosts}
            
            loader={<p>Loading more posts...</p>}
            endMessage={<p>No more posts to show.</p>}
        >
            <main className="feed-container">
                {posts.map((post) => (
                <Post
                    key={post.id}
                    post={post}
                    onPostClick={() => handlePostClick(post)}
                    onCommentClick={(e) => handleCommentClick(post, e)}
                />
                
            ))}

            </main>

            {showComments && <MobileCommentModal post={selectedPost} onClose={() => setShowComments(false)} />}
        </InfiniteScroll>
    )
}