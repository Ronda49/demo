from typing import List, Optional

from fastapi import FastAPI, HTTPException

from pydantic import BaseModel

app = FastAPI(title="Simple Backend API")

# Fake in-memory database
fake_db: List[dict] = []


# Pydantic model
class Item(BaseModel):
    id: int
    name: str
    description: Optional[str] = None


# Root endpoint
@app.get("/")
def root():
    return {"message": "Welcome to Simple Backend API"}


# Health check endpoint
@app.get("/health")
def health_check():
    return {"status": "ok"}


# CRUD Endpoints
@app.get("/items", response_model=List[Item])
def get_items():
    return fake_db


@app.get("/items/{item_id}", response_model=Item)
def get_item(item_id: int):
    for item in fake_db:
        if item["id"] == item_id:
            return item
    raise HTTPException(status_code=404, detail="Item not found")


@app.post("/items", response_model=Item)
def create_item(item: Item):
    fake_db.append(item.dict())
    return item


@app.put("/items/{item_id}", response_model=Item)
def update_item(item_id: int, updated_item: Item):
    for i, item in enumerate(fake_db):
        if item["id"] == item_id:
            fake_db[i] = updated_item.dict()
            return updated_item
    raise HTTPException(status_code=404, detail="Item not found")


@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    for i, item in enumerate(fake_db):
        if item["id"] == item_id:
            del fake_db[i]
            return {"detail": "Item deleted"}
    raise HTTPException(status_code=404, detail="Item not found")
