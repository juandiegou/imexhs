import pandas as pd
import numpy as np
import os
import psycopg2
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from ..models.data import DataDB as Data
from typing import Optional, List

from ..config.bd_conection import get_db_connection, create_db
from ..utils.logger import setup_logger

class DataRepository:
    """
    A repository class for managing data operations with a database.
    This class provides methods for CRUD operations (Create, Read, Update, Delete)
    and statistical analysis of data stored in a database.
    Attributes:
        db (Session | None): SQLAlchemy database session instance.
    Methods:
        get_data(name: Optional[str], limit: int, start: int) -> List[Data]
            Retrieves data from database with optional filtering by name.
        get_data_by_id(id: int) -> Data
            Retrieves a single data entry by its ID.
        create_data(data: Data) -> Data
            Creates a new data entry in the database.
        update_data(data: Data) -> Data
            Updates an existing data entry in the database.
        delete_data(data: Data) -> Data
            Deletes a data entry from the database.
        delete_data_by_id(id: int) -> Data
            Deletes a data entry by its ID.
        delete_data_by_name(name: str) -> Data
            Deletes data entries by name.
        get_data_size(name: str) -> int
            Returns the size of data entries for a given name.
        get_data_average(name: str) -> float
            Calculates the average of data entries.
        get_data_std(name: str) -> float
            Calculates the standard deviation of data entries.
        get_data_max(name: str) -> float
            Returns the maximum value in data entries.
        get_data_min(name: str) -> float
            Returns the minimum value in data entries.
        get_data_sum(name: str) -> float
            Calculates the sum of data entries.
        get_data_count(name: str) -> int
            Counts the number of data entries.
        get_data_describe(name: str) -> pd.DataFrame
            Generates descriptive statistics of data entries.
        get_data_info(name: str) -> pd.DataFrame
            Returns information about the data entries.
        get_data_hist(name: str) -> pd.DataFrame
            Generates a histogram of data entries.
        get_data_boxplot(name: str) -> pd.DataFrame
            Generates a box plot of data entries.
        get_data_scatter(name: str) -> pd.DataFrame
            Generates a scatter plot of data entries.
        get_data_correlation(name: str) -> pd.DataFrame
            Calculates correlation matrix of data entries.
        get_data_covariance(name: str) -> pd.DataFrame
            Calculates covariance matrix of data entries.
        get_data_skew(name: str) -> pd.DataFrame
            Calculates skewness of data entries.
    Dependencies:
        - SQLAlchemy
        - pandas
        - numpy
    Note:
        This class requires a properly configured database session to be set
        before using any of its methods.
    """
    
    # data repository object
    
    db : Session  | None = None
    
    def __init__(self):
        """
        Initialize DataRepository class.
        This constructor initializes a new instance of DataRepository with a database connection.
        Attributes:
            db: Database connection instance shared across all DataRepository objects
        """
        
        self.logger = setup_logger('data_repository')
        try:
            create_db()
            self.db = get_db_connection()
        except UnicodeDecodeError as e:
            self.logger.error(f"Error connecting to database: {str(e)}")
            raise Exception("Error connecting to database")

        
    def get_data(self, name: Optional[str] = None, limit: int = 100, start: int = 0) -> List[Data]:
        """
        Retrieves data records from the database with optional filtering by name.

        Args:
            name (Optional[str]): Name to filter data records by. If None, returns all records.
            limit (int): Maximum number of records to return. Defaults to 100.
            start (int): Starting offset for pagination. Defaults to 0.

        Returns:
            List[Data]: List of Data objects matching the query criteria.

        Example:
            >>> repo.get_data(name="test", limit=10, start=0) 
            [<Data object>, <Data object>, ...]
        """
        try:
            self.logger.info(f"Fetching data with name={name}, limit={limit}, start={start}")
            # get data from database
            if name:
                return self.db.query(Data).filter(Data.name == name).limit(limit).offset(start).all()
            return self.db.query(Data).limit(limit).offset(start).all()
        except SQLAlchemyError as e:
            self.logger.error(f"Database error while fetching data: {str(e)}")
            raise
    
    def get_data_by_id(self, id: str) -> Data:
        """
        Retrieves a Data object from the database by its ID.

        Args:
            id (str): The unique identifier of the Data object to retrieve.

        Returns:
            Data: The Data object with the specified ID if found, None otherwise.
        """
        # get data by id
        return self.db.query(Data).filter(Data.id == id).first()
    
    def create_data(self, data: Data) -> Data:
        """
        Create a new Data entry in the database.

        Args:
            data (Data): The Data object to be created and stored in the database.

        Returns:
            Data: The created Data object with updated information after being committed to the database.

        Example:
            >>> data = Data(name="example", value=123)
            >>> created_data = repository.create_data(data)
        """
        try:
            self.logger.info(f"Creating new data: {data}")
            # create data
            self.db.add(data)
            self.db.commit()
            self.db.refresh(data)
            return data
        except SQLAlchemyError as e:
            self.logger.error(f"Error creating data: {str(e)}")
            self.db.rollback()
            raise
    
    def update_data(self, data: Data) -> Data:
        """Updates data in the database.

        This method adds or updates a Data object in the database, commits the transaction,
        and refreshes the instance to ensure it contains any new database-generated values.

        Args:
            data (Data): The Data object to be updated in the database.

        Returns:
            Data: The updated Data object with refreshed values from the database.
        """
        try:
            self.logger.info(f"Updating data with id={data.id}")
            # update data
            self.db.add(data)
            self.db.commit()
            self.db.refresh(data)
            return data
        except SQLAlchemyError as e:
            self.logger.error(f"Error updating data: {str(e)}")
            self.db.rollback()
            raise
    
    def delete_data(self, data: Data) -> Data:
        """Delete data from the database.

        Args:
            data (Data): The data object to be deleted from the database.

        Returns:
            Data: The deleted data object.

        Example:
            >>> data_repo = DataRepository()
            >>> data = Data(id=1, name="test")
            >>> deleted_data = data_repo.delete_data(data)
        """
        try:
            
            self.logger.info(f"Deleting data: {data}")
            # delete data
            self.db.delete(data)
            self.db.commit()
            return data
        except SQLAlchemyError as e:
            self.logger.error(f"Error deleting data: {str(e)}")
            self.db.rollback()
            raise
    
    def delete_data_by_id(self, id: int) -> Data:
        """
        Delete data record by its ID.

        Args:
            id (int): Unique identifier of the data record to be deleted.

        Returns:
            Data: The deleted data object if found and successfully deleted.
            None: If no data record exists with the given ID.

        Raises:
            None
        """
        # delete data by id
        data = self.get_data_by_id(id)
        if data:
            return self.delete_data(data)
        return None
    
    def delete_data_by_name(self, name: str) -> Data:
        """
        Delete data by name from the repository.

        Args:
            name (str): The name identifier of the data to be deleted.

        Returns:
            Data: The deleted data object if found and deleted successfully.
            None: If no data was found with the given name.

        Example:
            >>> repo.delete_data_by_name("example_data")
            <Data object>
        """
        # delete data by name
        data = self.get_data(name)
        if data:
            return self.delete_data(data)
        return None
    
    def get_data_size(self, name: str) -> int:
        """
        Get the total number of records for a given name.

        Args:
            name (str): The name to filter the data by.

        Returns:
            int: The total count of records matching the name.
        """
        data = self.get_data(name)
        return len(data)
    
    def get_data_average(self, name: str) -> float:
        """
        Calculate the arithmetic mean of numeric values for records with the given name.

        Args:
            name (str): The name to filter the data by.

        Returns:
            float: The average/mean value of the data.
        """
        data = self.get_data(name)
        return np.mean(data)
    
    def get_data_std(self, name: str) -> float:
        """
        Calculate the standard deviation of numeric values for records with the given name.

        Args:
            name (str): The name to filter the data by.

        Returns:
            float: The standard deviation of the data.
        """
        data = self.get_data(name)
        return np.std(data)
    
    def get_data_max(self, name: str) -> float:
        """
        Find the maximum numeric value among records with the given name.

        Args:
            name (str): The name to filter the data by.

        Returns:
            float: The maximum value in the data.
        """
        data = self.get_data(name)
        return np.max(data)
    
    def get_data_min(self, name: str) -> float:
        """
        Find the minimum numeric value among records with the given name.

        Args:
            name (str): The name to filter the data by.

        Returns:
            float: The minimum value in the data.
        """
        data = self.get_data(name)
        return np.min(data)
    
    def get_data_sum(self, name: str) -> float:
        """
        Calculate the sum of numeric values for records with the given name.

        Args:
            name (str): The name to filter the data by.

        Returns:
            float: The sum of all values in the data.
        """
        data = self.get_data(name)
        return np.sum(data)
    
    def get_data_count(self, name: str) -> int:
        """
        Count the number of records with the given name.

        Args:
            name (str): The name to filter the data by.

        Returns:
            int: The count of records matching the name.
        """
        data = self.get_data(name)
        return len(data)
    
    def get_data_describe(self, name: str) -> pd.DataFrame:
        """
        Generate descriptive statistics for records with the given name.
        
        Includes count, mean, std, min, 25%, 50%, 75%, max.

        Args:
            name (str): The name to filter the data by.

        Returns:
            pd.DataFrame: A DataFrame containing the descriptive statistics.
        """
        data = self.get_data(name)
        return pd.DataFrame(data).describe()
    
    def get_data_info(self, name: str) -> pd.DataFrame:
        """
        Get information about the data structure for records with the given name.
        
        Includes data types, non-null count, and memory usage.

        Args:
            name (str): The name to filter the data by.

        Returns:
            pd.DataFrame: A DataFrame containing the data information.
        """
        data = self.get_data(name)
        return pd.DataFrame(data).info()
    
    def get_data_hist(self, name: str) -> pd.DataFrame:
        """
        Generate histogram plot data for records with the given name.

        Args:
            name (str): The name to filter the data by.

        Returns:
            pd.DataFrame: A DataFrame containing the histogram data.
        """
        data = self.get_data(name)
        return pd.DataFrame(data).hist()
    
    def get_data_boxplot(self, name: str) -> pd.DataFrame:
        """
        Generate box plot data for records with the given name.
        
        Shows quartiles, median, and potential outliers.

        Args:
            name (str): The name to filter the data by.

        Returns:
            pd.DataFrame: A DataFrame containing the box plot data.
        """
        data = self.get_data(name)
        return pd.DataFrame(data).boxplot()
    
    def get_data_scatter(self, name: str) -> pd.DataFrame:
        """
        Generate scatter plot data for records with the given name.

        Args:
            name (str): The name to filter the data by.

        Returns:
            pd.DataFrame: A DataFrame containing the scatter plot data.
        """
        data = self.get_data(name)
        return pd.DataFrame(data).scatter()
    
    def get_data_correlation(self, name: str) -> pd.DataFrame:
        """
        Calculate correlation matrix for numeric columns in records with the given name.

        Args:
            name (str): The name to filter the data by.

        Returns:
            pd.DataFrame: A DataFrame containing the correlation matrix.
        """
        data = self.get_data(name)
        return pd.DataFrame(data).corr()
    
    def get_data_covariance(self, name: str) -> pd.DataFrame:
        """
        Calculate covariance matrix for numeric columns in records with the given name.

        Args:
            name (str): The name to filter the data by.

        Returns:
            pd.DataFrame: A DataFrame containing the covariance matrix.
        """
        data = self.get_data(name)
        return pd.DataFrame(data).cov()
    
    def get_data_skew(self, name: str) -> pd.DataFrame:
        """
        Calculate skewness for numeric columns in records with the given name.
        
        Measures the asymmetry of the probability distribution.

        Args:
            name (str): The name to filter the data by.

        Returns:
            pd.DataFrame: A DataFrame containing the skewness values.
        """
        data = self.get_data(name)
        return pd.DataFrame(data).skew()
