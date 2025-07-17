# Book Review API - Backend Technical Assessment

This project is a simple RESTful API service for managing books and their reviews, built as part of a technical assessment. It is built using Python and the Flask framework.

## Features

*   **RESTful API:** A clean, well-documented API for CRUD operations on books and reviews.
*   **OpenAPI/Swagger Docs:** Interactive API documentation automatically generated with Flask-RESTx.
*   **Database Persistence:** Uses SQLAlchemy ORM for database interactions, with migrations managed by Flask-Migrate.
*   **Caching Layer:** Integrated with Redis for performance optimization, featuring a read-through cache strategy.
*   **Robust Error Handling:** Gracefully handles cache failures, falling back to the database without crashing.

---

## Getting Started (Windows Guide)

### Prerequisites

*   Python 3.8+
*   Pip
*   Git
*   An active Redis server instance (required for the caching layer)

### Setup & Installation

1.  **Clone the repository:**
    Open Command Prompt (`cmd`) and run:
    ```cmd
    git clone https://github.com/summer0212/Book-Review-Project.git
    cd Book-Review-Project
    ```

2.  **Create and activate a virtual environment:**
    ```cmd
    python -m venv venv
    .\venv\Scripts\activate
    ```
    You will see `(venv)` appear at the beginning of your command prompt line.

3.  **Install the dependencies:**
    ```cmd
    pip install -r requirements.txt
    ```

4.  **Configure Environment Variables:**
    Create a `.env` file in the project root. This file will store your Redis connection URL. You can create it by running this command:
    ```cmd
    echo REDIS_URL=your_redis_connection_url_here > .env
    ```
    Now, open the new `.env` file with a text editor (like Notepad) and replace `your_redis_connection_url_here` with your actual Redis URL.

    *Example for a Redis server with a password:*
    `REDIS_URL=redis://:your_password@your_host:6379/0`

    *Example for a local Redis server without a password:*
    `REDIS_URL=redis://localhost:6379/0`

5.  **Initialize the Database:**
    Run the database migrations to create the necessary tables.
    ```cmd
    rem Set the Flask app environment variable for the current session
    set FLASK_APP=run.py

    rem Run the upgrade command
    flask db upgrade
    ```
    This will create a `dev.db` (SQLite) file in your project directory.

---

## Usage

1.  **Start the Flask Server:**
    (Ensure your `(venv)` is active and you have set the `FLASK_APP` variable as shown above).
    ```cmd
    flask run
    ```
    The application will be running

2.  **Access the API Documentation:**
    Open your web browser and navigate to the interactive Swagger UI:
    [**http://127.0.0.1:5000/api/doc**](http://127.0.0.1:5000/api/doc)

    From here, you can explore and execute all the available API endpoints.

