from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException, status  # type: ignore
from scalar_fastapi import get_scalar_api_reference
from sqlmodel import Session  # type: ignore

from app.database.models import Shipment
from app.database.session import create_db_tables, get_session

from .schemas import ShipmentRead, ShipmentCreate, ShipmentUpdate
from .database import Database


@asynccontextmanager
async def lifespan_handler(app: FastAPI):
    create_db_tables()
    yield


app = FastAPI(lifespan=lifespan_handler)
db = Database()


# Read a shipment by id
@app.get("/shipment", response_model=ShipmentRead)
def get_shipment_by_id(id: int, session: Session = Depends(get_session)):
    shipment = session.get(Shipment, id)
    # Check for shipment with given id
    if shipment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Given ID: {id} does not exist",
        )
    return shipment


# Create a new shipment with content and weight
@app.post("/shipment", response_model=None)
def submit_shipment(
    shipment: ShipmentCreate, session: Session = Depends(get_session)
) -> dict[str, int]:
    new_id = db.create(shipment)
    # Return the response
    return {"id": new_id}


# Update fields of a shipment
@app.patch("/shipment", response_model=ShipmentRead)
def update_shipment(
    id: int, shipment: ShipmentUpdate, session: Session = Depends(get_session)
):
    # Update the provided fields
    shipment = db.update(id, shipment)
    return shipment


# Delete a shipment by id
@app.delete("/shipment")
def delete_shipment(id: int, session: Session = Depends(get_session)) -> dict[str, str]:
    db.delete(id)
    return {"detail": f"Shipment with #{id} id deleted!"}


@app.get("/scalar", include_in_schema=False)
def get_scalar_docs():
    return get_scalar_api_reference(openapi_url=app.openapi_url, title="Scalar API")
