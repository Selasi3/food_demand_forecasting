from pydantic import BaseModel


class Order(BaseModel):
    item_ordered: str
    quantity: int
    location: str
    time_of_order: str
    delivery_time: int

class Output(BaseModel):
    amount:int
