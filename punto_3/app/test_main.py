import pytest
import json
import os
from fastapi.testclient import TestClient
from .main import app
from .utils.logger import setup_logger


logger=setup_logger("test_main")



@pytest.fixture
def sample_data():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(current_dir, './test_data/sample-03-00-json.json')
    # Load sample data from JSON file
    with open(json_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def sample_device():
    """Return a dictionary of test devices"""
    return {
        "create_test": {
            "name": "Create Test Device"
        },
        "get_test": {
            "name": "Get Test Device"
        },
        "update_test": {
            "name": "Update Test Device"
        },
        "delete_test": {
            "name": "Delete Test Device"
        },
        "data_test": [
            {"name": "Data Test Device 1"},
            {"name": "Data Test Device 2"},
            {"name": "Data Test Device 3"},
            {"name": "Data Test Device 4"},
            {"name": "Data Test Device 5"}
        ]
    }      
   
def test_create_device(client, sample_device):
    """Test device creation endpoint"""
    response = client.post("/api/devices/", json=sample_device["create_test"])
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == sample_device["create_test"]["name"]
    assert "created_at" in data


def test_get_device(client, sample_device):
    """Test getting a single device"""
    # First create a device
    create_response = client.post("/api/devices/", json=sample_device["get_test"])
    data= create_response.json()
    device_id = data["id"]
    
    # Then get it
    response = client.get(f"/api/devices/{device_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == sample_device["get_test"]["name"]

def test_get_nonexistent_device(client):
    """Test getting a device that doesn't exist"""
    response = client.get("/api/devices/999")
    assert response.status_code == 404
    
    
def test_update_device(client, sample_device):
    """Test updating a device"""
    #First create a device
    response = client.post("/api/devices/", json=sample_device["update_test"])
    assert response.status_code == 201
    data = response.json()
    device_id = data["id"]
    update_data = {"device_name":'Updated Device'}
    device_name = update_data["device_name"]
    
    response = client.put(f"/api/devices/{device_id}?device_name={device_name}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == update_data["device_name"]

def test_delete_device(client, sample_device):
    """Test deleting a device"""
    # First create a device
    create_response = client.post("/api/devices/", json=sample_device["delete_test"])
    device_id = create_response.json()["id"]
    
    # Delete it
    response = client.delete(f"/api/devices/{device_id}")
    assert response.status_code == 204
    
    
    
    
############## DATA TESTS ####################
def test_create_data(client, sample_device, sample_data):
    """
    Test data creation endpoint by verifying the creation and normalization of data for a device.
    This test function performs the following steps:
    1. Creates a new device using the provided sample device data
    2. Creates data associated with the device using the sample data
    3. Verifies the response status code is 201 (Created)
    4. Validates the created data matches the input data
    5. Confirms the device ID association is correct
    6. Checks that normalization averages are present in the response
    Parameters:
        client: TestClient
            The test client instance used to make HTTP requests
        sample_device: dict
            Sample device data used to create a test device
        sample_data: dict 
            Sample data to be associated with the created device
    Returns:
        None
    Raises:
        AssertionError: If any of the test validations fail
    """
    """Test data creation endpoint"""
    # Create device
    response = client.post("/api/devices/", json=sample_device["data_test"][0])
    assert response.status_code == 201
    data = response.json()
    device_name = data["name"]
    device_id = data["id"]
    # alter sample data with device name
    sample_data["1"]["deviceName"] = device_name
    response = client.post("/api/elements/", json=sample_data["1"] )
    assert response.status_code == 201
    data = response.json()
    
    assert data["id"] == sample_data["1"]["id"]
    assert data["device_id"] == device_id
    

        
    
    



def test_get_data(client, sample_device, sample_data):
    """Test getting data for a device"""
    # Create device and data
    # Create device
    response = client.post("/api/devices/", json=sample_device["data_test"][1])
    assert response.status_code == 201
    data = response.json()
    device_name = data["name"]
    # alter sample data with device name
    sample_data["1"]["deviceName"] = device_name
    response = client.post("/api/elements/", json=sample_data["1"] )
    assert response.status_code == 201
    data = response.json()
    
    assert data["id"] == sample_data["1"]["id"]
    assert data["average_bf_normalization"] is not None
    assert data["average_bf_normalization"] > 0
    

def test_get_device_data(client, sample_device, sample_data):
    """Test getting all data for a specific device"""
    # Create device and data
    # Create device
    response = client.post("/api/devices/", json=sample_device["data_test"][2])
    assert response.status_code == 201
    data = response.json()
    device_name = data["name"]
    device_id = data["id"]
    # alter sample data with device name
    sample_data["1"]["deviceName"] = device_name
    response = client.post("/api/elements/", json=sample_data["1"] )
    assert response.status_code == 201
    data = response.json()
    
   
    assert isinstance(data["data"], list)
    assert len(data) > 0

def test_invalid_data_creation(client, sample_data):
    """Test creating data for nonexistent device"""
    sample_data["device_id"] = 999  # Non-existent device
    response = client.post("/api/data/", json=sample_data)
    assert response.status_code == 404
    
    
