import { SidebarLayout } from "@/components/sidebar-layout.tsx";
import ContentCard from "@/components/post.tsx"
import {apiCall} from "@/utils/ApiCall.tsx";
import {useEffect, useState} from "react";
import {Post} from "@/types/ModelTypes.tsx";

export function Homepage() {
  // Use state to manage the data and loading state
  const [data, setData] = useState<Post | null>(null);
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
        const response = await apiCall('authors/2/posts/2');
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
            post={data!}
          />
        </div>
      </SidebarLayout>
  )
}