/* eslint-disable react/prop-types */

import {useState} from "react"
import AuthContext from "../context/AuthProvider"
import ReactMarkdown from "react-markdown"
// import MediaComponent from "./MediaComponent"

import {Heart,MessageCircle,Share2} from "lucide-react"
import Comments from "./Comments"

export default function Post({post}){
    const {user} = AuthContext

   
    const [hasLiked, setLikes] = useState(getLikeStatus(user))
    /*
    Each post has its own post object as state
    
    */


    async function handleLike() {
        const authorObject = await getAuthorObject(user)
        const response = await fetch(`${post.author.id}/inbox`,{
            method: "POST",
            credentials: "include",
            headers : {
                "Content-Type":"application/json"
            },

            body : JSON.stringify({
                "type": "like",
                "author": JSON.stringify(authorObject),
                "published": new Date().toISOString(),
                "id": `http://localhost:8000/api/authors/${user.author_id}/liked/${crypto.randomUUID()}`,
                "object": `${post.id}`
            })

        })
        if (!response.ok) {
            throw new Error(`Error liking item: ${response.status}`);
        }
        else {
            setLikes(true)
        }

       
    }
    function handleShare(){
        if (navigator.clipboard) {
            navigator.clipboard.writeText(post.page)
                .then(() => alert("Post URL copied to clipboard!"))
                .catch(err => console.error("Failed to copy URL", err));
          }
    }
    async function getAuthorObject(user) {
        try {
            const response = await fetch(`http://localhost/api/authors/${user.author_id}`);
    
            if (!response.ok) {
                throw new Error(`Error fetching author: ${response.status}`);
            }
    
            const authorObject = await response.json(); 
            return authorObject; 
        } catch (error) {
            console.error("Failed to fetch author:", error);
            return null;
        }
    }
    async function getLikeStatus(user) {
        const response = await fetch(`http://localhost:8000/api/authors/${user.author_id}/liked`)
        if (response.ok){
            const liked = response.json()
            const targetObject = post.id
            const exists = liked.src.some(like => like.object === targetObject)
            return exists;
        }
    }
    /* Comments can't be deleted */

    return (
        <div className="post-container">
            <header className="post-header">
                <img className="post-pfp" src={post.author.profileImage}/>
                <div className="post-header-info">
                    <h3 className="post-title">{post.title}</h3>
                    <span>{post.author.displayName}</span>
                </div>
                <div className="post-main">
                    {/* <MediaComponent /> For later  */}
                    <ReactMarkdown className="post-description">
                        {post.description}
                    </ReactMarkdown>
                    <div className="post-icons">
                        <Heart size={24} className={`${hasLiked ? "liked" : ""}`} onClick={handleLike}/>
                        <MessageCircle size={24}/>
                        {post.visibility === "PUBLIC" ? <Share2 size={24} onClick={handleShare}/>: <></>}

                    </div>
                    <Comments comments={post.comments.src}/>

                </div>

                
            </header>
            
        </div>



    )
}
