from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base

# Create a base class for declarative models
Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    # Establish a one-to-many relationship with Message
    messages = relationship("Message", back_populates="user")

class Thread(Base):
    __tablename__ = "threads"

    id = Column(Integer, primary_key=True, index=True)
    # Establish a one-to-many relationship with Message
    messages = relationship("Message", back_populates="thread")

class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String)
    is_user = Column(Boolean, default=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    # Foreign keys to establish relationships
    user_id = Column(Integer, ForeignKey("users.id"))
    thread_id = Column(Integer, ForeignKey("threads.id"))
    # Establish many-to-one relationships with User and Thread
    user = relationship("User", back_populates="messages")
    thread = relationship("Thread", back_populates="messages")


    # This code defines the database models for a chat application using SQLAlchemy ORM.
    # It includes three main models:
    # 1. User: Represents application users.
    # 2. Thread: Represents conversation threads.
    # 3. Message: Represents individual messages within threads.
    # The models establish relationships between each other, allowing for efficient
    # querying and data management in a relational database structure.
    # This setup supports a multi-user chat system with threaded conversations.