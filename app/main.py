from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, status  # type: ignore
from scalar_fastapi import get_scalar_api_reference  # type: ignore

from .schemas import ShipmentRead, ShipmentCreate, ShipmentUpdate
from .database import Database


@asynccontextmanager
async def lifespan_handler(app: FastAPI):
    print("Server started...")
    yield
    print(".. Server Stopped!")


app = FastAPI(lifespan=lifespan_handler)
db = Database()


# Read a shipment by id
@app.get("/shipment", response_model=ShipmentRead)
def get_shipment_by_id(id: int):
    shipment = db.get(id)
    # Check for shipment with given id
    if shipment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Given ID: {id} does not exist",
        )
    return shipment


# Create a new shipment with content and weight
@app.post("/shipment", response_model=None)
def submit_shipment(shipment: ShipmentCreate) -> dict[str, int]:
    new_id = db.create(shipment)
    # Return the response
    return {"id": new_id}


# Update fields of a shipment
@app.patch("/shipment", response_model=ShipmentRead)
def update_shipment(id: int, shipment: ShipmentUpdate):
    # Update the provided fields
    shipment = db.update(id, shipment)
    return shipment


# Delete a shipment by id
@app.delete("/shipment")
def delete_shipment(id: int) -> dict[str, str]:
    db.delete(id)
    return {"detail": f"Shipment with #{id} id deleted!"}


@app.get("/scalar", include_in_schema=False)
def get_scalar_docs():
    return get_scalar_api_reference(openapi_url=app.openapi_url, title="Scalar API")
