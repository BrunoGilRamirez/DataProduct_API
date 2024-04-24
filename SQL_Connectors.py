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
    if os.environ.get("GCP_INSTANCE") is not None:
        instance_connection_name = os.environ["GCP_INSTANCE"]  # e.g. 'project:region:instance'
        db_user = os.environ["DB_USER"]  # e.g. 'my-db-user'
        db_pass = os.environ["DB_PASS"]  # e.g. 'my-db-password'
        db_name = os.environ[db_name]  # e.g. 'my-database'
        print(db_user)
        ip_type = IPTypes.PRIVATE if os.environ.get("PRIVATE_IP") else IPTypes.PUBLIC
        # initialize Cloud SQL Python Connector object
        connector = Connector()

        def getconn() -> pg8000.dbapi.Connection:
            conn: pg8000.dbapi.Connection = connector.connect(
                instance_connection_name,
                "pg8000",
                user=db_user,
                password=db_pass,
                db=db_name,
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
        print(f'Error loading credentials file.\n\nMake sure you have load the following variables:\nGCP_INSTANCE\nDB_USER\nDB_PASS\nDB_NAME\nPRIVATE_IP\n\nIn the same directory as the rest of files.')
        return None

def custom_connector(credentials: str='',db_name: str='') -> sqlalchemy.engine.base.Engine:
    '''This function returns a pool of connections created by create_engine.
    pool: sqlalchemy.engine.base.Engine'''
    if load_dotenv(credentials, override=True):
        db_user = os.environ["DB_USER"]  
        db_pass = os.environ["DB_PASS"]  # e.g. 'my-db-password'
        db_name = os.environ[db_name]  # e.g. 'my-database'
        db_host = os.environ["DB_HOST"]  # e.g. '
        db_port = os.environ["DB_PORT"]
        def getconn() -> pg8000.dbapi.Connection:
            conn: pg8000.dbapi.Connection = pg8000.connect(
                user=db_user,
                password=db_pass,
                database=db_name,
                host=db_host,
                port=db_port,
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
        print(f'Error loading credentials file.\n\nMake sure you have a .env file with the following variables:\nDB_USER\nDB_PASS\nDB_NAME\nDB_HOST\nDB_PORT\n\nIn the same directory as the rest of files.')
        return None