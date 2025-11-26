import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import { FlaskConical, User } from "lucide-react";

interface ChatMessageProps {
  role: "user" | "assistant";
  content: string;
}

export const ChatMessage = ({ role, content }: ChatMessageProps) => {
  return (
    <div className={`flex gap-4 ${role === "user" ? "justify-end" : ""}`}>
      {role === "assistant" && (
        <Avatar className="h-8 w-8 bg-primary">
          <AvatarFallback>
            <FlaskConical className="h-4 w-4 text-primary-foreground" />
          </AvatarFallback>
        </Avatar>
      )}
      <div
        className={`max-w-[80%] rounded-lg p-4 ${
          role === "user"
            ? "bg-primary text-primary-foreground"
            : "bg-card border"
        }`}
      >
        <p className="text-sm leading-relaxed">{content}</p>
      </div>
      {role === "user" && (
        <Avatar className="h-8 w-8 bg-secondary">
          <AvatarFallback>
            <User className="h-4 w-4 text-secondary-foreground" />
          </AvatarFallback>
        </Avatar>
      )}
    </div>
  );
};

