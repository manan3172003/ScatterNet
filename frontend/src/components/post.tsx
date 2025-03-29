// import React from 'react';
// import { Card, CardHeader, CardTitle, CardContent, CardDescription } from '@/components/ui/card';
// import ReactMarkdown from 'react-markdown';
// import { cn } from "@/lib/utils";
//
//
// interface ContentCardProps {
//   type: 'text' | 'markdown' | 'image';
//   title: string;
//   content: string;
//   description?: string;
//   className?: string;
// }
//
// const ContentCard: React.FC<ContentCardProps> = ({
//   type,
//   title,
//   content,
//   description,
//   className
// }) => {
//   const renderContent = () => {
//     switch (type) {
//       case 'text':
//         return <p className="text-sm text-muted-foreground">{content}</p>;
//
//       case 'markdown':
//         return (
//           <div className="prose prose-sm dark:prose-invert">
//             <ReactMarkdown>{content}</ReactMarkdown>
//           </div>
//         );
//
//       case 'image':
//         return (
//           <div className="w-full aspect-video relative">
//             <img
//               src={content}
//               alt={title}
//               className="object-cover rounded-md w-full h-full"
//               loading="lazy"
//             />
//           </div>
//         );
//
//       default:
//         return null;
//     }
//   };
//
//   return (
//     <Card className={cn("w-full max-w-md mx-auto", className)}>
//       <CardHeader>
//         <CardTitle>{title}</CardTitle>
//         {description && (
//           <CardDescription>{description}</CardDescription>
//         )}
//       </CardHeader>
//       <CardContent>
//         {renderContent()}
//       </CardContent>
//     </Card>
//   );
// };
//
// export default ContentCard;

import React, { useState } from 'react';
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
  EyeOff
} from 'lucide-react';
import { cn } from "@/lib/utils";
import MarkdownRenderer from "@/components/markdown.tsx";
// import remarkGfm from "remark-gfm";

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
  onFollow
}) => {
  const [liked, setLiked] = useState(false);
  const [likes, setLikes] = useState(stats.likes || 0);

  const renderContent = () => {
      if (type === 'text/plain') {
        return <p className="text-sm text-muted-foreground break-words">{content}</p>;
      } else if (type === 'text/markdown') {
        return (
            <div className={cn("dark:prose !prose-invert break-words", className)}>
              <MarkdownRenderer>{content}</MarkdownRenderer>
            </div>
        );
      } else if (type === "image/png;base64" || type === "image/jpeg;base64" || type === "application/base64") {
        return (
            <div className="w-full aspect-video relative">
              <img
                  src={`${id}/image`}
                  alt={title}
                  className="object-cover rounded-md w-full h-full"
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

  return (
    <Card className={cn("w-full max-w-md mx-auto", className)}>
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
            <CardDescription >{description}</CardDescription>
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
      <CardContent>
        <>
          {renderContent()}
          <div className="flex justify-between items-center mt-4">
            <div className="flex items-center space-x-4">
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
                {onEdit && (
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={onEdit}
                  >
                    <Edit className="w-4 h-4" />
                  </Button>
                )}
                {onDelete && (
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={onDelete}
                    className="text-red-500 hover:text-red-700"
                  >
                    <Trash2 className="w-4 h-4" />
                  </Button>
                )}
              </div>
            )}
          </div>
        </>
      </CardContent>
    </Card>
  );
};

export default ContentCard;