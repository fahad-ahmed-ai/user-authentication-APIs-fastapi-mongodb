# FastAPI MongoDB User Authentication

This is a FastAPI project using MongoDB with MongoEngine for user authentication.

## Project Structure

The project is structured as follows:

- `app`
  - `auth`
    - `db.py`: Contains MongoDB database operations.
    - `handler.py`: JWT token handler.
    - `routes.py`: Defines authentication routes.
    - `schemas.py`: Pydantic schemas for authentication.
    - `utils.py`: Utility functions for sending emails.
    - `views.py`: Defines authentication views.
  - `chat`
    - `views.py`: Contains views for generating replies and managing connections.
  - `utilities`
    - `config.py`: Configuration file to manage environment variables.
    - `responses.py`: Helper functions for creating responses.
    - `socketio_instance.py`: SocketIO instance (not used in provided code).
  - `models.py`: MongoDB document models.
- `application.py`: Main file containing FastAPI application setup.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/fahad-ahmed-ai/user-authentication-APIs-fastapi-mongodb.git
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables:

   Create a `.env` file and fill in the required variables (refer to `config.py` for details).

4. Run the FastAPI application:

   ```bash
   uvicorn application:application --reload
   ```

## Endpoints

- **POST /auth/signup**: Register a new user.
- **POST /auth/login**: Log in with existing user credentials.
- **POST /auth/logout**: Log out the user.
- **POST /auth/send_otp**: Send OTP for resetting password.
- **POST /auth/verify_otp**: Verify OTP for password reset.
- **PUT /auth/change_password**: Change user password.
- **PUT /auth/reset_user_password**: Reset user password.
- **DELETE /auth/delete_user_account**: Delete user account.
- **GET /auth/verify_token**: Verify user token.

## Environment Variables

Ensure these environment variables are set:

- `MONGO_URL`: MongoDB connection URL.
- `DATABASE_NAME`: MongoDB database name.
- `SEND_GRID_API_KEY`: SendGrid API key for sending emails.
- `SEND_GRID_EMAIL`: Sender email address.
- `APP_SECRET_KEY`: Secret key for JWT token encoding.

## Dependencies

- `fastapi`: Web framework.
- `uvicorn`: ASGI server.
- `mongoengine`: ODM for MongoDB.
- `bcrypt`: Password hashing library.
- `python-dotenv`: For loading environment variables from `.env` file.
- `sendgrid`: Library for sending emails.
- `pydantic`: Data validation and settings management library.

## Usage

Make HTTP requests to the defined endpoints using appropriate methods (GET, POST, PUT, DELETE). For example:

- Register a new user:

  ```bash
  curl -X POST -H "Content-Type: application/json" -d '{"user_name": "example", "email": "example@example.com", "password": "password", "confirm_password": "password"}' http://localhost:8000/auth/signup
  ```

- Log in:

  ```bash
  curl -X POST -H "Content-Type: application/json" -d '{"email": "example@example.com", "password": "password"}' http://localhost:8000/auth/login
  ```

- Log out:

  ```bash
  curl -X POST http://localhost:8000/auth/logout
  ```

- Change password:

  ```bash
  curl -X PUT -H "Content-Type: application/json" -d '{"email": "example@example.com", "password": "new_password", "confirm_password": "new_password"}' http://localhost:8000/auth/change_password
  ```

- Delete user account:

  ```bash
  curl -X DELETE -H "Content-Type: application/json" -d '{"password": "password"}' http://localhost:8000/auth/delete_user_account
  ```

## Contributors

- [Fahad Ahmed](https://github.com/fahad-ahmed-ai)
