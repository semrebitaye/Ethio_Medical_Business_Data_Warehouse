## Task 4 - Expose the Collected Data Using FastAPI
### Objective

Expose object detection data stored in a PostgreSQL database through a FastAPI-based API for easy access and integration.
### Setting Up the Environment

Install FastAPI and Uvicorn:

### Project Structure

my_project/ ├── main.py ├── database.py ├── models.py ├── schemas.py └── crud.py
### Database Configuration

Configure the database connection using SQLAlchemy in database.py.
### Creating Data Models

Define SQLAlchemy models for the database tables in models.py.
### Creating Pydantic Schemas

Define Pydantic schemas for data validation and serialization in schemas.py.
### CRUD Operations

Implement CRUD (Create, Read, Update, Delete) operations for the database in crud.py.
### Creating API Endpoints

Define the API endpoints using FastAPI in main.py.
### Running the Application

To run the FastAPI application, use Uvicorn:

uvicorn main:app --reload

The application will be available at http://127.0.0.1:8000 with API documentation at http://127.0.0.1:8000/docs.