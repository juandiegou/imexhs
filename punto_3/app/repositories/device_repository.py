from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from ..models.device import DeviceDB as Device
from typing import Optional, List
from ..config.bd_conection import get_db_connection, create_db
from ..utils.logger import setup_logger
from datetime import datetime
import psycopg2

class DeviceRepository:
    """
    A repository class for managing device operations with a database.
    This class provides methods for CRUD operations (Create, Read, Update, Delete)
    and statistical analysis of devices stored in a database.
    """
    
    db: Session | None = None
    
    def __init__(self):
        """Initialize DeviceRepository with database connection.

        The constructor establishes a database connection for the DeviceRepository instance
        using the get_db_connection() function.

        Returns:
            None
        """
        self.logger = setup_logger('device_repository')
        try:
            create_db()
            self.db = get_db_connection()
        except UnicodeDecodeError as e:
            self.logger.error(f"Error connecting to database: {str(e)}")
            raise Exception("Error connecting to database")

        
    def get_devices(self, name: Optional[str] = None, limit: int = 100, start: int = 0) -> List[Device]:
        """
        Retrieve a list of devices from the database with optional filtering and pagination.

        Args:
            name (str, optional): Filter devices by name. Defaults to None.
            limit (int, optional): Maximum number of devices to return. Defaults to 100.
            start (int, optional): Number of devices to skip for pagination. Defaults to 0.

        Returns:
            List[Device]: A list of Device objects matching the criteria.

        Example:
            >>> repository.get_devices(name="device1", limit=10, start=0)
            [Device(id=1, name="device1"), ...]
        """
        try:
            self.logger.info(f"Fetching devices with name={name}, limit={limit}, start={start}")
            if name:
                return self.db.query(Device).filter(Device.name == name).limit(limit).offset(start).all()
            return self.db.query(Device).limit(limit).offset(start).all()
        except SQLAlchemyError as e:
            self.logger.error(f"Database error while fetching devices: {str(e)}")
            raise
    
    def get_device_by_id(self, id: int) -> Optional[Device]:
        """
        Retrieve a device by its ID from the database.

        Args:
            id (int): The unique identifier of the device.

        Returns:
            Optional[Device]: The device if found, None otherwise.

        Raises:
            SQLAlchemyError: If there's a database error.
        """
        try:
            return self.db.query(Device).filter(Device.id == id).first()
        except SQLAlchemyError as e:
            self.db.rollback()
            raise Exception(f"Database error: {str(e)}")
        
    def get_device_by_name(self, name: str) -> Optional[Device]:
        """
        Retrieve a device by its name from the database.

        Args:
            name (str): The name of the device.

        Returns:
            Optional[Device]: The device if found, None otherwise.

        Raises:
            SQLAlchemyError: If there's a database error.
        """
        try:
            return self.db.query(Device).filter(Device.name == name).first()
        except SQLAlchemyError as e:
            self.db.rollback()
            raise Exception(f"Database error: {str(e)}")
        

    def create_device(self, device: Device) -> Device:
        """
        Create a new device in the database.

        Args:
            device (Device): The device object to be created.

        Returns:
            Device: The created device with updated information.

        Raises:
            SQLAlchemyError: If there's a database error.
            ValueError: If the device data is invalid.
        """
        try:
            self.logger.info("Creating new device: %s", str(device).encode('utf-8', errors='ignore').decode('utf-8'))
            if not device.name:                
                self.logger.error("Attempted to create device with empty name")
                raise ValueError("Device name cannot be empty")
            if not self.db:
                raise Exception("Database connection not established")

            self.db.add(device)
            self.db.commit()
            self.db.refresh(device)
            return device
        except SQLAlchemyError as e:
            self.logger.error(f"Error creating device: {str(e)}")
            raise Exception(f"Error creating device: {str(e)}")

    def update_device(self, device: Device) -> Device:
        """
        Update an existing device in the database.

        Args:
            device (Device): The device object with updated information.

        Returns:
            Device: The updated device.

        Raises:
            SQLAlchemyError: If there's a database error.
            ValueError: If the device doesn't exist.
        """
        try:
            self.logger.info(f"Updating device with id={device.id}")
            existing_device = self.get_device_by_id(device.id)
            if not existing_device:
                raise ValueError(f"Device with id {device.id} not found")
            
            self.db.add(device)
            self.db.commit()
            self.db.refresh(device)
            return device
        except SQLAlchemyError as e:
            self.logger.error(f"Error updating device: {str(e)}")
            self.db.rollback()
            raise Exception(f"Error updating device: {str(e)}")

    def delete_device(self, device: Device) -> Device:
        """
        Delete a device from the database.

        Args:
            device (Device): The device to be deleted.

        Returns:
            Device: The deleted device.

        Raises:
            SQLAlchemyError: If there's a database error.
            ValueError: If the device doesn't exist.
        """
        try:
            self.logger.info(f"Deleting device: {device}")
            self.db.delete(device)
            self.db.commit()
            return device
        except SQLAlchemyError as e:
            self.logger.error(f"Error deleting device: {str(e)}")
            self.db.rollback()
            raise Exception(f"Error deleting device: {str(e)}")

    def delete_device_by_id(self, id: int) -> Optional[Device]:
        """
        Delete a device by its ID.

        Args:
            id (int): The ID of the device to delete.

        Returns:
            Optional[Device]: The deleted device if found, None otherwise.

        Raises:
            SQLAlchemyError: If there's a database error.
        """
        try:
            device = self.get_device_by_id(id)
            if device:
                return self.delete_device(device)
            return None
        except SQLAlchemyError as e:
            self.db.rollback()
            raise Exception(f"Error deleting device: {str(e)}")

    def delete_device_by_name(self, name: str) -> Optional[Device]:
        """
        Delete devices by name.

        Args:
            name (str): The name of the devices to delete.

        Returns:
            Optional[Device]: The deleted device if found, None otherwise.

        Raises:
            SQLAlchemyError: If there's a database error.
        """
        try:
            device = self.get_devices(name)
            if device:
                return self.delete_device(device)
            return None
        except SQLAlchemyError as e:
            self.db.rollback()
            raise Exception(f"Error deleting device: {str(e)}")

    def get_device_size(self, name: str) -> int:
        """
        Get total number of devices with given name.

        Args:
            name (str): The name to filter devices by.

        Returns:
            int: The number of devices with the given name.

        Raises:
            SQLAlchemyError: If there's a database error.
        """
        try:
            devices = self.get_devices(name)
            return len(devices)
        except SQLAlchemyError as e:
            raise Exception(f"Error getting device count: {str(e)}")

   