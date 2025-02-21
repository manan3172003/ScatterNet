/* eslint-disable react/prop-types */

import {useState} from "react"
import AuthContext from "../context/AuthProvider"
// import MediaComponent from "./MediaComponent"

import {Heart,MessageCircle,Share2} from "lucide-react"

export default function Post({post}){
    const {user} = AuthContext

    let hasLiked = getLikeStatus(user)
    const [postLikes, setLikes] = useState(hasLiked)
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
                    <span className="post-description">
                        {post.description}
                    </span>
                    <div className="post-icons">

                        <Heart/>
                        <MessageCircle/>
                        <Share2/>

                    </div>
                    

                </div>

                
            </header>
            
        </div>



    )
}
