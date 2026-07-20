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

class BaseShipment(BaseModel):
    content:str
    weight: float = Field(le = 25)
    destination: int

class ShipmentRead(BaseShipment):
    status: ShipmentStatus

class ShipmentCreate(BaseShipment):
    pass

class ShipmentUpdate(BaseModel):
    status: ShipmentStatus