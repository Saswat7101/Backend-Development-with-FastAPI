# Shipment Tracking API

A FastAPI application for retrieving and creating shipment records. Data is stored in memory, so shipments created while the server is running are lost when it restarts.

## Features

- Retrieve a sample shipment, the latest shipment, a shipment by ID, or one field from a shipment.
- Create, fully update, partially update, and delete shipment records.
- Limit newly created shipments to a maximum weight of 25 kg.
- Browse the API using Swagger UI, ReDoc, or Scalar.

## Project structure

```text
.
|-- app/
|   |-- __init__.py
|   `-- main.py       # FastAPI application and shipment endpoints
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
| `POST` | `/shipment?content={content}&weight={weight}` | Creates a new shipment with the `Placed` status. |
| `PUT` | `/shipment?id={id}&content={content}&weight={weight}&status={status}` | Replaces every field of a shipment. |
| `PATCH` | `/shipment?id={id}` | Updates the shipment fields supplied in a JSON request body. |
| `DELETE` | `/shipment?id={id}` | Deletes a shipment. |

The initial shipment IDs are `12701` through `12707`.

### Create a shipment

`content` and `weight` are required query parameters. The weight must not exceed 25 kg.

```powershell
curl -X POST "http://127.0.0.1:8000/shipment?content=Desk%20Lamp&weight=2.3"
```

Successful requests return the assigned ID:

```json
{
  "id": 12708
}
```

### Update a shipment

Use `PUT` to replace all fields. Its `id`, `content`, `weight`, and `status` are required query parameters:

```powershell
curl -X PUT "http://127.0.0.1:8000/shipment?id=12701&content=Wooden%20Desk&weight=12.5&status=Processing"
```

Use `PATCH` to update only the fields included in its JSON body:

```powershell
curl -X PATCH "http://127.0.0.1:8000/shipment?id=12701" -H "Content-Type: application/json" -d '{"status":"Delivered"}'
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
- A new shipment weighing more than 25 kg returns `406 Not Acceptable`.

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
