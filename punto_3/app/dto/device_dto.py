from pydantic import BaseModel, Field, field_validator
from typing import Optional, Dict, Any
from datetime import datetime
from enum import Enum


class DeviceDTO(BaseModel):
    """
    Data Transfer Object for Device entity.
    
    This DTO handles the transfer of device data between layers of the application,
    providing validation, serialization, and data transformation capabilities.
    
    Attributes:
        id (Optional[int]): Unique identifier for the device
        name (str): Name of the device (1-100 characters)
        status (DeviceStatus): Current operational status
        created_at (datetime): Creation timestamp (UTC)
        updated_at (Optional[datetime]): Last update timestamp
        description (Optional[str]): Additional details (max 500 chars)
        
    Example:
        >>> device_dto = DeviceDTO(
        ...     name="Device1",
        ... )
    """
    id: Optional[int] = Field(None, description="Unique identifier for the device")
    name: str = Field(..., min_length=1, max_length=100, description="Name of the device")
    created_at: datetime = Field(default_factory=lambda: datetime.now(datetime.timezone.utc), description="Device creation timestamp")
    updated_at: Optional[datetime] = Field(None, description="Last update timestamp")


 
    def __init__(self, **data: Any):
        super().__init__(**data)
        self.update_timestamp()
        

    class ConfigDict:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "name": "device_001",
                "created_at": "2023-08-10T12:00:00",
                "updated_at": "2023-08-10T12:00:00"
            }
        }

    @classmethod
    def from_orm_with_timestamps(cls, db_model: Any) -> 'DeviceDTO':
        """
        Create a DTO instance from a database model with proper timestamp handling.
        
        This method ensures that datetime fields are properly converted when
        creating a DTO from an ORM model.
        
        Args:
            db_model: The database model instance to convert
            
        Returns:
            DeviceDTO: New DTO instance with data from the model
            
        Example:
            >>> device_dto = DeviceDTO.from_orm_with_timestamps(device_model)
        """
        return cls.model_validate(db_model)

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert DTO to dictionary format.
        
        Returns:
            Dict[str, Any]: Dictionary representation of DTO
        """
        return self.model_dump(exclude_unset=True)

    def update_timestamp(self) -> None:
        """Update the updated_at timestamp to current time"""
        self.updated_at = datetime.now(datetime.timezone.utc)
