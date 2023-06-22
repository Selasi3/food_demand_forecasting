from pydantic import BaseModel


class Order(BaseModel):
    item_ordered: str
    quantity: int
    location: str
    delivery_time: int
    month: int
    day: int
    

class Output(BaseModel):
    amount:int
