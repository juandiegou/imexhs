from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from typing import List, Union
from ..models.data import Data,DataInput
from ..services import DataService, DeviceService
from ..utils.mappings import mapping_data_to_db, mapping_db_to_data, mapping_db_list_to_data_list, mapping_data_to_json, mapping_data_list_to_json, mapping_device_to_json, mapping_db_to_device
from ..utils.logger import setup_logger
router = APIRouter(
    prefix="/api/elements",
    tags=["elements"]
)


logger=setup_logger("data_router")

service = DataService()
device_service = DeviceService()

@router.post("/", response_model= None)
def create_element(element_data: DataInput) -> JSONResponse:
    """
    Creates a new element in the system.

    Args:
        element (Data): The data element to be created. Must be an instance of Data model.

    Returns:
        The created element with its assigned ID and metadata.

    Raises:
        ValidationError: If the element data is invalid.
        DatabaseError: If there's an error while creating the element in the database.
    """
    # print(element_data,"original input")
    element_data = element_data.dict()
    device_name = element_data.pop("deviceName")
    # print(element_data,"input without device name")
    element = device_service.get_device_by_name(device_name)
    logger.info(f"Device found: {device_name}")
    if not element:
        logger.error(f"Device not found: {device_name}")
        logger.error(f"Device not found: {element}")
        return HTTPException(status_code=404, detail="Device not found")
    element_data["device_id"] = mapping_db_to_device(element).id
    element_data["data"] = [int(x) for y in element_data["data"] for x in y if x.isdigit()]
    data_element_creation = Data(**element_data)
    logger.info(f"Element creation data: {data_element_creation}")
    element = mapping_data_to_db(data_element_creation)
    creation_element_data = service.create_data(element)
    logger.info(f"Element created: {creation_element_data}")
    if creation_element_data:
        creation_element = mapping_data_to_json(mapping_db_to_data(creation_element_data))
        return JSONResponse(content=creation_element, status_code=201)
    else:
        return HTTPException(status_code=400, detail="Element creation failed")
    

@router.get("/", response_model=None)
def get_elements() -> JSONResponse:
    """
    Retrieves all elements from the service.

    Returns:
        list: A collection of all elements stored in the service.
    """
    all_elements=service.get_all_data()
    if all_elements:
        all_elements = mapping_data_list_to_json(mapping_db_list_to_data_list(all_elements))
        return JSONResponse(content=all_elements, status_code=200)
    else:
        return HTTPException(status_code=404, detail="No elements found")

@router.get("/{element_id}", response_model=None)
def get_element(element_id: str) -> JSONResponse:
    """
    Retrieve an element by its ID.

    Args:
        element_id (str): The unique identifier of the element to retrieve.

    Returns:
        The element matching the provided ID. The return type depends on the service implementation.

    Raises:
        May raise exceptions depending on the service implementation.
    """
    element_data =service.get_data_by_id(element_id)
    if element_data:
        element_data = mapping_data_to_json(mapping_db_to_data(element_data))
        return JSONResponse(content=element_data, status_code=200)
    else:
        return HTTPException(status_code=404, detail="Element not found")
    

@router.put("/{element_id}", response_model=None)
def update_element(element_id: str, device_name: str) -> JSONResponse:
    """
    Updates an element in the data system.

    Args:
        element_id (str): Unique identifier for the element to be updated
        device_name (str): New name for the device to be updated

    Returns:
        Data: Updated element information

    Raises:
        HTTPException: If element is not found or update fails
    """
    update_element_data = service.update_data(element_id, device_name)
    if update_element_data:
        update_element = mapping_data_to_json(mapping_db_to_data(update_element))
        return JSONResponse(content=update_element, status_code=200)
    else:
        return HTTPException(status_code=404, detail="Element not found")
    

@router.delete("/{element_id}", response_model=None)
def delete_element(element_id: str)-> JSONResponse:
    """
    Delete an element by its ID.

    Args:
        element_id (str): The unique identifier of the element to be deleted.

    Returns:
        dict: A dictionary containing a success message.
                Format: {"message": "Element deleted successfully"}

    Raises:
        HTTPException: If element is not found or deletion fails.
    """
    element_delete =service.delete_data(element_id)
    if element_delete:
        element_delete = mapping_data_to_json(mapping_db_to_data(element_delete))
        return JSONResponse(content={"message": "Element deleted successfully"}, status_code=200)
    else:
        return HTTPException(status_code=404, detail="Element not found")
    
