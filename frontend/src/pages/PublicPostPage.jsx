import { useEffect, useState } from "react";
import Post from "../components/Post";
import { useParams } from "react-router-dom";

export default function PublicPostPage() {
  const { authorId, postId } = useParams();
  const [post, setPost] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchPost() {
      try {
        const response = await fetch(
          `http://localhost:8000/api/authors/${authorId}/posts/${postId}`
        );
        if (!response.ok) throw new Error("Post not found");
        const data = await response.json();
        setPost(data);
      } catch (error) {
        console.error("Error fetching post:", error);
      } finally {
        setLoading(false);
      }
    }

    fetchPost();
  }, [authorId, postId]);

  return (
    <div className="post-page-container">
      {loading ? (
        <p>Loading...</p>
      ) : post ? (
        <Post post={post} />
      ) : (
        <p>Post not found</p>
      )}
    </div>
  );
}
