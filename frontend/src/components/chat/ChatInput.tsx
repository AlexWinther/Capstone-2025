import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { Send, Paperclip } from "lucide-react";

interface ChatInputProps {
  onSend: (message: string) => void;
  compact?: boolean;
}

export const ChatInput = ({ onSend, compact = false }: ChatInputProps) => {
  const [message, setMessage] = useState("");

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (message.trim()) {
      onSend(message);
      setMessage("");
    }
  };

  return (
    <form onSubmit={handleSubmit} className={`w-full transition-all duration-300 ${compact ? '' : 'space-y-3'}`}>
      {compact ? (
        <div className="flex items-center gap-2 rounded-xl border bg-background p-2 shadow-sm transition-shadow hover:shadow-md focus-within:shadow-md">
          <Button 
            type="button" 
            variant="ghost" 
            size="icon"
            className="h-8 w-8 shrink-0 text-muted-foreground hover:text-foreground"
          >
            <Paperclip className="h-4 w-4" />
          </Button>
          <Textarea
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            placeholder="Ask a research question..."
            className="min-h-[40px] max-h-[120px] resize-none border-0 bg-transparent p-2 text-sm shadow-none focus-visible:ring-0"
            rows={1}
            onKeyDown={(e) => {
              if (e.key === "Enter" && !e.shiftKey) {
                e.preventDefault();
                handleSubmit(e);
              }
            }}
          />
          <Button 
            type="submit" 
            size="icon"
            className="h-8 w-8 shrink-0"
            disabled={!message.trim()}
          >
            <Send className="h-4 w-4" />
          </Button>
        </div>
      ) : (
        <>
          <Textarea
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            placeholder="Ask a research question (e.g., 'What papers are related to Attention is All You Need?')"
            className="min-h-[120px] resize-none text-base"
            onKeyDown={(e) => {
              if (e.key === "Enter" && !e.shiftKey) {
                e.preventDefault();
                handleSubmit(e);
              }
            }}
          />
          <div className="flex items-center justify-between">
            <Button 
              type="button" 
              variant="outline" 
              size="sm" 
              className="gap-2 text-muted-foreground hover:text-foreground"
            >
              <Paperclip className="h-4 w-4" />
              Attach document
            </Button>
            <Button 
              type="submit" 
              size="sm" 
              className="gap-2 font-medium"
              disabled={!message.trim()}
            >
              <Send className="h-4 w-4" />
              Send message
            </Button>
          </div>
        </>
      )}
    </form>
  );
};

