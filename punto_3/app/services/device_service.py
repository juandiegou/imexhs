from typing import List, Optional
from fastapi import HTTPException
from ..models.device import DeviceDB as Device
from ..repositories.device_repository import DeviceRepository
from ..dto.device_dto import DeviceDTO
from ..utils.logger import setup_logger

class DeviceService:
    """
    Service layer for handling Device operations.
    
    This service provides high-level business logic for device operations,
    handling data validation, error management, and coordination between
    the API layer and data access layer.
    
    Attributes:
        repository (DeviceRepository): Repository for device data operations
        logger (Logger): Service-level logging instance
        
    Dependencies:
        - DeviceRepository for data persistence
        - FastAPI for HTTP exception handling
        - Logging utility for operation tracking
    """
    
    def __init__(self):
        """
        Initialize DeviceService.
        
        Sets up:
        - Device repository connection
        - Logging configuration
        - Error handling preparations
        """
        self.repository = DeviceRepository()
        self.logger = setup_logger('device_service')
        
    def get_all_devices(self, name: Optional[str] = None, 
                       limit: int = 100, 
                       start: int = 0) -> List[DeviceDTO]:
        """
        Retrieve a filtered list of devices with pagination.
        
        Args:
            name (str, optional): Filter by device name
            limit (int): Maximum number of records to return
            start (int): Starting offset for pagination
            
        Returns:
            List[DeviceDTO]: List of device DTOs matching criteria
            
        Raises:
            HTTPException: 500 on operation failure
            
        Example:
            >>> devices = service.get_all_devices(name="dev", limit=10)
        """
        try:
            devices = self.repository.get_devices(name, limit, start)
            return [device for device in devices]
        except Exception as e:
            self.logger.error(f"Error retrieving devices: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))
            
    def get_device_by_id(self, id: int) -> DeviceDTO:
        """Get device by ID.

        This method retrieves a device from the repository by its ID and returns it as a DTO.

        Args:
            id (int): The unique identifier of the device to retrieve.

        Returns:
            DeviceDTO: The device data transfer object containing the device information.

        Raises:
            HTTPException: If device is not found (404) or if there's a server error (500).
        """
        try:
            device = self.repository.get_device_by_id(id)
            if not device:
                raise HTTPException(status_code=404, detail=f"Device with id {id} not found")
            return device
        except HTTPException:
            raise
        except Exception as e:
            self.logger.error(f"Error retrieving device by id: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))
    
    def get_device_by_name(self, name: str) -> DeviceDTO:
        """Get device by name.

        This method retrieves a device from the repository by its name and returns it as a DTO.

        Args:
            name (str): The name of the device to retrieve.

        Returns:
            DeviceDTO: The device data transfer object containing the device information.

        Raises:
            HTTPException: If device is not found (404) or if there's a server error (500).
        """
        try:
            device = self.repository.get_device_by_name(name)
            if not device:
                raise HTTPException(status_code=404, detail=f"Device with name {name} not found")
            return device
        except HTTPException:
            raise
        except Exception as e:
            self.logger.error(f"Error retrieving device by name: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))
        
            
    def create_device(self, device_dto: DeviceDTO) -> DeviceDTO:
        """Create new device.

        This method creates a new device in the system using the provided DeviceDTO.

        Args:
            device_dto (DeviceDTO): Data transfer object containing the device information to be created.

        Returns:
            DeviceDTO: Data transfer object containing the created device information.

        Raises:
            HTTPException: If there's an error during device creation with status code 500.
        """
        try:
            device = Device(**device_dto.model_dump_json())
            created_device = self.repository.create_device(device)
            return created_device
        except Exception as e:
            self.logger.error(f"Error creating device: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))
            
    def update_device(self, id: int, new_name: str) -> DeviceDTO:
        """
        Updates an existing device's information in the system.
        Args:
            id (int): The unique identifier of the device to update
            device_dto (DeviceDTO): Data transfer object containing the updated device information
        Returns:
            DeviceDTO: Updated device information wrapped in a DTO object
        Raises:
            HTTPException: If device with given id is not found (404) or if there's a server error (500)
        """
        try:
            print(id, new_name)
            existing_device = self.repository.get_device_by_id(id)
            if not existing_device:
                raise HTTPException(status_code=404, detail=f"Device with id {id} not found")
            existing_device.name = new_name  
            updated_device = self.repository.update_device(existing_device)
            return updated_device
        except HTTPException:
            raise
        except Exception as e:
            self.logger.error(f"Error updating device: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))
            
    def delete_device(self, id: int) -> DeviceDTO:
        """
        Delete a device from the system by its ID.
        Args:
            id (int): The unique identifier of the device to delete.
        Returns:
            DeviceDTO: Data transfer object containing the deleted device information.
        Raises:
            HTTPException: If device is not found (404) or if there's a server error (500).
        """
        try:
            device = self.repository.get_device_by_id(id)
            if not device:
                raise HTTPException(status_code=404, detail=f"Device with id {id} not found")
                
            deleted_device = self.repository.delete_device(device)
            return deleted_device
        except HTTPException:
            raise
        except Exception as e:
            self.logger.error(f"Error deleting device: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))
