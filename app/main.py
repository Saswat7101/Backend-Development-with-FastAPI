from enum import Enum

from fastapi import FastAPI, HTTPException, status # type: ignore
from scalar_fastapi import get_scalar_api_reference # type: ignore
from typing import Any

from app.schemas import Shipment

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

@app.get("/shipment/{id:int}")
def get_shipment_by_id(id: int) -> dict[str, Any]:
    if id not in shipments:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The searched ID does not exist"
        )
    return shipments[id]

@app.post("/shipment")
def submit_shipment(shipment: Shipment) -> dict[str, Any]:
    # Create and assignshipment a new id
    new_id = max(shipments.keys()) + 1
    shipments[new_id] = {
        "content": shipment.content,
        "weight": shipment.weight,
        "status": "Placed"
    }
    # Return the response
    return {"id": new_id}

@app.get("/shipment/{field}")
def get_shipment_field(field: str, id: int) ->  Any:
    if id not in shipments:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The searched ID does not exist"
        )

    if field not in shipments[id]:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The field '{field}' does not exist"
        )

    return shipments[id][field]

class ShipmentStatus(str, Enum):
    placed = "Placed"
    in_transit = "In Transit"
    out_for_delivery = "Out For Delivery"
    delivered = "Delivered"

@app.patch("/shipment")
def update_shipment(id: int, body: dict[str, ShipmentStatus]) -> dict[str, Any]:
    # Update the provided fields
    shipments[id].update(body)
    return shipments[id]

@app.delete("/shipment")
def delete_shipment(id: int) -> dict[str, str]:
    shipments.pop(id)
    return {"detail": f"Shipment with #{id} id deleted!"}

@app.get("/scalar", include_in_schema = False)
def get_scalar_docs():
    return get_scalar_api_reference(
        openapi_url = app.openapi_url,
        title = "Scalar API"
    )
