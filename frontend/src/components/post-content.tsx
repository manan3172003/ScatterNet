import React, { useRef, useEffect } from 'react';
import MarkdownRenderer from "@/components/markdown.tsx";
import { Post } from "@/types/ModelTypes.tsx";
import { cn } from "@/lib/utils";

interface PostContentProps {
  post: Post;
  maxHeight: number;
  expanded: boolean;
  setShouldShowReadMore: (value: boolean) => void;
  className?: string;
}

const PostContent: React.FC<PostContentProps> = ({
  post,
  maxHeight,
  expanded,
  setShouldShowReadMore,
  className
}) => {
  const contentRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (contentRef.current) {
      const shouldTruncate = contentRef.current.scrollHeight > maxHeight;
      setShouldShowReadMore(shouldTruncate);
    }
  }, [post.content, maxHeight, post.contentType]);

  const contentStyle = !expanded ? { maxHeight: `${maxHeight}px`, overflow: 'hidden' } : {};

  if (post.contentType === 'text/plain') {
    return (
      <div ref={contentRef} style={contentStyle} className="text-sm text-muted-foreground break-words w-full">
        {post.content}
      </div>
    );
  } else if (post.contentType === 'text/markdown') {
    return (
      <div ref={contentRef} style={contentStyle} className={cn("dark:prose !prose-invert break-words w-full", className)}>
        <MarkdownRenderer>{post.content}</MarkdownRenderer>
      </div>
    );
  } else if (post.contentType === "image/png;base64" || post.contentType === "image/jpeg;base64" || post.contentType === "application/base64") {
    return (
      <div className="w-full aspect-video relative">
        <img
          src={`${post.id}/image`}
          alt={post.title}
          className="object-contain rounded-md w-full h-full"
          loading="lazy"
        />
      </div>
    );
  } else {
    return null;
  }
};

export default PostContent;
