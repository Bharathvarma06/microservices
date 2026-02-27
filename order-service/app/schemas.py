from pydantic import BaseModel

class CartAdd(BaseModel):
    user_id: int
    product_id: int
    quantity: int

class OrderResponse(BaseModel):
    id: int
    total_amount: float
    status: str

    class Config:
        orm_mode = True
