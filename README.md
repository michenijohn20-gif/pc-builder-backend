# PC Builder Backend

Flask API for the PC Builder app. It manages user authentication, exposes component and build endpoints, and powers the data flow behind browsing parts, assembling builds, and saving changes from the frontend.

The project uses Flask, SQLAlchemy, and JWT authentication. A local SQLite database is configured by default.

## Installation

1. `cd pc-backend`
2. Create and activate a virtual environment.
3. `pip install -r requirements.txt`

## Run

1. `cd pc-backend`
2. `python main.py`

The API runs on `http://127.0.0.1:5000`.
