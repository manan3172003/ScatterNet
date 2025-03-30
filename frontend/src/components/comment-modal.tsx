import React from 'react';
import { Dialog, DialogTrigger, DialogContent, DialogHeader, DialogTitle, DialogDescription } from "@/components/ui/dialog";
import { Button } from '@/components/ui/button';
import { MessageCircle } from 'lucide-react';
import { useMediaQuery } from '@mantine/hooks'; // Hook for media queries
import { Post } from "@/types/ModelTypes"

interface CommentModalProps {
  post: Post;
}

const CommentModal: React.FC<CommentModalProps> = ({ post }) => {
  // Use media query to detect if the screen size is smaller than 768px (mobile breakpoint)
  const isMobile = useMediaQuery('(max-width: 768px)');

  return (
    <Dialog>
      <DialogTrigger asChild>
        <Button variant="ghost" size="sm" className="flex items-center gap-2">
          <MessageCircle className="w-4 h-4" />
          {post.comments.count}
        </Button>
      </DialogTrigger>
      <DialogContent
        className={isMobile ? "p-4 w-full rounded-t-md" : "p-4 w-[500px] mx-auto"} // Mobile: full width, larger screens: centered modal
      >
        <DialogHeader>
          <DialogTitle>{isMobile ? 'Comments (Mobile View)' : 'Comments'}</DialogTitle>
          <DialogDescription>
            {isMobile ? 'Leave a comment below (mobile)' : 'Leave a comment below'}
          </DialogDescription>
        </DialogHeader>
        {/* Add your comment form or comment section here */}
        <div className="p-4">
          {/* Comment input form */}
          <textarea
            className="w-full p-2 border rounded-md"
            placeholder="Write a comment..."
          />
          <Button className="mt-2 w-full">Post Comment</Button>
        </div>
      </DialogContent>
    </Dialog>
  );
};

export default CommentModal;
