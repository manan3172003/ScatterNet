import { useState, useEffect } from 'react';
import { ScrollArea } from '@/components/ui/scroll-area';
import { Card, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';

const CommentList = () => {
  const [items, setItems] = useState(Array.from({ length: 20 }, (_, i) => `Item ${i + 1}`));
  const [isFetching, setIsFetching] = useState(false);

  useEffect(() => {
    const handleScroll = (e) => {
      const { scrollTop, scrollHeight, clientHeight } = e.target;
      if (scrollHeight - scrollTop === clientHeight && !isFetching) {
        fetchMoreItems();
      }
    };
    const scrollArea = document.getElementById('infinite-scroll-area');
    if (scrollArea) {
      scrollArea.addEventListener('scroll', handleScroll);
    }
    return () => scrollArea?.removeEventListener('scroll', handleScroll);
  }, [isFetching]);

  const fetchMoreItems = () => {
    setIsFetching(true);
    setTimeout(() => {
      setItems((prevItems) => [
        ...prevItems,
        ...Array.from({ length: 20 }, (_, i) => `Item ${prevItems.length + i + 1}`),
      ]);
      setIsFetching(false);
    }, 1000);
  };

  return (
    <ScrollArea id="infinite-scroll-area" className="h-[300px] w-full rounded-md border p-4">
      {items.map((item, index) => (
        <Card key={index} className="mb-2">
          <CardContent>{item}</CardContent>
        </Card>
      ))}
      {isFetching && <Button disabled>Loading more...</Button>}
    </ScrollArea>
  );
};

export default CommentList;