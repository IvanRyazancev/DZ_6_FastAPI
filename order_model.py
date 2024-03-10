from pydantic import BaseModel


class Order(BaseModel):
    id: int
    user_id: int
    item_id: int
    order_date: str
    status: str
