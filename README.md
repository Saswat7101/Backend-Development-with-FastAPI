# Shipment Tracking API

A FastAPI application for creating, retrieving, updating, and deleting shipment records. Records are persisted in a local SQLite database (`sqlite.db`).

## Features

- Create and retrieve shipments by numeric ID.
- Update a shipment's status.
- Delete shipments.
- Validate request and response data with Pydantic models.
- Browse the API through Swagger UI, ReDoc, or Scalar.

## Project structure

```text
.
|-- app/
|   |-- __init__.py
|   |-- database.py   # SQLite data-access layer
|   |-- main.py       # FastAPI application and routes
|   `-- schemas.py    # Pydantic shipment models and status values
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
| `GET` | `/shipment?id={id}` | Returns the shipment with the provided numeric ID. |
| `POST` | `/shipment` | Creates a shipment from a JSON request body. |
| `PATCH` | `/shipment?id={id}` | Updates a shipment's status from a JSON request body. |
| `DELETE` | `/shipment?id={id}` | Deletes the shipment with the provided ID. |

## Request examples

### Create a shipment

Send `content` and `weight` in the JSON body. The maximum permitted weight is 25 kg; new shipments receive the `Placed` status.

```powershell
curl -X POST "http://127.0.0.1:8000/shipment" -H "Content-Type: application/json" -d '{"content":"Desk Lamp","weight":2.3}'
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

### Update a shipment status

Send the new status in the JSON body. The available values are `Placed`, `In Transit`, `Out For Delivery`, and `Delivered`.

```powershell
curl -X PATCH "http://127.0.0.1:8000/shipment?id=12701" -H "Content-Type: application/json" -d '{"status":"Delivered"}'
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
