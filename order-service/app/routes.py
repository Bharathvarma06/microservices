from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import requests

from app.database import SessionLocal
from app import models, schemas
from app.config import PRODUCT_SERVICE_URL

router = APIRouter(prefix="/order", tags=["Orders"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 🛒 Add to cart
@router.post("/cart")
def add_to_cart(data: schemas.CartAdd, db: Session = Depends(get_db)):
    cart_item = models.Cart(**data.dict())
    db.add(cart_item)
    db.commit()
    return {"msg": "Added to cart"}

# 📦 Create order
@router.post("/create", response_model=schemas.OrderResponse)
def create_order(user_id: int, db: Session = Depends(get_db)):
    cart_items = db.query(models.Cart).filter(
        models.Cart.user_id == user_id
    ).all()

    if not cart_items:
        raise HTTPException(status_code=400, detail="Cart is empty")

    total = 0
    order = models.Order(user_id=user_id, total_amount=0)
    db.add(order)
    db.commit()
    db.refresh(order)

    for item in cart_items:
        # Call Product Service
        res = requests.get(
            f"{PRODUCT_SERVICE_URL}/products/{item.product_id}"
        )
        if res.status_code != 200:
            raise HTTPException(status_code=400, detail="Invalid product")

        product = res.json()
        price = product["price"]
        total += price * item.quantity

        order_item = models.OrderItem(
            order_id=order.id,
            product_id=item.product_id,
            quantity=item.quantity,
            price=price
        )
        db.add(order_item)
        db.delete(item)

    order.total_amount = total
    db.commit()
    db.refresh(order)

    return order
