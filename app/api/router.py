from fastapi import APIRouter, HTTPException, status  # type: ignore

from app.api.schemas.shipment import ShipmentCreate, ShipmentRead, ShipmentUpdate
from app.database.models import Shipment
from app.database.session import SessionDep
from app.services.shipment import ShipmentService

router = APIRouter()


# Read a shipment by id
@router.get("/shipment", response_model=ShipmentRead)
async def get_shipment_by_id(id: int, session: SessionDep):
    shipment = ShipmentService(session).get(id)
    # Check for shipment with given id
    if shipment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Given ID: {id} does not exist",
        )
    return shipment


# Create a new shipment with content and weight
@router.post("/shipment")
async def submit_shipment(shipment: ShipmentCreate, session: SessionDep) -> Shipment:
    return await ShipmentService(session).add(shipment)


# Update fields of a shipment
@router.patch("/shipment", response_model=ShipmentRead)
async def update_shipment(
    id: int, shipment_update: ShipmentUpdate, session: SessionDep
):
    # Update the provided fields
    update = shipment_update.model_dump(exclude_none=True)

    if not update:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No data provided to update",
        )

    return await ShipmentService(session).update(shipment_update)


# Delete a shipment by id
@router.delete("/shipment")
async def delete_shipment(id: int, session: SessionDep) -> dict[str, str]:
    # Remove from database
    await ShipmentService(session).delete(id)

    return {"detail": f"Shipment with #{id} id deleted!"}
