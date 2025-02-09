# FastAPI Blog Project

This is a FastAPI project for managing blogs and users. The project includes user authentication, blog creation, and management features.

## Features

- User registration and authentication
- Blog creation, update, and deletion
- User profile management
- JWT-based authentication

## Requirements

- Python 3.10+
- FastAPI
- SQLAlchemy
- bcrypt
- email-validator
- python-dotenv
- uvicorn

## Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/tinyfroggy/full-stake-blogs/tree/main
   cd backend
   ```

## Running the Project Locally

1. Create and activate a virtual environment:
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

2. Install the required dependencies:
   ```sh
   pip install -r requirements.txt
   ```

3. Set up the environment variables by creating a `.env` file in the project root directory and adding the necessary configurations:
   ```env
   DATABASE_URL=sqlite:///./test.db
   SECRET_KEY=your_secret_key
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   ```

4. Run the database migrations:
   ```sh
   alembic upgrade head
   ```

5. Start the FastAPI server:
   ```sh
   uvicorn main:app --reload
   ```

6. Open your browser and navigate to `http://127.0.0.1:8000/docs` to access the API documentation.