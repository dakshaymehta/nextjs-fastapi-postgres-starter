import { NextResponse } from 'next/server';

// Define the structure of a Message object
type Message = {
  id: number;
  content: string;
  isUser: boolean;
  timestamp: string;
};

// In-memory storage for messages (Note: This will reset on server restart)
let messages: Message[] = [];

// GET handler to retrieve all messages
export async function GET() {
  return NextResponse.json(messages);
}

// POST handler to create a new message
export async function POST(request: Request) {
  // Extract content and isUser from the request body
  const { content, isUser } = await request.json();
  
  // Validate that content is provided
  if (!content) {
    return NextResponse.json({ error: 'Content is required' }, { status: 400 });
  }

  // Create a new message object
  const newMessage: Message = {
    id: Date.now(), // Use current timestamp as a simple unique ID
    content,
    isUser,
    timestamp: new Date().toISOString(),
  };

  // Add the new message to our in-memory storage
  messages.push(newMessage);
  
  // Return the newly created message with a 201 status code
  return NextResponse.json(newMessage, { status: 201 });
}

// Hey Nick,
//
// This file implements a simple in-memory message storage system using Next.js API routes.
// It provides two main functionalities:
// 1. GET: Retrieves all stored messages
// 2. POST: Adds a new message to the storage
//
// Some of the Key points:
// - We're using in-memory storage (messages array), which means data won't persist between server restarts.
// - The Message type ensures consistent structure for our message objects.
