from random import randint
from enum import Enum
from pydantic import BaseModel, Field

def random_destination():
    return randint(11000, 11999)

class ShipmentStatus(str, Enum):
    placed = "Placed"
    in_transit = "In Transit"
    out_for_delivery = "Out For Delivery"
    delivered = "Delivered"

class Shipment(BaseModel):
    content:str = Field(max_length = 30)
    weight: float = Field(description = "Weight of the shipment in kilograms(kg)", le = 25, ge = 1)
    destination: int | None = Field(default_factory = random_destination)
    status: ShipmentStatus