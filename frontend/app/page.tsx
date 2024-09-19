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
import { MeowyAlert } from "@/components/MeowyAlert";
import { Loading } from "@/components/Loading"; // Import Loading component

const Page = () => {
  const [messages, setMessages] = useState<
    {
      sender: string;
      text?: string;
      isMeowy?: boolean;
      showGallery?: boolean;
      imageUrls?: string[];
      isLoading?: boolean; // New flag to track if this specific message is loading
    }[]
  >([]);
  const [inputValue, setInputValue] = useState("");
  const [messageKey, setMessageKey] = useState(0);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Scroll to bottom when new messages are added
  const scrollToBottom = () => {
    if (messagesEndRef.current) {
      messagesEndRef.current.scrollIntoView({ behavior: "smooth" });
    }
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Handle sending the message
  const sendMessage = async () => {
    if (inputValue.trim()) {
      // Add user's message to the chat
      setMessages((prev) => [...prev, { sender: "user", text: inputValue }]);
      setInputValue("");

      // Add a loading message for Meowy
      setMessages((prev) => [
        ...prev,
        {
          sender: "meowy",
          text: "", // Empty for now until response is received
          isMeowy: true,
          isLoading: true, // Set loading to true for this message
        },
      ]);

      // Scroll to bottom after user input
      scrollToBottom();

      try {
        // Send request to backend
        const response = await fetch("http://localhost:8000/api/chat/", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ user_input: inputValue }),
          credentials: "include",
        });

        const data = await response.json();
        const showGallery = data.urls.length > 0;

        // Update the last message (Meowy's loading message) with the actual response
        setMessages((prev) => {
          const updatedMessages = [...prev];
          const lastMessage = updatedMessages[updatedMessages.length - 1];
          lastMessage.text = data.response;
          lastMessage.isLoading = false; // Set loading to false
          lastMessage.showGallery = showGallery;
          lastMessage.imageUrls = data.urls;
          return updatedMessages;
        });

        setMessageKey((prevKey) => prevKey + 1);
      } catch (error) {
        console.error("Error fetching Meowy's response:", error);
      }
    }
  };

  return (
    <div className="flex min-h-screen flex-col items-center bg-black p-4 text-white">
      {/* Show Meowy Alert if no messages */}
      {messages.length === 0 && (
        <div className="flex h-screen w-full max-w-lg flex-grow flex-col items-center justify-center space-y-4 shadow-lg">
          <MeowyAlert />
        </div>
      )}

      {/* Display messages if there are any */}
      {messages.length > 0 && (
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
                    {/* If loading, show loading skeleton */}
                    {message.isLoading ? (
                      <Loading />
                    ) : (
                      <LLMOutputRenderer
                        key={messageKey}
                        output={message.text || ""}
                        isStreamFinished={true}
                      />
                    )}

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
      )}

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
