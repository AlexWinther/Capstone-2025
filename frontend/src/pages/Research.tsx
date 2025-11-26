import { useState } from "react";
import { ChatInput } from "@/components/chat/ChatInput";
import { ChatMessage } from "@/components/chat/ChatMessage";
import { ResearchResults } from "@/components/research/ResearchResults";

const Research = () => {
  const [messages, setMessages] = useState<Array<{
    role: "user" | "assistant";
    content: string;
  }>>([]);
  const [showResults, setShowResults] = useState(false);

  const handleSendMessage = (message: string) => {
    setMessages([...messages, {
      role: "user",
      content: message
    }]);

    // Simulate AI response
    setTimeout(() => {
      setMessages(prev => [...prev, {
        role: "assistant",
        content: "I'm searching through the research database to find papers related to your query..."
      }]);

      // Show structured results after a delay
      setTimeout(() => {
        setShowResults(true);
      }, 1500);
    }, 500);
  };

  return (
    <div className="flex h-[calc(100vh-4rem)] flex-col">
      {messages.length === 0 ? (
        <div className="flex h-full flex-col items-center justify-center px-6">
          <div className="w-full max-w-3xl space-y-8 text-center">
            <div className="space-y-4">
              <h1 className="text-4xl font-bold tracking-tight text-foreground">
                Welcome to FraunhoferAI
              </h1>
              <p className="text-lg text-muted-foreground">
                Your AI research assistant for exploring scientific literature
              </p>
            </div>
            <div className="w-full">
              <ChatInput onSend={handleSendMessage} />
            </div>
            <div className="grid gap-3 text-left text-sm text-muted-foreground sm:grid-cols-2">
              <div className="rounded-lg border bg-card/50 p-4">
                <p className="font-medium text-foreground">Find related papers</p>
                <p className="mt-1">Ask about papers related to your research topic</p>
              </div>
              <div className="rounded-lg border bg-card/50 p-4">
                <p className="font-medium text-foreground">Discover connections</p>
                <p className="mt-1">Explore relationships between different research areas</p>
              </div>
            </div>
          </div>
        </div>
      ) : (
        <>
          <div className="flex-1 overflow-auto p-6">
            <div className="mx-auto max-w-4xl space-y-6">
              {messages.map((message, index) => (
                <ChatMessage key={index} role={message.role} content={message.content} />
              ))}
              {showResults && <ResearchResults />}
            </div>
          </div>
          <div className="sticky bottom-0 border-t bg-background/95 p-3 backdrop-blur supports-[backdrop-filter]:bg-background/80">
            <div className="mx-auto max-w-4xl">
              <ChatInput onSend={handleSendMessage} compact />
            </div>
          </div>
        </>
      )}
    </div>
  );
};

export default Research;

