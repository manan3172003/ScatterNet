import * as React from "react"

import {
  Sidebar,
  SidebarContent, SidebarHeader,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
  SidebarRail,
} from "@/components/ui/sidebar"
import {useContext} from "react";
import {AuthContext} from "@/context/AuthContext.tsx";
import {getCookie} from "@/utils/ApiCall.tsx";

export function AppSidebar({ ...props }: React.ComponentProps<typeof Sidebar>) {

  const { user } = useContext(AuthContext);
  const isAdmin = getCookie("isAdmin") === "true";

  // Simplified navigation data
  const data = [
    {
      title: "Home",
      url: "/home",
    },
    {
      title: "Post",
      url: "/post",
    },
    {
      title: "Profile",
      url: `/authors/${user!.author_id}`,
    },
    {
      title: "Followers",
      url: "/requests",
    },
    ...(isAdmin ? [{
      title: "Admin",
      url: "/admin",
    }] : [])
  ]

  return (
    <Sidebar {...props}>
      <SidebarHeader>
      </SidebarHeader>
      <SidebarContent>
        <SidebarMenu className="p-6">
          {data.map((item) => (
            <SidebarMenuItem key={item.title}>
              <SidebarMenuButton
                asChild
              >
                <a href={item.url}>{item.title}</a>
              </SidebarMenuButton>
            </SidebarMenuItem>
          ))}
        </SidebarMenu>
      </SidebarContent>
      <SidebarRail/>
    </Sidebar>
  )
}