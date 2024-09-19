"use client";
import { useState, useEffect, useRef } from "react";
import {
  Card,
  CardHeader,
  CardTitle,
  CardDescription,
  CardContent,
  CardFooter,
} from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import LLMOutputRenderer from "@/components/LLMOutputRenderer";
import { ImageGallery } from "@/components/ImageGallery";
import { useStreamExample, throttleBasic } from "@llm-ui/react";

const Page = () => {
  const [messages, setMessages] = useState<
    {
      sender: string;
      text?: string;
      isMeowy?: boolean;
      showGallery?: boolean;
      imageUrls?: string[];
    }[]
  >([]);
  const [inputValue, setInputValue] = useState("");
  const [meowyResponse, setMeowyResponse] = useState("");
  const [messageKey, setMessageKey] = useState(0);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    if (messagesEndRef.current) {
      messagesEndRef.current.scrollIntoView({ behavior: "smooth" });
    }
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const sendMessage = async () => {
    if (inputValue.trim()) {
      // Add user's message
      setMessages((prev) => [...prev, { sender: "user", text: inputValue }]);
      setInputValue(""); // Clear input field

      // Fetch request with cookies included
      const response = await fetch("http://localhost:8000/api/chat/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ user_input: inputValue }),
        credentials: "include", // Include cookies in the request
      });

      const data = await response.json();

      // Check if there are URLs to render in the gallery
      const showGallery = data.urls.length > 0;

      setMessages((prev) => [
        ...prev,
        {
          sender: "meowy",
          text: data.response,
          isMeowy: true,
          showGallery,
          imageUrls: data.urls,
        },
      ]);

      setMessageKey((prevKey) => prevKey + 1); // Force re-render
    }
  };

  return (
    <div className="flex min-h-screen flex-col items-center bg-black p-4 text-white">
      {/* Chat Area with padding-bottom to account for input field */}
      <div className="w-full max-w-lg flex-grow space-y-4 overflow-y-auto pb-24 shadow-lg">
        {messages.map((message, index) => (
          <Card key={index} className="text-white">
            <CardHeader>
              <CardTitle>
                {message.sender === "user" ? "You" : "Meowy"}
              </CardTitle>
              <CardDescription>
                {message.sender === "user"
                  ? "User's message"
                  : "Assistant's response"}
              </CardDescription>
            </CardHeader>
            <CardContent>
              {message.isMeowy ? (
                <>
                  <LLMOutputRenderer
                    key={messageKey}
                    output={message.text || ""}
                    isStreamFinished={true} // Assuming stream is complete for simplicity
                  />
                  {/* Render Image Gallery if there are URLs */}
                  {message.showGallery && message.imageUrls && (
                    <div className="mt-4 flex items-center justify-center">
                      <ImageGallery imageUrls={message.imageUrls} />
                    </div>
                  )}
                </>
              ) : (
                <p>{message.text}</p>
              )}
            </CardContent>
          </Card>
        ))}
        <div ref={messagesEndRef} />
      </div>

      {/* Fixed Input Area */}
      <div className="fixed bottom-0 left-1/2 w-full max-w-lg -translate-x-1/2 transform bg-black p-4">
        <CardFooter className="flex space-x-2">
          <Input
            type="text"
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            placeholder="Type a message..."
            className="flex-1"
            onKeyDown={(e) => e.key === "Enter" && sendMessage()}
          />
          <Button onClick={sendMessage}>Send</Button>
        </CardFooter>
      </div>
    </div>
  );
};

export default Page;
