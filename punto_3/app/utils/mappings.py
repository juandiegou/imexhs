from typing import  List
import numpy as np
from ..models import Data, DataDB, Device, DeviceDB
from datetime import datetime, timezone

def mapping_data_to_db(data: Data) -> DataDB:
    """
    Maps Data model to DataDB model for database operations.
    
    Args:
        data (Data): Source data model
        
    Returns:
        DataDB: Database model instance
    """
    return DataDB(
        id=data.id if hasattr(data, 'id') else None,
        data=data.data,
        device_id=data.device_id,
        average_bf_normalization=data.average_bf_normalization,
        average_af_normalization=data.average_af_normalization,
        data_size=len(data.data) if data.data else 0,
        created_date=data.created_date or datetime.utcnow(),
        update_date=data.update_date
    )

def mapping_db_to_data(db_data: DataDB) -> Data:
    """
    Maps DataDB model to Data model for API responses.
    
    Args:
        db_data (DataDB): Source database model
        
    Returns:
        Data: API model instance
    """
    return Data(
        id=db_data.id,
        data=db_data.data,
        device_id=db_data.device_id,
        average_bf_normalization=db_data.average_bf_normalization,
        average_af_normalization=db_data.average_af_normalization,
        data_size=db_data.data_size,
        created_date=db_data.created_date,
        update_date=db_data.update_date
    )

def mapping_db_list_to_data_list(db_data_list: List[DataDB]) -> List[Data]:
    """
    Maps a list of DataDB models to Data models.
    
    Args:
        db_data_list (List[DataDB]): List of database models
        
    Returns:
        List[Data]: List of API models
    """
    return [mapping_db_to_data(item) for item in db_data_list]

def calculate_data_metrics(data: List[int]) -> tuple[float, float]:
    """
    Calculates data metrics (averages before and after normalization).
    
    Args:
        data (List[int]): Raw data values
        
    Returns:
        tuple[float, float]: (average_before, average_after)
    """
    if not data:
        return 0.0, 0.0
        
    avg_before = np.mean(data)
    
    # Normalize data (example implementation)
    # max_val = max(abs(min(data)), abs(max(data)))
    # normalized = [x/max_val if max_val != 0 else 0 for x in data]
    # avg_after = sum(normalized) / len(normalized)
    normalized = np.linalg.norm(data)
    avg_after = np.mean(normalized)
    
    
    return avg_before, avg_after


def mapping_device_to_db(device: Device) -> DeviceDB:
    """
    Maps Device model to DeviceDB model for database operations.
    
    Args:
        device (Device): Source device model
        
    Returns:
        DeviceDB: Database model instance
    """
    return DeviceDB(
        id=device.id if hasattr(device, 'id') else None,
        name=device.name,
        description=device.description,
        device_type=device.device_type,
        created_at=device.created_date or datetime.now(tz=timezone.utc),
        update_at=device.update_date
    )
    
def mapping_db_to_device(db_device: DeviceDB) -> Device:
    """
    Maps DeviceDB model to Device model for API responses.
    
    Args:
        db_device (DeviceDB): Source database model
        
    Returns:
        Device: API model instance
    """
    return Device(
        id=db_device.id,
        name=db_device.name,
        created_at=str(db_device.created_at),
        updated_at=str(db_device.updated_at)
    )
    
def mapping_db_list_to_device_list(db_device_list: List[DeviceDB]) -> List[Device]:
    """
    Maps a list of DeviceDB models to Device models.
    
    Args:
        db_device_list (List[DeviceDB]): List of database models
    
    Returns:
        List[Device]: List of API models
    """
    return [mapping_db_to_device(item) for item in db_device_list]

def mapping_device_to_db(device: Device) -> DeviceDB:
    """
    Maps Device model to DeviceDB model for database operations.
    
    Args:
        device (Device): Source device model
        
    Returns:
        DeviceDB: Database model instance
    """
    return DeviceDB(
        id=device.id if hasattr(device, 'id') else None,
        name=device.name,
        created_at=device.created_at or datetime.now(tz=timezone.utc),
        updated_at=device.updated_at or datetime.now(tz=timezone.utc)
    )
    
    
def mapping_device_to_json(device: Device) -> dict:
    """
    Maps Device model to a JSON-compatible dictionary.
    
    Args:
        device (Device): Source device model
        
    Returns:
        dict: Dictionary representation of the device
    """
    return {
        "id": device.id,
        "name": device.name,
        "created_at": str(device.created_at),
        "updated_at": str(device.updated_at)
    }
    
def mapping_data_to_json(data: Data) -> dict:
    """
    Maps Data model to a JSON-compatible dictionary.
    
    Args:
        data (Data): Source data model
        
    Returns:
        dict: Dictionary representation of the data
    """
    return {
        "id": data.id,
        "data": data.data,
        "device_id": data.device_id,
        "average_bf_normalization": data.average_bf_normalization,
        "average_af_normalization": data.average_af_normalization,
        "data_size": data.data_size,
        "created_date": str(data.created_date),
        "update_date": str(data.update_date)
    }
    
def mapping_device_list_to_json(device_list: List[Device]) -> List[dict]:
    """
    Maps a list of Device models to a list of JSON-compatible dictionaries.
    
    Args:
        device_list (List[Device]): List of device models
        
    Returns:
        List[dict]: List of dictionary representations of the devices
    """
    return [mapping_device_to_json(item) for item in device_list]

def mapping_data_list_to_json(data_list: List[Data]) -> List[dict]:
    """
    Maps a list of Data models to a list of JSON-compatible dictionaries.
    
    Args:
        data_list (List[Data]): List of data models
        
    Returns:
        List[dict]: List of dictionary representations of the data
    """
    return [mapping_data_to_json(item) for item in data_list]
