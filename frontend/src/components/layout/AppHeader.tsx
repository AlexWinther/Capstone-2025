import { SidebarTrigger } from "@/components/ui/sidebar";
import { FlaskConical } from "lucide-react";
import { NavLink } from "@/components/NavLink";
export const AppHeader = () => {
  return <header className="sticky top-0 z-50 flex h-16 items-center gap-4 border-b bg-card px-6">
      <SidebarTrigger className="-ml-2" />
      <div className="flex items-center gap-2">
        <FlaskConical className="h-6 w-6 text-primary" />
        <h1 className="text-xl font-bold text-foreground">FraunhoferAI</h1>
      </div>
      <nav className="ml-auto flex items-center gap-6">
        <NavLink to="/" end className="text-sm font-medium text-muted-foreground transition-colors hover:text-foreground" activeClassName="text-primary">
          Research
        </NavLink>
        <NavLink to="/profile" className="text-sm font-medium text-muted-foreground transition-colors hover:text-foreground" activeClassName="text-primary">
          Profile
        </NavLink>
      </nav>
    </header>;
};

