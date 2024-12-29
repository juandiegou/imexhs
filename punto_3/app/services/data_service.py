from typing import List, Optional
from fastapi import HTTPException
from ..models.data import DataDB as Data
from ..repositories.data_repository import DataRepository
from ..dto.data_dto import DataDTO
from ..utils.logger import setup_logger
from ..utils.mappings import (
    mapping_data_to_db,
    mapping_db_to_data,
    mapping_db_list_to_data_list,
    calculate_data_metrics
)

class DataService:
    """
    Service layer for managing Data operations and business logic.

    This service class provides a high-level interface for data operations,
    implementing business rules, validation, and error handling. It acts as
    an intermediary between the API controllers and the data repository.

    Key Features:
        - CRUD operations for Data entities
        - Data validation through DTOs
        - Error handling and logging
        - Business logic implementation
        - Transaction management

    Attributes:
        repository (DataRepository): Instance of data repository for database operations
        logger (Logger): Logging instance for error and operation tracking

    Dependencies:
        - FastAPI for HTTP exception handling
        - DataRepository for data persistence
        - DataDTO for data transfer and validation
        - Logger for operation tracking

    Example:
        >>> service = DataService()
        >>> data_dto = DataDTO(name="test", value=123.45)
        >>> created = service.create_data(data_dto)
        >>> data_list = service.get_all_data(limit=10)

    Note:
        All methods include error handling and logging.
        Failed operations are rolled back automatically.
    """

    def __init__(self):
        """
        Initialize the DataService with required dependencies.

        Sets up:
            - Database repository connection
            - Logging configuration
            - Error handling preparations

        Raises:
            Exception: If required dependencies cannot be initialized
        """
        self.repository = DataRepository()
        self.logger = setup_logger('data_service')
       
        
    def get_all_data(self, name: Optional[str] = None, 
                     limit: int = 100, 
                     start: int = 0) -> List[DataDTO]:
        """
        Retrieve a filtered and paginated list of data records.

        This method provides flexible data retrieval with optional filtering
        by name and pagination support.

        Args:
            name (Optional[str]): Filter records by name
            limit (int): Maximum number of records to return (default: 100)
            start (int): Starting offset for pagination (default: 0)

        Returns:
            List[DataDTO]: List of data records converted to DTOs

        Raises:
            HTTPException: 
                - 500: Database or server errors
                - 400: Invalid parameters

        Example:
            >>> service.get_all_data(name="sensor", limit=10, start=0)
            [DataDTO(...), DataDTO(...), ...]
        """
        try:
            self.logger.info(f"Retrieving data: name={name}, limit={limit}, start={start}")
            db_data = self.repository.get_data(name, limit, start)
            return mapping_db_list_to_data_list(db_data)
        except Exception as e:
            self.logger.error(f"Error retrieving data: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))
            
    def get_data_by_id(self, id: str) -> DataDTO:
        """Get data by ID from the repository.

        Args:
            id (str): The unique identifier of the data to retrieve.

        Returns:
            DataDTO: The data transfer object containing the retrieved data.

        Raises:
            HTTPException: If data is not found (404) or if there's a server error (500).
            
        Example:
            >>> data_service.get_data_by_id(1)
            DataDTO(id=1, ...)
        """
        try:
            data = self.repository.get_data_by_id(id)
            if not data:
                
                raise HTTPException(status_code=404, detail=f"Data with id {id} not found")
            return DataDTO.model_validate(data)
        except HTTPException:
            raise
        except Exception as e:
            self.logger.error(f"Error retrieving data by id: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))
            
    def create_data(self, data: Data) -> Data:
        """
        Create a new data record in the system.

        This method validates the input DTO, creates a new Data entity,
        and persists it to the database.

        Args:
            data_dto (DataDTO): Data transfer object containing the new record information

        Returns:
            DataDTO: Created data record wrapped in a DTO

        Raises:
            HTTPException: 
                - 500: Database or server errors
                - 400: Validation errors
                - 409: Conflict with existing data

        Example:
            >>> new_data = DataDTO(name="test", data=[1, 2, 3], device_id=1 )
            >>> created = service.create_data(new_data)

        Note:
            Automatically generates timestamps and validates data constraints
        """
        try:
            # Calculate metrics
            avg_bf, avg_af = calculate_data_metrics(data.data)
            data.average_bf_normalization = float(avg_bf)
            data.average_af_normalization = float(avg_af)
            data.data_size = len(data.data)
            # Convert to DB model and save
            db_data = Data(**mapping_db_to_data(data).model_dump())
            data_created =self.repository.create_data(db_data)
            return data_created
        except Exception as e:
            self.logger.error(f"Error creating data: {str(e)}")
            raise HTTPException(status_code=500, detail="Could not create data")
            
    def update_data(self, id: int, data_dto: DataDTO) -> DataDTO:
        """
        Update an existing data record.

        This method validates the update data, finds the existing record,
        and applies the changes while maintaining data integrity.

        Args:
            id (int): Unique identifier of the record to update
            data_dto (DataDTO): DTO containing the updated information

        Returns:
            DataDTO: Updated data record wrapped in a DTO

        Raises:
            HTTPException: 
                - 404: Record not found
                - 500: Database or server errors
                - 400: Validation errors

        Example:
            >>> updated = service.update_data(1, updated_dto)
        """
        if not data_dto.name:
            raise HTTPException(status_code=400, detail="Name is required")
            
        try:
            self.db.begin_nested()
            existing_data = self.repository.get_data_by_id(id)
            if not existing_data:
                raise HTTPException(status_code=404, detail=f"Data with id {id} not found")
                
            for key, value in data_dto.model_dump(exclude={'id'}).items():
                setattr(existing_data, key, value)
                
            if not self._validate_data(existing_data):
                self.db.rollback()
                raise HTTPException(status_code=400, detail="Invalid update data")
                
            self.db.commit()
            return DataDTO.model_validate(existing_data)
        except HTTPException:
            raise
        except Exception as e:
            self.db.rollback()
            self.logger.error(f"Error updating data: {str(e)}")
            raise HTTPException(status_code=500, detail="Could not update data")
            
    def delete_data(self, id: int) -> DataDTO:
        """
        Delete a data record from the system.

        This method ensures safe deletion with proper cleanup and
        constraint checking.

        Args:
            id (int): Unique identifier of the record to delete

        Returns:
            DataDTO: The deleted record's information

        Raises:
            HTTPException: 
                - 404: Record not found
                - 500: Database or server errors
                - 409: Constraint violation

        Example:
            >>> deleted = service.delete_data(1)
        """
        try:
            self.db.begin_nested()
            data = self.repository.get_data_by_id(id)
            if not data:
                raise HTTPException(status_code=404, detail=f"Data with id {id} not found")
                
            if self._has_dependencies(data):
                self.db.rollback()
                raise HTTPException(status_code=400, detail="Cannot delete data with dependencies")
                
            deleted_data = self.repository.delete_data(data)
            self.db.commit()
            return DataDTO.model_validate(deleted_data)
        except HTTPException:
            raise
        except Exception as e:
            self.db.rollback()
            self.logger.error(f"Error deleting data: {str(e)}")
            raise HTTPException(status_code=500, detail="Could not delete data")


