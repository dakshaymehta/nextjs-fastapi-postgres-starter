import os
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine
from dotenv import load_dotenv
from models import Base

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set")

# Create synchronous engine
sync_engine = create_engine(DATABASE_URL)


def reset_database():
    Base.metadata.drop_all(bind=sync_engine)
    print("All tables dropped.")

    Base.metadata.create_all(bind=sync_engine)
    print("Database tables created successfully")


# Hey Nick:
# The reasons for creating an asynchronous engine are:
# 1. Improved performance: Async operations can handle more concurrent requests efficiently.
# 2. Non-blocking I/O: Allows the application to perform other tasks while waiting for database operations.
# 3. Scalability: Better suited for high-concurrency scenarios in web applications.
# 4. Compatibility: Some FastAPI features work best with async database operations.
async_engine = create_async_engine(DATABASE_URL.replace(
    "postgresql://", "postgresql+asyncpg://"))

print(f"Database engines created for URL: {DATABASE_URL}")


# Note: replace 'postgresql://' with 'postgresql+asyncpg://' to use the asyncpg driver for async operations.
