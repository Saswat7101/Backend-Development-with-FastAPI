# Shipment Tracking API

A FastAPI application for creating, retrieving, updating, and deleting shipment records. It persists records to a local SQLite database (`sqlite.db`) through SQLModel sessions and creates its tables when the application starts.

## Features

- Create and retrieve shipments by numeric ID.
- Update a shipment's status or estimated delivery time.
- Delete shipments.
- Store shipment destinations and automatically assign an estimated delivery three days after creation.
- Validate API data with Pydantic schemas and define shipment entities with SQLModel.
- Browse the API through Swagger UI, ReDoc, or Scalar.

## Project structure

```text
.
|-- app/
|   |-- __init__.py
|   |-- database.py   # Earlier SQLite helper
|   |-- database/
|   |   |-- __init__.py
|   |   |-- models.py # SQLModel shipment entity and status enum
|   |   `-- session.py # SQLModel engine, sessions, and table setup
|   |-- main.py       # FastAPI application and routes
|   `-- schemas.py    # Pydantic request and response schemas
|-- sqlite.db         # SQLite database
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
pip install fastapi "uvicorn[standard]" scalar-fastapi sqlmodel
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
| `GET` | `/shipment?id={id}` | Returns the shipment with the provided numeric ID. |
| `POST` | `/shipment` | Creates a shipment from a JSON request body. |
| `PATCH` | `/shipment?id={id}` | Updates a shipment's status and/or estimated delivery from a JSON request body. |
| `DELETE` | `/shipment?id={id}` | Deletes the shipment with the provided ID. |

## Request examples

### Create a shipment

Send `content`, `weight`, and `destination` in the JSON body. The maximum permitted weight is 25 kg. New shipments receive the `Placed` status and an estimated delivery timestamp three days after creation.

```powershell
curl -X POST "http://127.0.0.1:8000/shipment" -H "Content-Type: application/json" -d '{"content":"Desk Lamp","weight":2.3,"destination":11001}'
```

The endpoint returns the database ID assigned to the new shipment:

```json
{
  "id": 12708
}
```

### Retrieve a shipment

```powershell
curl "http://127.0.0.1:8000/shipment?id=12701"
```

### Update a shipment

Send either or both supported fields in the JSON body. `status` accepts `Placed`, `In Transit`, `Out For Delivery`, or `Delivered`; `estimated_delivery` accepts an ISO 8601 date-time value. An empty body returns `400 Bad Request`.

```powershell
curl -X PATCH "http://127.0.0.1:8000/shipment?id=12701" -H "Content-Type: application/json" -d '{"status":"Delivered","estimated_delivery":"2026-07-26T10:00:00"}'
```

### Delete a shipment

```powershell
curl -X DELETE "http://127.0.0.1:8000/shipment?id=12701"
```

Successful deletion returns:

```json
{
  "detail": "Shipment with #12701 id deleted!"
}
```

## Error responses

- A `GET /shipment` request for an unknown ID returns `404 Not Found`.
- Missing or invalid request data, including a weight above 25 kg or an unsupported status, returns `422 Unprocessable Entity`.
- An empty `PATCH` request body returns `400 Bad Request`.

For example, an unknown shipment ID returns:

```json
{
  "detail": "Given ID: 99999 does not exist"
}
```

## API documentation

- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`
- Scalar: `http://127.0.0.1:8000/scalar`
