from SQL_Connectors import custom_connector, GCP_connector
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

def get_session(env: str='', db_name:str='DB_NAME',verbose=True, override=True, interpolate=True) -> sessionmaker|None:
    conection = None
    if os.getenv("GCP_INSTANCE") and os.getenv("GCP_INSTANCE") != '':
        conection = GCP_connector(credentials=env, db_name=db_name)
        print('GCP connection')
    elif load_dotenv(env, verbose=verbose, override=override, interpolate=interpolate):
        conection = custom_connector(credentials=env, db_name=db_name)
        print('Custom connection')
    Session = sessionmaker(bind=conection) if conection is not None else None
    try:
        session = Session()
        print(f'Session created: {db_name}')
    except Exception as e:
        print(f'\n\nError creating session: {e}\n\n')
        session = None
    return session