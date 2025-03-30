import React from 'react';
import { Dialog, DialogTrigger, DialogContent, DialogHeader, DialogTitle, DialogDescription } from "@/components/ui/dialog";
import { Button } from '@/components/ui/button';
import { MessageCircle } from 'lucide-react';
import { useMediaQuery } from '@mantine/hooks'; // Hook for media queries
import { Post } from "@/types/ModelTypes"
import {Card} from "@/components/ui/card.tsx";

// Desktop modal component
const DesktopModal: React.FC = () => (
  <DialogContent className="[&>button]:hidden">
    <Card className="p-6"></Card>
  </DialogContent>
);

// Mobile modal component
const MobileModal: React.FC = () => (
  <DialogContent className="p-4 w-full rounded-t-md">
    <DialogHeader>
      <DialogTitle>Comments (Mobile View)</DialogTitle>
      <DialogDescription>Leave a comment below (mobile)</DialogDescription>
    </DialogHeader>
    <div className="p-4">
      <textarea className="w-full p-2 border rounded-md" placeholder="Write a comment..." />
      <Button className="mt-2 w-full">Post Comment</Button>
    </div>
  </DialogContent>
);

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
      {/* Render DesktopModal or MobileModal based on the screen size */}
      {isMobile ? <MobileModal /> : <DesktopModal />}
    </Dialog>
  );
};

export default CommentModal;
