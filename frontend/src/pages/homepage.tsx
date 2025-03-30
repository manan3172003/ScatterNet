import { SidebarLayout } from "@/components/sidebar-layout.tsx";
import InfiniteScroll from "@/components/infinite-scroll.tsx";
// import {SidebarInset} from "@/components/ui/sidebar.tsx";
// import {Header} from "@/components/header.tsx";

export function Homepage() {
  return (
      <SidebarLayout>
        {/*<SidebarInset className="sticky top-0 z-2 bg-background">*/}
        {/*  <Header/>*/}
        {/*</SidebarInset>*/}
        <div className="p-6">
          <InfiniteScroll/>
        </div>
      </SidebarLayout>
  )
}