import { SidebarLayout } from "@/components/sidebar-layout.tsx";
import ContentCard from "@/components/post.tsx"
import {apiCall} from "@/utils/ApiCall.tsx";
import {useEffect, useState} from "react";

export function Homepage() {
  interface PostData {
    id: string;
    title: string;
    description: string;
    contentType: 'text/plain' | 'text/markdown' | 'image/png;base64' | 'image/jpeg;base64' | 'application/base64';
    content:string;
    author: {
      id: string,
      displayName: string,
      profileImage: string,
    };
    visibility: 'PUBLIC' | 'FRIENDS' | 'UNLISTED' | 'DELETED';

  }

  // Use state to manage the data and loading state
  const [data, setData] = useState<PostData | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    // Create an async function inside useEffect
    const fetchData = async () => {
      try {
        // Reset loading and error states
        setIsLoading(true);
        setError(null);

        // Make the API call
        const response = await apiCall('authors/2/posts/3');
        const responseData = await response.json();

        // Update state with fetched data
        setData(responseData);
        setIsLoading(false);
      } catch (err) {
        // Handle any errors during fetching
        setError('Failed to load post data');
        setIsLoading(false);
        console.error('Error fetching data:', err);
      }
    };

    // Call the async function
    fetchData();
  }, []); // Empty dependency array means this runs once on component mount

  // Handle loading and error states
  if (isLoading) {
    return <div>Loading...</div>;
  }

  if (error) {
    return <div>Error: {error}</div>;
  }


  return (
      <SidebarLayout>
        <div className="p-6">
          <ContentCard
              id ={data!.id}
              type ={data!.contentType}
              title ={data!.title}
              content ={data!.content}
              description = {data!.description}
              user = {{
                id: data!.author.id,
                username: data!.author.displayName,
                profilePicture: data!.author.profileImage,
                isCurrentUser: true
              }}
              visibility = {data!.visibility}
          />
        </div>
      </SidebarLayout>
  )
}