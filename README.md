# FastAPI Backend

A starter Python backend project structured for building an API with [FastAPI](https://fastapi.tiangolo.com/).

## Project structure

```text
.
├── app/
│   ├── __init__.py
│   └── main.py       # FastAPI application entry point
├── .gitignore
└── README.md
```

## Setup

Create and activate a virtual environment:

```powershell
python -m venv env
.\env\Scripts\Activate.ps1
```

Install the application dependencies:

```powershell
pip install fastapi "uvicorn[standard]"
```

## Run the API

Once `app/main.py` defines an ASGI application named `app`, start the development server with:

```powershell
uvicorn app.main:app --reload
```

The API will be available at `http://127.0.0.1:8000`, with interactive documentation at:

- `http://127.0.0.1:8000/docs`
- `http://127.0.0.1:8000/redoc`
