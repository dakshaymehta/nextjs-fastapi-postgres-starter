import { NextResponse } from 'next/server';

type Message = {
  id: number;
  content: string;
  isUser: boolean;
  timestamp: string;
};

let messages: Message[] = [];

export async function GET() {
  return NextResponse.json(messages);
}

export async function POST(request: Request) {
  const { content, isUser } = await request.json();
  
  if (!content) {
    return NextResponse.json({ error: 'Content is required' }, { status: 400 });
  }

  const newMessage: Message = {
    id: Date.now(),
    content,
    isUser,
    timestamp: new Date().toISOString(),
  };

  messages.push(newMessage);
  return NextResponse.json(newMessage, { status: 201 });
}