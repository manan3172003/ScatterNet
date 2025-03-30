import React, {useState, useRef, useEffect, useContext} from 'react';
import { Card, CardHeader, CardContent, CardDescription, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar';
import {
  Heart,
  MessageCircle,
  Share2,
  Edit,
  Trash2,
  UserPlus,
  Lock,
  Globe,
  ChevronDown,
  ChevronUp, Link
} from 'lucide-react';
import { cn } from "@/lib/utils";
import MarkdownRenderer from "@/components/markdown.tsx";
import {Post} from "@/types/ModelTypes.tsx";
import {AuthContext} from "@/context/AuthContext.tsx";

interface ContentCardProps {
  post: Post;
  className?: string;
  maxHeight?: number;
}

const ContentCard: React.FC<ContentCardProps> = ({
  post,
  className,
  maxHeight = 300 // Default max height in pixels before showing "Read more"
}) => {
  const [liked, setLiked] = useState(false);
  const [likes, setLikes] = useState(post.likes.count || 0);
  const [expanded, setExpanded] = useState(false);
  const [shouldShowReadMore, setShouldShowReadMore] = useState(false);
  const contentRef = useRef<HTMLDivElement>(null);
  const [isCurrentUser, setIsCurrentUser] = useState<boolean | null>(null);
  const { user } = useContext(AuthContext);

  // Check if content exceeds max height on mount and on window resize
  useEffect(() => {
    const checkHeight = () => {
      if (contentRef.current) {
        const shouldTruncate = contentRef.current.scrollHeight > maxHeight;
        setShouldShowReadMore(shouldTruncate);
      }
    };

    // Run on initial render and whenever content changes
    checkHeight();
    if (user!.author_id != post.author.serial) {
      setIsCurrentUser(false);
    } else {
      setIsCurrentUser(true);
    }

    // Add resize listener
    window.addEventListener('resize', checkHeight);

    // Clean up
    return () => window.removeEventListener('resize', checkHeight);
  }, [post.content, maxHeight, post.contentType]);

  const onFollow = () => {

  }

  const onEdit = () => {

  }

  const onDelete = () => {

  }

  const renderContent = () => {
    const contentStyle = shouldShowReadMore && !expanded
      ? { maxHeight: `${maxHeight}px`, overflow: 'hidden' }
      : {};

    if (post.contentType === 'text/plain') {
      return (
        <div ref={contentRef} style={contentStyle} className="text-sm text-muted-foreground break-words w-full">
          {post.content}
        </div>
      );
    } else if (post.contentType === 'text/markdown') {
      return (
        <div
          ref={contentRef}
          style={contentStyle}
          className={cn("dark:prose !prose-invert break-words w-full", className)}
        >
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

  const renderPrivacyIcon = () => {
    switch (post.visibility) {
      case 'PUBLIC':
        return <Globe className="w-4 h-4 text-green-500" />;
      case 'FRIENDS':
        return <Lock className="w-4 h-4 text-yellow-500" />;
      case 'UNLISTED':
        return <Link className="w-4 h-4 text-gray-500" />;
      case 'DELETED':
        return <Trash2 className="w-4 h-4 text-red-500" />;
      default:
        return null;
    }
  };

  const handleLike = () => {
    setLiked(!liked);
    setLikes(liked ? likes - 1 : likes + 1);
  };

  const toggleExpand = () => {
    setExpanded(!expanded);
  };

  return (
    <Card className={cn("w-full mx-auto max-w-full lg:max-w-2xl", className)}>
      <CardHeader className="flex flex-row items-center space-x-4">
        <Avatar>
          <AvatarImage
            src={post.author.profileImage}
            alt={`${post.author.displayName}'s profile`}
          />
          <AvatarFallback>
            {post.author.displayName.charAt(0).toUpperCase()}
          </AvatarFallback>
        </Avatar>
        <div className="flex-1">
          <div className="flex items-center space-x-2">
            <CardTitle>{post.author.displayName}</CardTitle>
            {renderPrivacyIcon()}
          </div>
          <div className="mx-auto">
            {post.description && (
              <CardDescription>{post.description}</CardDescription>
            )}
          </div>
        </div>
        {!isCurrentUser && onFollow && (
          <Button
            variant="outline"
            size="sm"
            onClick={onFollow}
            className="flex items-center gap-2"
          >
            <UserPlus className="w-4 h-4" /> Follow
          </Button>
        )}
      </CardHeader>
      <CardContent className="w-full">
        <div className="w-full">
          {renderContent()}

          {shouldShowReadMore && (
            <Button
              variant="ghost"
              size="sm"
              onClick={toggleExpand}
              className="mt-2 flex items-center gap-1 text-primary"
            >
              {expanded ? (
                <>Show less <ChevronUp className="w-4 h-4" /></>
              ) : (
                <>Read more <ChevronDown className="w-4 h-4" /></>
              )}
            </Button>
          )}

          <div className="flex justify-between items-center mt-4">
            <div className="flex items-center space-x-2">
              <Button
                variant="ghost"
                size="sm"
                onClick={handleLike}
                className={cn(
                  "flex items-center gap-2",
                  liked && "text-red-500"
                )}
              >
                <Heart
                  className={cn(
                    "w-4 h-4",
                    liked ? "fill-current" : "stroke-current"
                  )}
                />
                {likes}
              </Button>
              <Button variant="ghost" size="sm" className="flex items-center gap-2">
                <MessageCircle className="w-4 h-4" />
                {post.comments.count || 0}
              </Button>
              <Button variant="ghost" size="sm">
                <Share2 className="w-4 h-4" />
              </Button>
            </div>
            {isCurrentUser && (
              <div className="flex items-center space-x-2">
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={onEdit}
                >
                  <Edit className="w-4 h-4" />
                </Button>
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={onDelete}
                  className="text-red-500 hover:text-red-700"
                >
                  <Trash2 className="w-4 h-4" />
                </Button>
              </div>
            )}
          </div>
        </div>
      </CardContent>
    </Card>
  );
};

export default ContentCard;