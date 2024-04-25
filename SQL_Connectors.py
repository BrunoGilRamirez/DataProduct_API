import os
from dotenv import load_dotenv
from google.cloud.sql.connector import Connector, IPTypes
import pg8000
import sqlalchemy


def GCP_connector(credentials: str='',db_name: str='') -> sqlalchemy.engine.base.Engine:
    """
    Initializes a connection pool for a Cloud SQL instance of Postgres.
    Uses the Cloud SQL Python Connector package.
    Returns a SQLAlchemy engine object.
    pool: sqlalchemy.engine.base.Engine
    """
    credentials = {
        "DB_USER": os.environ.get("DB_USER"),
        "DB_PASS": os.environ.get("DB_PASS"),
        "DB_NAME": os.environ.get(db_name),
        "GCP_INSTANCE": os.environ.get("GCP_INSTANCE"),
    }
    missing = check_credentials(credentials)
    if missing == []:
        
        ip_type = IPTypes.PRIVATE if os.environ.get("PRIVATE_IP") else IPTypes.PUBLIC
        # initialize Cloud SQL Python Connector object
        connector = Connector()

        def getconn() -> pg8000.dbapi.Connection:
            conn: pg8000.dbapi.Connection = connector.connect(
                credentials["GCP_INSTANCE"],
                "pg8000",
                user=credentials["DB_USER"],
                password=credentials["DB_PASS"],
                db=credentials["DB_NAME"],
                ip_type=ip_type,
            )
            return conn # pg8000 will handle closing the connection for us when we are done

        pool = sqlalchemy.create_engine(
            "postgresql+pg8000://", # The connection string for the database, "{'postgresql'}+pg8000://" is the driver for the connection, and the rest of the string is the connection parameters.
            creator=getconn, # The function that will create the connections.
            pool_size=5,# sets the number of connections that the engine will maintain at once.
            max_overflow=2,# The total number of concurrent connections for your application will be a total of pool_size and max_overflow.
            pool_timeout=30,  # is the maximum number of seconds to wait when retrieving a new connection from the pool. After the specified amount of time, an exception will be thrown.
            pool_recycle=1800,  # 'pool_recycle' is the maximum number of seconds a connection can persist. Connections that live longer than the specified amount of time will be reestablished to ensure that they remain fresh.
        )
        return pool # SQLAlchemy engine object.
    else:
        print(f"Error loading remote credentials file.\n\nMake sure you have a .env file with the following variables:{missing}\n\nIn the same directory as the rest of files.")
        return None

def custom_connector(credentials: str='',db_name: str='') -> sqlalchemy.engine.base.Engine:
    '''This function returns a pool of connections created by create_engine.
    pool: sqlalchemy.engine.base.Engine'''
    credentials = {
        "DB_USER": os.environ.get("DB_USER"),
        "DB_PASS": os.environ.get("DB_PASS"),
        "DB_NAME": os.environ.get(db_name),
        "DB_HOST": os.environ.get("DB_HOST"),
        "DB_PORT": os.environ.get("DB_PORT"),
    }
    missing = check_credentials(credentials)
    if missing == []:
        def getconn() -> pg8000.dbapi.Connection:
            conn: pg8000.dbapi.Connection = pg8000.connect(
                user=credentials["DB_USER"],
                password=credentials["DB_PASS"],
                database=credentials["DB_NAME"],
                host=credentials["DB_HOST"],
                port=credentials["DB_PORT"],
            )
            return conn # pg8000 will handle closing the connection for us when we are done
        pool = sqlalchemy.create_engine(
            "postgresql+pg8000://", # The connection string for the database, "{'postgresql'}+pg8000://" is the driver for the connection, and the rest of the string is the connection parameters.
            creator=getconn, # The function that will create the connections
            pool_size=5, # sets the number of connections that the engine will maintain at once.
            max_overflow=2, # The total number of concurrent connections for your application will be a total of pool_size and max_overflow.
            pool_timeout=30,  # sets the number of seconds to wait when retrieving a new connection from the pool. After the specified amount of time, an exception will be thrown.
            pool_recycle=1800,  # 'pool_recycle' is the maximum number of seconds a connection can persist. Connections that live longer than the specified amount of time will be reestablished to ensure that they remain fresh.
        )
        return pool # SQLAlchemy engine object.
    else:
        print(f"Error loading local credentials file.\n\nMake sure you have a .env file with the following variables:{missing}\n\nIn the same directory as the rest of files.")
        return None

def check_credentials(credentials: dict) -> list:
    '''This function checks if the credentials are valid.
    credentials: dict'''
    missing = []
    for key in list(credentials.keys()):
        if credentials[key]=="" or credentials[key]==None:
            missing.append(key)
    return missing