from fastapi.testclient import TestClient
from main import app, create_db_tables

client = TestClient(app)

def test_read_cardapio():
    create_db_tables()
    response = client.get('/cardapio')
    assert response.status_code == 200