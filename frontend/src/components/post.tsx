import React, { useState, useRef, useEffect } from 'react';
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
  EyeOff,
  ChevronDown,
  ChevronUp
} from 'lucide-react';
import { cn } from "@/lib/utils";
import MarkdownRenderer from "@/components/markdown.tsx";

interface ContentCardProps {
  id: string;
  type: 'text/plain' | 'text/markdown' | 'image/png;base64' | 'image/jpeg;base64' | 'application/base64';
  title: string;
  content: string;
  description?: string;
  className?: string;
  user: {
    id: string;
    username: string;
    profilePicture?: string;
    isCurrentUser?: boolean;
  };
  visibility: 'PUBLIC' | 'FRIENDS' | 'UNLISTED' | 'DELETED';
  stats?: {
    likes?: number;
    comments?: number;
  };
  onEdit?: () => void;
  onDelete?: () => void;
  onFollow?: () => void;
  maxHeight?: number;
}

const ContentCard: React.FC<ContentCardProps> = ({
  id,
  type,
  title,
  content,
  description,
  className,
  user,
  visibility,
  stats = { likes: 0, comments: 0 },
  onEdit,
  onDelete,
  onFollow,
  maxHeight = 300 // Default max height in pixels before showing "Read more"
}) => {
  const [liked, setLiked] = useState(false);
  const [likes, setLikes] = useState(stats.likes || 0);
  const [expanded, setExpanded] = useState(false);
  const [shouldShowReadMore, setShouldShowReadMore] = useState(false);
  const contentRef = useRef<HTMLDivElement>(null);

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

    // Add resize listener
    window.addEventListener('resize', checkHeight);

    // Clean up
    return () => window.removeEventListener('resize', checkHeight);
  }, [content, maxHeight, type]);

  const renderContent = () => {
    const contentStyle = shouldShowReadMore && !expanded
      ? { maxHeight: `${maxHeight}px`, overflow: 'hidden' }
      : {};

    if (type === 'text/plain') {
      return (
        <div ref={contentRef} style={contentStyle} className="text-sm text-muted-foreground break-words w-full">
          {content}
        </div>
      );
    } else if (type === 'text/markdown') {
      return (
        <div
          ref={contentRef}
          style={contentStyle}
          className={cn("dark:prose !prose-invert break-words w-full", className)}
        >
          <MarkdownRenderer>{content}</MarkdownRenderer>
        </div>
      );
    } else if (type === "image/png;base64" || type === "image/jpeg;base64" || type === "application/base64") {
      return (
        <div className="w-full aspect-video relative">
          <img
            src={`${id}/image`}
            alt={title}
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
    switch (visibility) {
      case 'PUBLIC':
        return <Globe className="w-4 h-4 text-green-500" />;
      case 'FRIENDS':
        return <Lock className="w-4 h-4 text-yellow-500" />;
      case 'UNLISTED':
        return <EyeOff className="w-4 h-4 text-gray-500" />;
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
            src={user.profilePicture}
            alt={`${user.username}'s profile`}
          />
          <AvatarFallback>
            {user.username.charAt(0).toUpperCase()}
          </AvatarFallback>
        </Avatar>
        <div className="flex-1">
          <div className="flex items-center space-x-2">
            <CardTitle>{user.username}</CardTitle>
            {renderPrivacyIcon()}
          </div>
          <div className="mx-auto">
            {description && (
              <CardDescription>{description}</CardDescription>
            )}
          </div>
        </div>
        {!user.isCurrentUser && onFollow && (
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
                {stats.comments || 0}
              </Button>
              <Button variant="ghost" size="sm">
                <Share2 className="w-4 h-4" />
              </Button>
            </div>
            {user.isCurrentUser && (
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