from typing import List, Optional, Union
from fastapi import APIRouter, HTTPException, Response
from fastapi.responses import JSONResponse
from ..models.device import Device
from ..utils.logger import setup_logger
from ..services.device_service import DeviceService
from ..utils.mappings import mapping_device_to_db, mapping_db_to_device, mapping_db_list_to_device_list, mapping_device_to_json, mapping_device_list_to_json
import logging

router = APIRouter(
    prefix="/api/devices",
    tags=["devices"]
)

service = DeviceService() 

@router.post("/", response_model=None)
def create_device(device: Device) -> JSONResponse:
    """
    Creates a new device in the system.

    Args:
        device (Device): The device to be created. Must be an instance of Device model.

    Returns:
        The created device with its assigned ID and metadata.

    Raises:
        ValidationError: If the device data is invalid.
        DatabaseError: If there's an error while creating the device in the database.
    """
    device = mapping_device_to_db(device)
    creation_device = service.create_device(device)
    if creation_device:
        creation_device = mapping_device_to_json(mapping_db_to_device(creation_device)  )
        return JSONResponse(content=creation_device, status_code=201)
    else:
        return HTTPException(status_code=400, detail="Device creation failed")
    
@router.get("/", response_model=None)
def get_devices(name: Optional[str] = None, limit: Optional[int] = None, start: Optional[int] = None) -> JSONResponse:
    """
    Retrieves all devices from the service.

    Args:
        name (str): The name of the device to filter by.
        limit (int): The maximum number of devices to retrieve.
        start (int): The starting index of the devices to retrieve.

    Returns:
        list: A collection of all devices stored in the service.
    """
    all_devices = service.get_all_devices(name, limit, start)
    if all_devices:
        all_devices = mapping_device_list_to_json(mapping_db_list_to_device_list(all_devices))
        return JSONResponse(content=all_devices, status_code=200)
    else:
        return HTTPException(status_code=404, detail="No devices found")
    
@router.get("/{device_id}", response_model=None)
def get_device(device_id: int) -> JSONResponse:
    """
    Retrieve a device by its ID.

    Args:
        device_id (int): The unique identifier of the device to retrieve.

    Returns:
        The device matching the provided ID. The return type depends on the service implementation.
    """
    device = service.get_device_by_id(device_id)
    if device:
        device = mapping_device_to_json(mapping_db_to_device(device))
        return JSONResponse(content=device, status_code=200)
    else:
        return HTTPException(status_code=404, detail="Device not found")
    
@router.put("/{device_id}", response_model=None)
def update_device(device_id: int, device_name: str) -> JSONResponse:
    """
    Update a device by its ID.

    Args:
        device_id (int): The unique identifier of the device to update.
        device_name (str): The new name to assign to the device.

    Returns:
        The updated device matching the provided ID. The return type depends on the service implementation.
    """
    updated_device = service.update_device(device_id, device_name)
    if updated_device:
        updated_device = mapping_device_to_json(mapping_db_to_device(updated_device))
        return JSONResponse(content=updated_device, status_code=200)
    else:
        return HTTPException(status_code=404, detail="Device not found")
    
@router.delete("/{device_id}")
def delete_device(device_id: int,response_model=None ) -> JSONResponse:
    """
    Delete a device by its ID.

    Args:
        device_id (int): The unique identifier of the device to delete.

    Returns:
        The status of the operation. The return type depends on the service implementation.
    """
    deleted_device = service.delete_device(device_id)
    if deleted_device:
        deleted_device = mapping_device_to_json(mapping_db_to_device(deleted_device))
        return JSONResponse(content={"message":"Element deleted successfully"}, status_code=204)
    else:
        return HTTPException(status_code=404, detail="Device not found")
    

    
    