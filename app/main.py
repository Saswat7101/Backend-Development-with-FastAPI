from fastapi import FastAPI, HTTPException, status # type: ignore
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

@app.get("/shipment/{id:int}")
def get_shipment_by_id(id: int) -> dict[str, Any]:
    if id not in shipments:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The searched ID does not exist"
        )
    return shipments[id]

@app.post("/shipment")
def submit_shipment(content: str, weight: float) -> dict[str, Any]:
    # Validate weight:
    if weight > 25:
        raise HTTPException(
            status_code = status.HTTP_406_NOT_ACCEPTABLE,
            detail = "Maximum weight limit is 25kg"
        )
    # Create and assignshipment a new id
    new_id = max(shipments.keys()) + 1
    shipments[new_id] = {
        "content": content,
        "weight": weight,
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

@app.put("/shipment")
def shipment_update(id: int, content: str, weight: float, status: str) -> dict[str, Any]:
    #Update the shipment data with new data
    shipments[id] = {
        "content": content,
        "weight": weight,
        "status": status
    }
    return shipments[id]

@app.get("/scalar", include_in_schema = False)
def get_scalar_docs():
    return get_scalar_api_reference(
        openapi_url = app.openapi_url,
        title = "Scalar API"
    )
