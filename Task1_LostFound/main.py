from fastapi import FastAPI, HTTPException
from sqlmodel import Session, select

from .database import engine, create_tables
from .models import Item, ItemStatus
from .schemas import ItemCreate


app = FastAPI(title="Campus Lost & Found API")


@app.on_event("startup")
def startup():
    create_tables()


@app.post("/items")
def create_item(item_data: ItemCreate):
    item = Item(**item_data.model_dump())

    with Session(engine) as session:
        session.add(item)
        session.commit()
        session.refresh(item)
        return item


@app.get("/items")
def get_items():
    with Session(engine) as session:
        items = session.exec(select(Item)).all()
        return items


@app.get("/items/{item_id}")
def get_item(item_id: int):
    with Session(engine) as session:
        item = session.get(Item, item_id)

        if not item:
            raise HTTPException(
                status_code=404,
                detail="Item not found"
            )

        return item


@app.put("/items/{item_id}")
def update_item(item_id: int, item_data: ItemCreate):
    with Session(engine) as session:
        item = session.get(Item, item_id)

        if not item:
            raise HTTPException(
                status_code=404,
                detail="Item not found"
            )

        updated_data = item_data.model_dump()

        for key, value in updated_data.items():
            setattr(item, key, value)

        session.add(item)
        session.commit()
        session.refresh(item)

        return item


@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    with Session(engine) as session:
        item = session.get(Item, item_id)

        if not item:
            raise HTTPException(
                status_code=404,
                detail="Item not found"
            )

        session.delete(item)
        session.commit()

        return {"message": "Item deleted successfully"}


@app.get("/items/status/{status}")
def get_items_by_status(status: ItemStatus):
    with Session(engine) as session:
        items = session.exec(
            select(Item).where(Item.status == status)
        ).all()

        return items


@app.get("/items/category/{category}")
def get_items_by_category(category: str):
    with Session(engine) as session:
        items = session.exec(
            select(Item).where(Item.category == category)
        ).all()

        return items