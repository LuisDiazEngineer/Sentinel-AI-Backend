# Sentinel-AI 
**Automated Threat Logging & Classification System**

This is a professional Backend API built with **FastAPI** and **SQLAlchemy**. It monitors security threats and uses internal logic to classify severity automatically.

## Key Features
* **Automated Classification:** Analyzes threat descriptions to assign priority (Critical, Medium, Low).
* **Data Integrity:** Implements SQLAlchemy sessions with `rollback` for safe database transactions.
* **Input Validation:** Uses Pydantic models to ensure clean and secure data entry.

## Tech Stack
* Python 3.x
* FastAPI
* SQLAlchemy (SQLite)
* Pydantic

## Setup
1. Install dependencies:
   `pip install -r requirements.txt`
2. Run the server:
   `uvicorn main:app --reload`