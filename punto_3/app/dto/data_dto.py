from pydantic import BaseModel, Field, field_validator
from typing import Optional, Dict, Any
from datetime import datetime

class DataDTO(BaseModel):
    """
    Data Transfer Object for Data entity.
    
    This DTO handles the transfer of data between the API layer and service layer,
    including validation and data transformation.
    
    Attributes:
        id (Optional[int]): Unique identifier for the data record
        name (str): Name of the data record
        value (float): Numeric value associated with the data
        created_at (datetime): Timestamp when the record was created
        updated_at (Optional[datetime]): Timestamp of last update
    """
    idf: Optional[int] = Field(None, description="Unique identifier for the data record")
    id: str = Field(..., min_length=1, max_length=100, description="Name of the data record")
    value: float = Field(..., description="Numeric value associated with the data")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Record creation timestamp")
    updated_at: Optional[datetime] = Field(None, description="Last update timestamp")

    

    class ConfigDict:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "name": "example_data",
                "value": 123.45,
                "created_at": "2023-08-10T12:00:00",
                "updated_at": "2023-08-10T12:00:00"
            }
        }

    @classmethod
    def from_orm_with_timestamps(cls, db_model: Any) -> 'DataDTO':
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
