import {AppSidebar} from "@/components/app-sidebar.tsx";
import {SidebarInset, SidebarProvider, SidebarTrigger} from "@/components/ui/sidebar.tsx";

interface SidebarLayoutProps {
    children: React.ReactNode;
}

export function SidebarLayout({children}: SidebarLayoutProps) {
    return (
    <SidebarProvider>
      <AppSidebar />
      <SidebarInset>
        <header className="flex sticky top-0 bg-background h-16 shrink-0 items-center gap-2 border-b px-4 z-1">
          <SidebarTrigger className="-ml-1" />
        </header>
          { children }
      </SidebarInset>
    </SidebarProvider>
  )
}