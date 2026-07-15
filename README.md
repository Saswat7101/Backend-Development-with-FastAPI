# Shipment Tracking API

A small FastAPI application for retrieving shipment information from an in-memory data store.

## Features

- Retrieve a sample shipment.
- Retrieve the most recently added shipment.
- Look up a shipment by its numeric ID.
- Browse the API with FastAPI's Swagger UI, ReDoc, or Scalar.

## Project structure

```text
.
├── app/
│   ├── __init__.py
│   └── main.py       # FastAPI application and shipment endpoints
├── .gitignore
└── README.md
```

## Setup

Create and activate a virtual environment:

```powershell
python -m venv env
.\env\Scripts\Activate.ps1
```

Install the dependencies:

```powershell
pip install fastapi "uvicorn[standard]" scalar-fastapi
```

## Run the API

Start the development server from the project root:

```powershell
uvicorn app.main:app --reload
```

The API will run at `http://127.0.0.1:8000`.

## Endpoints

| Method | Path | Description |
| --- | --- | --- |
| `GET` | `/shipment` | Returns a sample shipment. |
| `GET` | `/shipment/latest` | Returns the shipment with the highest ID. |
| `GET` | `/shipment/{id}` | Returns the shipment for the provided numeric ID. |

Available sample shipment IDs: `12701` through `12707`.

For an ID that is not present, the API returns:

```json
{
  "detail": "The searched ID does not exist"
}
```

## API documentation

- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`
- Scalar: `http://127.0.0.1:8000/scalar`
