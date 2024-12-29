import datetime
from pydantic import BaseModel
from sqlalchemy import Column, Integer, ForeignKey, Float, DateTime, ARRAY, String
from sqlalchemy.orm import relationship
from ..config import Entity

class DataDB(Entity):
    """
    Data entity model representing a data record in the system.
    
    This class defines the structure and behavior of Data objects in the database,
    including their properties and relationships.
    
    Attributes:
        id (int): Primary key identifier for the data record
        data (list[int]): List of data values
        device_id (int): Foreign key reference to the device
        average_bf_normalization (float): Average before normalization
        average_af_normalization (float): Average after normalization
        data_size (int): Number of data values
        created_date (DateTime): Timestamp when the data was created
        update_date (DateTime): Timestamp of last update
        
    Table name:
        data
        
    Example:
        >>> data = Data(data=[1, 2, 3], device_id=1)
        >>> session.add(data)
        >>> session.commit()
        
    """
    __tablename__ = 'data'
    idf = Column(Integer, primary_key=True, index=True)
    id = Column(String, index=True)
    data = Column(ARRAY(Integer))
    device_id = Column(Integer, ForeignKey('device.id'))
    device = relationship("DeviceDB")
    average_bf_normalization = Column(Float)
    average_af_normalization = Column(Float)
    data_size = Column(Integer)
    created_date = Column(DateTime, default=lambda: datetime.datetime.now(datetime.timezone.utc))
    update_date = Column(DateTime, onupdate=lambda: datetime.datetime.now(datetime.timezone.utc), default=lambda: datetime.datetime.now(datetime.timezone.utc))

class Data(BaseModel):
    idf: int | None = None
    id: str
    data: list[int]
    device_id: int
    average_bf_normalization: float | None = None
    average_af_normalization: float | None = None
    data_size: int | None = None
    created_date: datetime.datetime | None = None
    update_date: datetime.datetime | None = None

    class ConfigDict:
        from_attributes = True
    

class DataInput(BaseModel):
    id: str
    data: list[str]
    deviceName: str

    class ConfigDict:
        json_schema_extra = {"example": {"id": "123", "data": ["1", "2"], "deviceName": "device1"}}
        from_attributes = True

    def dict(self, *args, **kwargs):
        return super().model_dump(*args, **kwargs)
    
    