from fastapi import FastAPI, HTTPException
from user_model import User
from order_model import Order
from item_model import Item
from typing import List
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import uvicorn

app = FastAPI()

SQLALCHEMY_DATABASE_URL = "sqlite:///./database.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)


class OrderModel(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    item_id = Column(Integer, ForeignKey('items.id'))
    order_date = Column(DateTime, default=datetime.utcnow)
    status = Column(String)


class ItemModel(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    price = Column(Float)


Base.metadata.create_all(bind=engine)


@app.post("/users/", response_model=User)
async def create_user(user: User):
    db = SessionLocal()
    user_db = UserModel(
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        password=user.password
    )
    db.add(user_db)
    db.commit()
    db.refresh(user_db)
    return user_db

@app.post("/orders/", response_model=Order)
async def create_order(order: Order):
    db = SessionLocal()
    order_db = OrderModel(
        user_id=order.user_id,
        item_id=order.item_id,
        status=order.status
    )
    db.add(order_db)
    db.commit()
    db.refresh(order_db)
    return order_db

@app.post("/items/", response_model=Item)
async def create_item(item: Item):
    db = SessionLocal()
    item_db = ItemModel(
        name=item.name,
        description=item.description,
        price=item.price
    )
    db.add(item_db)
    db.commit()
    db.refresh(item_db)
    return item_db

@app.get("/users/", response_model=List[User])
async def read_users():
    db = SessionLocal()
    users = db.query(UserModel).all()
    return users

@app.get("/orders/", response_model=List[Order])
async def read_orders():
    db = SessionLocal()
    orders = db.query(OrderModel).all()
    return orders

@app.get("/items/", response_model=List[Item])
async def read_items():
    db = SessionLocal()
    items = db.query(ItemModel).all()
    return items


if __name__ == "__main__":
    uvicorn.run(app, port=8000)