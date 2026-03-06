# Printing Shop Order Management System

A FastAPI-based backend system for managing printing shop orders on campus. This system automates order processing, pricing calculation, and payment handling to reduce errors during rush hours.

## Features

- Create and manage printing orders
- Automatic pricing calculation (B&W: ₱2/page, Colored: ₱5/page, Photo Paper: ₱20/page)
- Payment processing with change calculation
- Order status tracking (Pending, Paid, Completed)
- RESTful API endpoints
- SQLite database persistence via SQLAlchemy
- Simple HTML/CSS/JavaScript frontend served from `/`

## Prerequisites

- Python 3.8 or higher
- Windows 10 or above (as per requirements)

## Installation and Setup

### 1. Navigate to the Project Directory

Open PowerShell and navigate to the project folder:

```powershell
cd "C:\Users\Admin\Documents\SCHOOL FILES\SY 25-26 BSIT 3rdYear 2ndSem\AppDev\Printing Shop System for Campus"
```

### 2. Create Virtual Environment (if not already created)

If the `.venv` folder doesn't exist, create a virtual environment:

```powershell
python -m venv .venv
```

### 3. Activate Virtual Environment

Activate the virtual environment:

```powershell
.\.venv\Scripts\Activate.ps1
```

You should see `(.venv)` at the beginning of your PowerShell prompt.

### 4. Install Dependencies

Install the required Python packages:

```powershell
pip install -r requirements.txt
```

This will install:
- FastAPI: Web framework
- Uvicorn: ASGI server
- Pydantic: Data validation
- SQLAlchemy: Object-relational mapper for database management

### 5. Run the Application

Start the FastAPI server with auto-reload for development:

```powershell
uvicorn main:app --reload
```

The server will start on `http://localhost:8000`

### 6. Access the API

- **API Documentation**: Visit `http://localhost:8000/docs` for interactive Swagger UI
- **Alternative Docs**: Visit `http://localhost:8000/redoc` for ReDoc documentation
- **Root Endpoint**: `http://localhost:8000/` returns a welcome message

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/orders` | Create a new printing order |
| GET | `/orders` | Get all orders |
| GET | `/orders/{id}` | Get specific order by ID |
| PUT | `/orders/{id}` | Update order details |
| POST | `/orders/{id}/pay` | Process payment for an order |
| DELETE | `/orders/{id}` | Delete an order |

## Frontend

A basic single‑page UI is provided under the `static/` folder and served at the root (`http://localhost:8000/`).

It allows you to create orders, view the list, process payments and delete orders without using curl or Postman. The JavaScript code uses the same REST API endpoints described below.

## Testing the API

### Create an Order (POST /orders)

```powershell
Invoke-WebRequest -Uri "http://localhost:8000/orders" -Method POST -ContentType "application/json" -Body '{"student_name": "John Doe", "document_name": "Thesis.pdf", "pages": 10, "print_type": "Colored"}'
```

### Get All Orders (GET /orders)

```powershell
Invoke-WebRequest -Uri "http://localhost:8000/orders" -Method GET
```

### Process Payment (POST /orders/{id}/pay)

```powershell
Invoke-WebRequest -Uri "http://localhost:8000/orders/1/pay" -Method POST -ContentType "application/json" -Body '{"amount": 50.0}'
```

## Data Persistence

Orders are stored in an SQLite database file `printing_shop.db` located at the project root. The database is managed through SQLAlchemy and tables are created automatically when the application starts. You can inspect the file with any SQLite viewer if needed.

## Project Structure

```
printing-shop-system/
├── main.py                 # FastAPI application entry point
├── models.py               # SQLAlchemy models + Pydantic schemas
├── database.py             # Database configuration (SQLite + SQLAlchemy)
├── requirements.txt        # Python dependencies
├── routes/
│   └── orders.py           # Order management endpoints using DB
├── printing_shop.db        # SQLite database file (auto-generated)
├── static/                 # Frontend assets
│   ├── index.html
│   ├── style.css
│   └── script.js
└── README.md               # This file
```

## Development

To stop the server, press `Ctrl+C` in the terminal.

To deactivate the virtual environment:

```powershell
deactivate
```

## Troubleshooting

- **Port already in use**: Change the port with `uvicorn main:app --reload --port 8001`
- **Permission errors**: Run PowerShell as Administrator
- **Import errors**: Ensure virtual environment is activated and dependencies are installed

## Requirements Compliance

- ✅ Handles whole day workload (lightweight FastAPI application)
- ✅ Works on Windows 10 and above
- ✅ Automates order acceptance and processing
- ✅ Calculates pricing and change accurately
- ✅ Provides order management functionality