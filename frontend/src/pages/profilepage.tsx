import {SidebarLayout} from "@/components/sidebar-layout.tsx";
import {useParams} from "react-router-dom";

export function Profilepage() {
    const { author_serial } = useParams();

  return (
      <SidebarLayout>
        <div>
          ProfilePage of author {author_serial}
        </div>
      </SidebarLayout>
  )
}