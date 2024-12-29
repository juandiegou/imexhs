#an class with database possgres connection

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.orm import registry
from dotenv import load_dotenv
import logging
from datetime import datetime  
import os

log_dir = "logs"
if not os.path.exists(log_dir):
    os.makedirs(log_dir)
 
__name__ = "bd_conection"   
# Create logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

    
# Create formatter
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


# File handler
today = datetime.now().strftime('%Y-%m-%d')
file_handler = logging.FileHandler(f"{log_dir}/{__name__}_{today}.log")
file_handler.setFormatter(formatter)

# Add handler if it doesn't exist
if not logger.handlers:
    logger.addHandler(file_handler)

mapper_registry = registry()
Entity = mapper_registry.generate_base()

load_dotenv()

from os import environ as env

# Database URL
DATABASE_URL = f"postgresql://{env.get('DATABASE_USERNAME')}:{env.get('DATABASE_PASSWORD')}@{env.get('DATABASE_HOSTNAME', 'localhost')}:{env.get('DATABASE_PORT', '5432')}/{env.get('DATABASE_NAME')}"

# Create Database Engine
Engine = create_engine(
    DATABASE_URL,
    echo=env.get('DEBUG_MODE', 'false').lower() == 'true',
    future=True,
    pool_size=5,
    max_overflow=10,
    pool_timeout=30,
    pool_recycle=1800,
    pool_pre_ping=True
)

SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=Engine
)


def get_db_connection():
    db = scoped_session(SessionLocal)
    try:
        logger.info("Database connection established")
        return db
    finally:
        db.close()
        
def create_db():
    try:
        with Engine.begin() as connection:
            Entity.metadata.create_all(connection)
        logger.info("Database created")
        logger.info("Database tables created")
    except Exception as e:
        logger.error(f"Error creating database: {str(e)}")
        raise Exception(f"Error creating database: {str(e)}")
    

    