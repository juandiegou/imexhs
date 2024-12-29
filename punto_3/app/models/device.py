# device model
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime, timezone
from ..config.bd_conection import Entity 

class DeviceDB(Entity):
    """
    Device entity model representing a device in the system.
    
    This class defines the structure and behavior of Device objects in the database,
    including their properties and relationships.
    
    Attributes:
        id (int): Primary key identifier for the device
        name (str): Name of the device
        created_at (DateTime): Timestamp when the device was created
        updated_at (DateTime): Timestamp of last update
        
    Table name:
        device
        
    Example:
        >>> device = Device(name="Device1", status="active")
        >>> session.add(device)
        >>> session.commit()
    """
    
    __tablename__ = 'device'
    id = Column(Integer, primary_key=True, doc="Unique identifier for the device", autoincrement=True)
    name = Column(String(100), nullable=False, doc="Name of the device")
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), doc="Creation timestamp")
    updated_at = Column(DateTime, onupdate=lambda: datetime.now(timezone.utc), doc="Last update timestamp", default=lambda: datetime.now(timezone.utc))

    def model_dump_json(self) -> object:
        """
        Convert the database model to a object.
        
        Returns:
            ob: object representation of the database model
        """
        return {
            "id": self.id,
            "name": self.name,
            "created_at": self.created_at ,
            "updated_at": self.updated_at 
        }
        
    
    
class Device(BaseModel):
    id: int | None = None
    name: str
    created_at: datetime | None = None
    updated_at: datetime | None = None

    class ConfigDict:
        from_attributes = True