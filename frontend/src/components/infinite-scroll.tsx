import { useEffect, useState, useRef, useCallback } from 'react';
import {Post} from "@/types/ModelTypes.tsx";
import {apiCall} from "@/utils/ApiCall.tsx";
import ContentCard from "@/components/post.tsx";

export default function InfiniteScroll() {
    const [posts, setPosts] = useState<Post[]>([]);
    const [page, setPage] = useState<number>(1);
    const [hasMore, setHasMore] = useState<boolean>(true);
    const [loading, setLoading] = useState<boolean>(false);
    const [error, setError] = useState<string | null>(null);
    const observer = useRef<IntersectionObserver | null>(null);
    const POSTS_PER_PAGE = 5;

    const fetchPosts = async (pageNum: number) => {
      if (loading) return;

      setLoading(true);
      try {
        const res = await apiCall(
          `posts?page=${pageNum}&size=${POSTS_PER_PAGE}`,
        );
        const data = await res.json();
        setPosts((prev) => [...prev, ...data.src || []]);
        if (data.next === null) {
          setHasMore(false);
        }
      } catch (err) {
        setError('An error occurred while fetching data.');
      } finally {
        setLoading(false);
      }
    };

    const lastPostElementRef = useCallback(
      (node: HTMLDivElement) => {
        if (loading) return;
        if (observer.current) observer.current.disconnect();
        observer.current = new IntersectionObserver(
          (entries) => {
            if (entries[0].isIntersecting && hasMore) {
              setPage((prevPage) => prevPage + 1);
            }
          },
          { threshold: 1.0 }
        );
        if (node) observer.current.observe(node);
      },
      [loading, hasMore]
    );

    useEffect(() => {
        fetchPosts(page);
    }, [page]);

    return (
  <div className="p-4">
    {posts.map((post, index) => {
      if (posts.length === index + 1) {
        return (
          <div
            ref={lastPostElementRef}
            key={post.id}
          >
            <ContentCard
                post={post}
            />
          </div>
        );
      } else {
        return (
          <div key={post.id} className="pb-6">
            <ContentCard
                post={post}
            />
          </div>
        );
      }
    })}
    {loading && <p className="text-center py-4">Loading...</p>}
    {error && <p className="text-center text-red-500 py-4">{error}</p>}
  </div>
);}
