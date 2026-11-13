import pytest
from app import create_app

@pytest.fixture
def client(tmp_path):
    db_path = tmp_path / "test.db"
    app = create_app({"TESTING": True, "DATABASE": str(db_path), "SECRET_KEY": "test"})
    with app.test_client() as client:
        yield client

def test_home_page(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Flor" in response.data

def test_register_product(client):
    response = client.post("/produtos/novo", data={
        "name": "Creme Hidratante Flor",
        "category": "Hidratante",
        "price": "25.00",
        "quantity": "10",
        "minimum_quantity": "5"
    }, follow_redirects=True)
    assert response.status_code == 200
    assert "Creme Hidratante Flor".encode() in response.data

def test_prevent_stock_below_zero(client):
    client.post("/produtos/novo", data={
        "name": "Máscara Facial", "category": "Máscara",
        "price": "30", "quantity": "2", "minimum_quantity": "1"
    })
    with client.application.app_context():
        from flask import current_app
        db = __import__("sqlite3").connect(current_app.config["DATABASE"])
        product_id = db.execute("SELECT id FROM products").fetchone()[0]
        db.close()
    response = client.post(f"/produtos/movimentar/{product_id}",
                           data={"movement": "saida", "amount": "3"},
                           follow_redirects=True)
    assert "A saída não pode ser maior".encode() in response.data
