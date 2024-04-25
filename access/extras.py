from .schemas import *
from jose import JWTError
from passlib.context import CryptContext
from datetime import datetime
from fastapi import Depends, HTTPException, status
from .crud import *
from session_management import get_session
from fastapi.security import OAuth2PasswordBearer
import os

#------------------------------------- cryptography -------------------------------------
session_root = get_session('.env', 'DB_NAME_token')
secret_key_ps = os.getenv('secret_key_ps')
ALGORITHM = os.getenv('ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES')
cookie_path= os.getenv('path_cookie')
scheme = os.getenv('cryp_scheme')
pwd_context = CryptContext(schemes=[scheme], deprecated="auto") # bcrypt is the hashing algorithm used to hash the password
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="key")

#------------------------------------- session -------------------------------------

#------------------------------------- database -------------------------------------
def get_db():
    db = session_root
    try:
        yield db #yield is used to create a generator function
    finally:
        db.close()

async def get_current_user_API(token: str = Depends(oauth2_scheme), session: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token does not exist or is no longer valid",
        headers={"WWW-Authenticate": "Bearer"},
    )
    key = get_keys_by_value(session, token)
    try:
        if isinstance(key,Keys) and key.valid:
            if check_if_still_on_valid_time(key.valid_until) is False:
                raise credentials_exception
            else:
                user = decode_and_verify(key.owner, session)
                if isinstance(user, User):
                    return True #the user is authenticated
    except Exception as e:
        print(f"\n\n\n\n\nerror: {e}\n\n\n\n\n")
        raise credentials_exception
     
def decode_and_verify(secret: str, db: Session):
    try:
        user= get_all_user_info(db, secret=secret)
        return user
    except Exception as e:
        print(f"\n\n\n\n\nerror: {e}\n\n\n\n\n")
        return False

def check_if_still_on_valid_time(valid_until: str)->bool:
    if datetime.now() < valid_until:
        return True
    else:
        return False