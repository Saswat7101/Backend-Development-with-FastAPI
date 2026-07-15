from fastapi import FastAPI # type: ignore
from scalar_fastapi import get_scalar_api_reference # type: ignore
from typing import Any

app = FastAPI()

@app.get("/shipment")
def get_shipment():
    return {
        "content": "Wooden Table",
        "status": "In Transit"
    }

@app.get("/shipment/latest")
def get_latest_shipment() -> dict[str, Any]:
    return {
        "id": 12,
        "weight": 0.6,
        "content": "Glassware",
        "status": "Placed"
    }

@app.get("/shipment/{id}")
def get_shipment_by_id(id: int) -> dict[str, Any]:
    return {
        "id": id,
        "weight": 2.5,
        "content": "Wooden Table",
        "status": "In Transit"
    }

@app.get("/scalar", include_in_schema = False)
def get_scalar_docs():
    return get_scalar_api_reference(
        openapi_url = app.openapi_url,
        title = "Scalar API"
    )