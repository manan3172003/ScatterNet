/* eslint-disable react/prop-types */

import {useState} from "react"
import { AuthContext } from "../context/AuthContext";
import ReactMarkdown from "react-markdown"
import "../assets/styles/post.css"

import {useContext,useEffect} from "react"
import {Heart,MessageCircle,Share2} from "lucide-react"
import getCookie from "../context/Cookie"

export default function Post({post, onPostClick,onCommentClick}){
    const {user} = useContext(AuthContext)
    const csrfToken = getCookie('csrftoken')

    const [likeCount,setLikeCount] = useState(post.likes.count)
    const [commountCount,setCommentCount] = useState(post.comments.count)
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
    }, [hasLiked]);
    async function handleLike() {
        if (user === null){
            // Not logged in so do nothing
            return
        }

        const authorObject = await getAuthorObject(user)
        
        const response = await fetch(`http://localhost:8000/api/like`,{
            method: "POST",
            credentials: "include", 
            "X-CSRFToken": csrfToken,
            headers : {
                "Content-Type":"application/json"
            },
            
            body : JSON.stringify({
                "author_id": `${user.author_id}`,
                "object": `${post.id}`
            }),
            

        })
        if (!response.ok) {
            throw new Error(`Error liking item: ${response.status}`);
        }
        else {
            setLikes(true)
            setLikeCount(prevCount => prevCount + 1);
            
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
            const response = await fetch(`http://localhost:8000/api/authors/${user.author_id}`);
    
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

        <span>{post.description}</span>
        
        <div className="post-body">
            <div className="post-caption">
                    {<ReactMarkdown className="markdown">{post.content}</ReactMarkdown>}
            
            </div>
          <div className="post-icons">
           
            <Heart size={24} className={`${hasLiked ? "liked" : ""}`} onClick={handleLike}/>
            <MessageCircle size={24} onClick={onCommentClick}/>
            {post.visibility === "PUBLIC" ? <Share2 size={24} onClick={handleShare}/>: <></>}
            
          </div>
          {post.visibility === "PUBLIC" || post.visibility === "UNLISTED" ? <div className="likes">{likeCount} likes</div>:<></>}
          
         
  
          <span className="view-comments" onClick={onCommentClick}>
            View all {post.comments.count} comments
          </span>
        </div>
      </div>

    )
}
