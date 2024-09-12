## Running the Application

## Required Software

1. Python
2. Node.js
3. Docker and Docker Compose
4. [Poetry](https://python-poetry.org/docs/#installation)
5. Postgres libpq header files (e.g. `apt install libpq-dev` on Ubuntu, `brew install postgresql` on macOS)

### First-Time Setup

1. `cd` into `backend` and run `poetry install`.
2. `cd` into `frontend` and run `npm install`.

### Running the Application

1. From the root directory, run `docker compose up`.
2. In a separate terminal, `cd` into `backend` and run `poetry run uvicorn main:app --reload`.
3. In a separate terminal, `cd` into `frontend` and run `npm run dev`.


## Notes

## Application Description

This application is an AI-powered chat interface that allows users to interact with an AI assistant. It's designed to showcase a modern web application architecture with a focus on real-time communication.

### Key Features:
- Real-time chat functionality
- User-friendly interface

### Implementation Details:
- Frontend: Next.js with TypeScript, utilizing React for the UI components
- Backend: FastAPI (Python) for handling API requests and WebSocket connections
- Database: PostgreSQL for data persistence
- State Management: In-memory storage for messages (with plans to integrate database storage)
- Styling: Tailwind CSS for responsive design

The application demonstrates the integration of a React-based frontend with a Python backend, showcasing how to build a full-stack application with modern web technologies.

