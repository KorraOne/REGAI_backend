# REGAI Prototype Backend

## Setup

```bash
python -m venv .venv
.venv\Scripts\Activate.ps1   # Windows
pip install -r requirements.txt
```

## Start Server

```bash
uvicorn app.main:app --reload
```

Server runs at:
http://127.0.0.1:8000

## Endpoint Documentation

- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

Swagger is good for browsing the endpoint structure.
ReDoc is good for testing since it has built‑in request buttons.

## Database

There is no real database yet, everything is stored in variables in memory. So data resets whenever you restart the backend server.