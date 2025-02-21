/* eslint-disable react/prop-types */

import {useState} from "react"
import { AuthContext } from "../context/AuthContext";
import ReactMarkdown from "react-markdown"
import "../assets/styles/post.css"
// import MediaComponent from "./MediaComponent"
import {useContext,useEffect} from "react"
import {Heart,MessageCircle,Share2} from "lucide-react"


export default function Post({post, onPostClick,onCommentClick}){
    const {user} = useContext(AuthContext)

   
        /*
    Each post has its own post object as state
    
    */

    const [hasLiked, setLikes] = useState(false); // Default to false

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
            console.log(user)
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
            const liked = await response.json()
            const targetObject = post.id
            const exists = liked.src.some(like => like.object === targetObject)
          
            return exists;
        }
    }
    /* Comments can't be deleted */

    return (
      

    <div className="post-container" onClick={onPostClick}>
        <div className="post-header">
          <h2 className="post-title">{post.title}</h2>
          <div className="post-author">
            <img
              src={post.author.profileImage}
              alt={post.author.displayName}
              className="post-avatar"
            />
            <span className="post-author-name">{post.author.displayName}</span>
          </div>
        </div>
  
        <img
        src={"https://i.imgur.com/k7XVwpB.jpeg"}
        alt="Post"
        className="post-image"
      />
  
        <div className="post-body">
          <div className="post-icons">
           
            <Heart size={24} className={`${hasLiked ? "liked" : ""}`} onClick={handleLike}/>
            <MessageCircle size={24} onClick={onCommentClick}/>
            {post.visibility === "PUBLIC" ? <Share2 size={24} onClick={handleShare}/>: <></>}
            
          </div>
          {post.visibility === "PUBLIC" || post.visibility === "UNLISTED" ? <div className="likes">{post.likes.count} likes</div>:<></>}
          <ReactMarkdown className="post-caption">
            <span className="post-author-name">{post.author.displayName}</span> {post.description}
          </ReactMarkdown>
  
          <span className="view-comments" >
            View all {post.comments.count} comments
          </span>
        </div>
      </div>

    )
}
