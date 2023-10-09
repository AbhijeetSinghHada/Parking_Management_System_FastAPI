from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)


def test_add_vehicle():
    response = client.post("/vehicle", json={
        "vehicle_number": "RJ20CD7259",
        "vehicle_type": "LMV",
        "customer": {
            "customer_id": 1,
            "name": "John Doe",
            "email_address": "johndoe@example.com",
            "phone_number": "1234567890"
        }
    }, cookies={"access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOjEsIm5hbWUiOiJBYmhpamVldCBTaW5naCIsInJvbGUiOlsiQWRtaW4iLCJPcGVyYXRvciJdLCJleHAiOjE2OTY3Njc5NTN9.6AFYQWldjFLIsjbakxRTcf5Wu6_Jzld1deoUDckl5_Y"})
    assert response.status_code == 200
    assert response.json() == {
        "vehicle_number": "RJ20CD7259",
        "vehicle_type": "LMV",
        "customer": {
            "customer_id": 1,
            "name": "John Doe",
            "email_address": "johndoe@example.com",
            "phone_number": "1234567890"
        },
        "message": "Vehicle added successfully"
    }
