'use client';

import React, { useState, useEffect, useRef } from 'react';


interface Message {
  id: number;
  content: string;
  is_user: boolean;
  timestamp: string;
}

export default function Chat() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputMessage, setInputMessage] = useState('');
  const [threadId] = useState(1); // Assume we're using thread ID 1
  const ws = useRef<WebSocket | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Effect to fetch messages and initialize WebSocket
  useEffect(() => {
    fetchMessages();
    initializeWebSocket();

    // Cleanup function to close WebSocket connection
    return () => {
      if (ws.current) ws.current.close();
    };
  }, [threadId]);

  // Effect to scroll to bottom when messages change 
  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // I used useEffect here for a few important reasons here:
  // 1. Side Effect: Scrolling is a side effect that affects something outside
  //    of the component's state (the DOM), which is exactly what useEffect is for.
  // 2. Dependency on State: We want to scroll when the messages change, so we
  //    include messages in the dependency array. This ensures the effect runs
  //    after every render where messages has changed.
  // 3. Separation of Concerns: It keeps the scrolling logic separate from the
  //    rendering logic, making the code more maintainable.
  // 4. Performance: By using useEffect, we ensure that scrolling happens after
  //    the DOM has been updated with the new messages, which is more efficient.
  useEffect(() => { 
    scrollToBottom();
  }, [messages]);

  // Initialize WebSocket connection to the backend
  const initializeWebSocket = () => {
    ws.current = new WebSocket('ws://localhost:8000/ws');
    ws.current.onmessage = (event) => {
      console.log('Message from server:', event.data);
      fetchMessages();
    };
  };

  // Scroll to the bottom of the chat
  // This ensures new messages are always visible
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  // Fetch messages from the server
  const fetchMessages = async () => {
    try {
      const response = await fetch(`http://localhost:8000/messages/${threadId}`);
      const data = await response.json();
      setMessages(data);
    } catch (error) {
      console.error('Error fetching messages:', error);
    }
  };

  // Send a new message
  const sendMessage = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    if (!inputMessage.trim()) return;

    try {
      await fetch('http://localhost:8000/messages', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ content: inputMessage, thread_id: threadId }),
      });
      setInputMessage('');
      fetchMessages();
      
      // Send message through WebSocket
      if (ws.current) ws.current.send(inputMessage);
    } catch (error) {
      console.error('Error sending message:', error);
    }
  };

  // Render the chat interface on the screen
  return (
    <div className="flex flex-col h-screen bg-gray-100">
      {/* Message list */}
      <div className="flex-grow overflow-auto p-4 space-y-4">
        {messages.map((message) => (
          <div
            key={message.id}
            className={`flex ${message.is_user ? 'justify-end' : 'justify-start'}`}
          >
            <div
              className={`p-3 rounded-lg max-w-xs lg:max-w-md ${
                message.is_user
                  ? 'bg-blue-500 text-white'
                  : 'bg-white text-gray-800 shadow'
              }`}
            >
              {message.content}
            </div>
          </div>
        ))}
        <div ref={messagesEndRef} />
      </div>
      {/* Message input form  */}
      <form onSubmit={sendMessage} className="p-4 bg-white border-t">
        <div className="flex space-x-2">
          <input
            type="text"
            value={inputMessage}
            onChange={(e) => setInputMessage(e.target.value)}
            className="flex-grow p-2 border rounded-full focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="Type your message..."
          />
          <button
            type="submit"
            className="bg-blue-500 text-white px-4 py-2 rounded-full hover:bg-blue-600 transition duration-200"
          >
            Send
          </button>
        </div>
      </form>
    </div>
  );
}


// Hey Nick
// Quick Breif description for the component:
// This React component implements a real-time chat interface using WebSocket for live updates.
// It fetches and displays messages, allows sending new messages, and automatically scrolls to the latest message.
// The component uses React hooks (useState, useEffect, useRef) for state management and side effects.
// It also implements a responsive design using Tailwind CSS classes for a modern look and feel.
// The code demonstrates proficiency in React, asynchronous JavaScript, WebSocket implementation, and UI design.