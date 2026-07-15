from fastapi import FastAPI # type: ignore
from scalar_fastapi import get_scalar_api_reference # type: ignore
from typing import Any

app = FastAPI()

shipments = {
    12701: {
        "weight": 2.5,
        "content": "Wooden Table",
        "status": "In Transit"
    },
    12702: {
        "weight": 0.8,
        "content": "Ceramic Mugs",
        "status": "Placed"
    },
    12703: {
        "weight": 14.2,
        "content": "Office Chair",
        "status": "Out for Delivery"
    },
    12704: {
        "weight": 1.1,
        "content": "Wireless Headphones",
        "status": "Delivered"
    },
    12705: {
        "weight": 6.7,
        "content": "Kitchen Blender",
        "status": "Processing"
    },
    12706: {
        "weight": 3.4,
        "content": "Cotton Bed Sheets",
        "status": "In Transit"
    },
    12707: {
        "weight": 9.5,
        "content": "Floor Lamp",
        "status": "Delayed"
    }
}

@app.get("/shipment")
def get_shipment():
    return {
        "content": "Wooden Table",
        "status": "In Transit"
    }

@app.get("/shipment/latest")
def get_latest_shipment() -> dict[str, Any]:
    id = max(shipments.keys())
    return shipments[id]

@app.get("/shipment/{id}")
def get_shipment_by_id(id: int) -> dict[str, Any]:
    if  id not in shipments:
        return {"detail": "The searched ID does not exist"}
    return shipments[id]

@app.get("/scalar", include_in_schema = False)
def get_scalar_docs():
    return get_scalar_api_reference(
        openapi_url = app.openapi_url,
        title = "Scalar API"
    )
