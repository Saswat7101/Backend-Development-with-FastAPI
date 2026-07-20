# Shipment Tracking API

A FastAPI application for managing shipment records. It uses Pydantic models to validate request and response data. Data is stored in memory, so changes are lost when the server restarts.

## Features

- Retrieve a sample shipment, the latest shipment, a shipment by ID, or one field from a shipment.
- Create, partially update, and delete shipment records.
- Validate shipment content, weight, destination, and status with Pydantic schemas.
- Limit shipment weight to 25 kg.
- Browse the API using Swagger UI, ReDoc, or Scalar.

## Project structure

```text
.
|-- app/
|   |-- __init__.py
|   |-- main.py       # FastAPI application and shipment endpoints
|   `-- schemas.py    # Pydantic shipment models and status values
|-- .gitignore
`-- README.md
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

The API runs at `http://127.0.0.1:8000`.

## Endpoints

| Method | Path | Description |
| --- | --- | --- |
| `GET` | `/shipment` | Returns a sample shipment. |
| `GET` | `/shipment/latest` | Returns the shipment with the highest ID. |
| `GET` | `/shipment/{id}` | Returns a shipment by numeric ID. |
| `GET` | `/shipment/{field}?id={id}` | Returns one field (such as `content`, `weight`, or `status`) for a shipment. |
| `POST` | `/shipment` | Creates a new shipment from a JSON request body with the `Placed` status. |
| `PATCH` | `/shipment?id={id}` | Updates the shipment fields supplied in a JSON request body. |
| `DELETE` | `/shipment?id={id}` | Deletes a shipment. |

The initial shipment IDs are `12701` through `12707`.

### Create a shipment

Send `content`, `weight`, and `destination` in a JSON request body. `weight` must not exceed 25 kg.

```powershell
curl -X POST "http://127.0.0.1:8000/shipment" -H "Content-Type: application/json" -d '{"content":"Desk Lamp","weight":2.3,"destination":11001}'
```

Successful requests return the assigned ID:

```json
{
  "id": 12708
}
```

### Update a shipment

Use `PATCH` to update a shipment. The ID is a required query parameter; `status` is required in the JSON body, while `content`, `weight`, and `destination` are optional. Valid status values are `Placed`, `In Transit`, `Out For Delivery`, and `Delivered`.

```powershell
curl -X PATCH "http://127.0.0.1:8000/shipment?id=12701" -H "Content-Type: application/json" -d '{"status":"Delivered","destination":11002}'
```

### Delete a shipment

```powershell
curl -X DELETE "http://127.0.0.1:8000/shipment?id=12701"
```

The endpoint confirms the deleted shipment ID:

```json
{
  "detail": "Shipment with #12701 id deleted!"
}
```

### Error responses

- `GET /shipment/{id}` and field lookup requests for an unknown shipment ID return `404 Not Found`.
- A field lookup for an unknown field returns `404 Not Found`.
- Missing or invalid request data, including a weight above 25 kg, returns `422 Unprocessable Entity`.

For example:

```json
{
  "detail": "The searched ID does not exist"
}
```

## API documentation

- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`
- Scalar: `http://127.0.0.1:8000/scalar`
