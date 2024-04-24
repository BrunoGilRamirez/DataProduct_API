from SQL_Connectors import custom_connector, GCP_connector
from sqlalchemy.orm import sessionmaker


def get_session(env: str='', db_name:str='DB_NAME', remote_hosting:bool=False) -> sessionmaker|None:
    if remote_hosting:
        conecction = GCP_connector(credentials=env, db_name=db_name)
    else:
        conecction = custom_connector(credentials=env, db_name=db_name)
    Session = sessionmaker(bind=conecction) # We create a sessionmaker for the remote database
    try:
        session = Session()
    except Exception as e:
        print(f'\n\nError creating session: {e}\n\n')
        session = None
    return session