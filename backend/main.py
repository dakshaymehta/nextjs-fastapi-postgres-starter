from fastapi import FastAPI, HTTPException, Depends, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy.future import select
from pydantic import BaseModel
from typing import List
import random
from datetime import datetime

from db_engine import sync_engine, reset_database
from models import Message as DBMessage, User as DBUser, Thread as DBThread
from sqlalchemy.orm import sessionmaker

app = FastAPI()

# CORS middleware setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency
def get_db():
    db = sessionmaker(autocommit=False, autoflush=False, bind=sync_engine)()
    try:
        yield db
    finally:
        db.close()

class MessageCreate(BaseModel):
    content: str
    thread_id: int

class MessageResponse(BaseModel):
    id: int
    content: str
    is_user: bool
    timestamp: datetime
    user_id: int
    thread_id: int

@app.post("/messages", response_model=MessageResponse)
def create_message(message: MessageCreate, db: Session = Depends(get_db)):
    # Assume user with id=1 exists
    user = db.query(DBUser).filter(DBUser.id == 1).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    thread = db.query(DBThread).filter(DBThread.id == message.thread_id).first()
    if not thread:
        thread = DBThread()
        db.add(thread)
        db.commit()
        db.refresh(thread)

    db_message = DBMessage(content=message.content, is_user=True, user_id=user.id, thread_id=thread.id)
    db.add(db_message)
    db.commit()
    db.refresh(db_message)

    # Generate bot response
    bot_responses = [
        "That's interesting! Tell me more.",
        "I see. How does that make you feel?",
        "Can you elaborate on that?",
        "What do you think about that?",
        "Interesting perspective. Have you considered alternatives?",
    ]
    bot_message = DBMessage(content=random.choice(bot_responses), is_user=False, user_id=user.id, thread_id=thread.id)
    db.add(bot_message)
    db.commit()
    db.refresh(bot_message)

    return MessageResponse(
        id=db_message.id,
        content=db_message.content,
        is_user=db_message.is_user,
        timestamp=db_message.timestamp,
        user_id=db_message.user_id,
        thread_id=db_message.thread_id
    )

@app.get("/messages/{thread_id}", response_model=List[MessageResponse])
def read_messages(thread_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    messages = db.query(DBMessage).filter(DBMessage.thread_id == thread_id).offset(skip).limit(limit).all()
    return [
        MessageResponse(
            id=message.id,
            content=message.content,
            is_user=message.is_user,
            timestamp=message.timestamp,
            user_id=message.user_id,
            thread_id=message.thread_id
        ) for message in messages
    ]

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Message received: {data}")

def create_test_user(db: Session):
    user = db.query(DBUser).filter(DBUser.id == 1).first()
    if not user:
        user = DBUser(id=1, name="Test User")
        db.add(user)
        db.commit()
        db.refresh(user)
        print("Test user created")
    else:
        print("Test user already exists")

if __name__ == "__main__":
    reset_database()
    db = next(get_db())
    create_test_user(db)
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)