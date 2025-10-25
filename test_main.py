from fastapi.testclient import TestClient
from main import app, fake_db

client = TestClient(app)


# Clear fake_db before each test
def setup_function():
    fake_db.clear()


# Test root endpoint
def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to Simple Backend API"}


# Test health check endpoint
def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


# Test creating an item
def test_create_item():
    response = client.post("/items", json={"id": 1, "name": "Test Item"})
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert data["name"] == "Test Item"


# Test getting all items
def test_get_items_empty():
    response = client.get("/items")
    assert response.status_code == 200
    assert response.json() == []


def test_get_items_after_creation():
    client.post("/items", json={"id": 1, "name": "Test Item"})
    response = client.get("/items")
    assert response.status_code == 200
    items = response.json()
    assert len(items) == 1
    assert items[0]["id"] == 1


# Test getting an item by ID
def test_get_item_by_id():
    client.post("/items", json={"id": 2, "name": "Another Item"})
    response = client.get("/items/2")
    assert response.status_code == 200
    assert response.json()["name"] == "Another Item"


def test_get_item_not_found():
    response = client.get("/items/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Item not found"


# Test updating an item
def test_update_item():
    client.post("/items", json={"id": 3, "name": "Old Name"})
    response = client.put("/items/3", json={"id": 3, "name": "Updated Name"})
    assert response.status_code == 200
    assert response.json()["name"] == "Updated Name"


# Test deleting an item
def test_delete_item():
    client.post("/items", json={"id": 4, "name": "Delete Me"})
    response = client.delete("/items/4")
    assert response.status_code == 200
    assert response.json()["detail"] == "Item deleted"
    # Confirm item is deleted
    response = client.get("/items/4")
    assert response.status_code == 404
