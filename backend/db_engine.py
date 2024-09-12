import os
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine
from dotenv import load_dotenv
from models import Base

# Load environment variables
load_dotenv()

# Get the DATABASE_URL from the environment variable
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set")

# Create synchronous engine
sync_engine = create_engine(DATABASE_URL)

def reset_database():
    # Drop all tables
    Base.metadata.drop_all(bind=sync_engine)
    print("All tables dropped.")
    
    # Create all tables
    Base.metadata.create_all(bind=sync_engine)
    print("Database tables created successfully")

# Create asynchronous engine
async_engine = create_async_engine(DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://"))

print(f"Database engines created for URL: {DATABASE_URL}")