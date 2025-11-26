import { MessageSquare, Folder, ChevronRight } from "lucide-react";
import { NavLink } from "@/components/NavLink";
import {
  Sidebar,
  SidebarContent,
  SidebarGroup,
  SidebarGroupContent,
  SidebarGroupLabel,
  SidebarMenu,
  SidebarMenuItem,
  SidebarMenuButton,
  useSidebar,
  SidebarHeader,
} from "@/components/ui/sidebar";
import { Collapsible, CollapsibleContent, CollapsibleTrigger } from "@/components/ui/collapsible";
import { useState } from "react";

const recentChats = [
  { id: 1, title: "Attention mechanism research", date: "Today" },
  { id: 2, title: "Transformer architectures", date: "Yesterday" },
  { id: 3, title: "NLP survey papers", date: "2 days ago" },
];

const folders = [
  { id: 1, name: "Attention Papers", count: 12 },
  { id: 2, name: "Deep Learning", count: 8 },
  { id: 3, name: "Computer Vision", count: 5 },
];

export function AppSidebar() {
  const { open } = useSidebar();
  const [foldersOpen, setFoldersOpen] = useState(true);

  return (
    <Sidebar className="border-r">
      <SidebarHeader className="border-b p-4">
        <h2 className="font-semibold text-sidebar-foreground">Navigation</h2>
      </SidebarHeader>
      <SidebarContent>
        <SidebarGroup>
          <SidebarGroupLabel>Recent Chats</SidebarGroupLabel>
          <SidebarGroupContent>
            <SidebarMenu>
              {recentChats.map((chat) => (
                <SidebarMenuItem key={chat.id}>
                  <SidebarMenuButton asChild>
                    <button className="flex w-full items-center gap-2 hover:bg-sidebar-accent">
                      <MessageSquare className="h-4 w-4" />
                      {open && (
                        <div className="flex flex-1 flex-col items-start overflow-hidden">
                          <span className="truncate text-sm">{chat.title}</span>
                          <span className="text-xs text-muted-foreground">{chat.date}</span>
                        </div>
                      )}
                    </button>
                  </SidebarMenuButton>
                </SidebarMenuItem>
              ))}
            </SidebarMenu>
          </SidebarGroupContent>
        </SidebarGroup>

        <Collapsible open={foldersOpen} onOpenChange={setFoldersOpen}>
          <SidebarGroup>
            <CollapsibleTrigger asChild>
              <SidebarGroupLabel className="flex cursor-pointer items-center justify-between hover:bg-sidebar-accent">
                <span>Project Folders</span>
                <ChevronRight
                  className={`h-4 w-4 transition-transform ${foldersOpen ? "rotate-90" : ""}`}
                />
              </SidebarGroupLabel>
            </CollapsibleTrigger>
            <CollapsibleContent>
              <SidebarGroupContent>
                <SidebarMenu>
                  {folders.map((folder) => (
                    <SidebarMenuItem key={folder.id}>
                      <SidebarMenuButton asChild>
                        <NavLink
                          to={`/folder/${folder.id}`}
                          className="flex w-full items-center gap-2 hover:bg-sidebar-accent"
                        >
                          <Folder className="h-4 w-4" />
                          {open && (
                            <>
                              <span className="flex-1 truncate text-sm">{folder.name}</span>
                              <span className="text-xs text-muted-foreground">
                                {folder.count}
                              </span>
                            </>
                          )}
                        </NavLink>
                      </SidebarMenuButton>
                    </SidebarMenuItem>
                  ))}
                </SidebarMenu>
              </SidebarGroupContent>
            </CollapsibleContent>
          </SidebarGroup>
        </Collapsible>
      </SidebarContent>
    </Sidebar>
  );
}

