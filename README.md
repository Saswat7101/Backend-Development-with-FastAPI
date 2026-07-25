# Shipment Tracking API

An asynchronous FastAPI application for creating, retrieving, updating, and deleting shipments. It uses PostgreSQL, SQLModel, and SQLAlchemy's async session support.

## Features

- Asynchronous shipment CRUD endpoints, organized with router and service layers.
- PostgreSQL persistence through `asyncpg`, SQLModel, and async SQLAlchemy sessions.
- Automatic table creation during application startup.
- Pydantic validation for shipment payloads.
- Automatic `placed` status and a UTC estimated delivery time three days after creation.
- Swagger UI, ReDoc, and Scalar API documentation.

## Project structure

```text
.
|-- app/
|   |-- api/
|   |   |-- schemas/
|   |   |   `-- shipment.py  # Request and response schemas
|   |   |-- dependencies.py  # FastAPI dependency injection
|   |   `-- router.py        # Shipment routes
|   |-- database/
|   |   |-- models.py        # SQLModel shipment entity and status enum
|   |   `-- session.py       # Async engine, sessions, and table setup
|   |-- services/
|   |   `-- shipment.py      # Shipment business and data-access logic
|   |-- config.py            # Environment-based PostgreSQL configuration
|   `-- main.py              # Application setup and lifespan handler
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
pip install fastapi "uvicorn[standard]" scalar-fastapi sqlmodel sqlalchemy asyncpg pydantic-settings
```

Create a `.env` file in the project root with your PostgreSQL connection settings:

```dotenv
POSTGRES_SERVER=localhost
POSTGRES_PORT=5432
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_password
POSTGRES_DB=shipments
```

Ensure PostgreSQL is running and that the configured database already exists. The application creates the `shipment` table on startup.

## Run the API

Start the development server from the project root:

```powershell
uvicorn app.main:app --reload
```

The API runs at `http://127.0.0.1:8000`.

## Endpoints

| Method | Path | Description |
| --- | --- | --- |
| `GET` | `/shipment/?id={id}` | Returns a shipment by numeric ID. |
| `POST` | `/shipment/` | Creates a shipment from a JSON request body. |
| `PATCH` | `/shipment/?id={id}` | Updates a shipment's status and/or estimated delivery. |
| `DELETE` | `/shipment/?id={id}` | Deletes a shipment by numeric ID. |

## Request examples

### Create a shipment

Send `content`, `weight`, and `destination` in the JSON body. `weight` must not exceed 25 kg. New shipments receive `placed` status and a UTC estimated delivery timestamp three days after creation.

```powershell
curl -X POST "http://127.0.0.1:8000/shipment/" -H "Content-Type: application/json" -d '{"content":"Desk Lamp","weight":2.3,"destination":11001}'
```

### Retrieve a shipment

```powershell
curl "http://127.0.0.1:8000/shipment/?id=1"
```

### Update a shipment

Provide one or both supported JSON fields. Valid status values are `placed`, `in_transit`, `out_for_delivery`, and `delivered`. `estimated_delivery` accepts an ISO 8601 date-time value.

```powershell
curl -X PATCH "http://127.0.0.1:8000/shipment/?id=1" -H "Content-Type: application/json" -d '{"status":"delivered","estimated_delivery":"2026-07-28T10:00:00Z"}'
```

An empty update body returns `400 Bad Request`.

### Delete a shipment

```powershell
curl -X DELETE "http://127.0.0.1:8000/shipment/?id=1"
```

Successful deletion returns:

```json
{
  "detail": "Shipment with id #1 is deleted!"
}
```

## Error responses

- A `GET /shipment/` request for an unknown ID returns `404 Not Found`.
- Missing or invalid request data, including a weight above 25 kg or an unsupported status, returns `422 Unprocessable Entity`.
- An empty `PATCH` request body returns `400 Bad Request`.

For example, an unknown shipment ID returns:

```json
{
  "detail": "Given id doesn't exist!"
}
```

## API documentation

- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`
- Scalar: `http://127.0.0.1:8000/scalar`
