import { unlikeReel, likeReel } from "../utils/reelsApi";
import { useState, useEffect } from "react";
import {Heart} from "lucide-react";
export default function LikeButton({reel,onLikeToggle}){
    const [isLiked, setIsLiked] = useState(reel.is_liked || false);
    const [likesCount, setLikesCount] = useState(reel.likes_count || 0);
    const [likeStatus, setLikeStatus] = useState('idle');
    useEffect(() => {
        setIsLiked(!!reel.is_liked); 
        setLikesCount(reel.likes_count || 0);
    }, [reel.is_liked, reel.likes_count, reel.id]);
    const handleLike = async () => {
        try {
            if (likeStatus === 'pending') return;
            setLikeStatus('pending');
            const newIsLiked = !isLiked;
            const newLikesCount = isLiked ? likesCount - 1 : likesCount + 1;

            setIsLiked(newIsLiked);
            setLikesCount(newLikesCount);
            
            const response = isLiked ? 
                await unlikeReel(reel.id) : 
                await likeReel(reel.id);
            if (response.ok) {
                
                if (onLikeToggle) {
                    onLikeToggle(newIsLiked, newLikesCount);
                }
            } else {
    
                setIsLiked(!newIsLiked);
                setLikesCount(isLiked ? likesCount : likesCount - 1);
            }
        } catch (error) {
            console.error("Error liking/unliking reel:", error);
            // Revert the like on error
            setIsLiked(isLiked);
            setLikesCount(likesCount);
        } finally {
            setLikeStatus('idle');
        }
    };

    return (
        <button
            className={`action-button ${isLiked ? "liked" : ""}`}
            onClick={handleLike}
          >
            <Heart
              size={20}
              className={`action-icon ${isLiked ? "liked" : ""}`}
            />
              <span className="action-count">{likesCount}</span>
        </button>

      );
}