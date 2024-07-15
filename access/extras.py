from .schemas import *
from jose import JWTError
from passlib.context import CryptContext
from datetime import datetime
from fastapi import Depends, HTTPException, status, Request
from .crud import *
from starlette.datastructures import MutableHeaders
from session_management import get_session
from fastapi.security import OAuth2PasswordBearer
import traceback
import os
from sqlalchemy import exc

#------------------------------------- cryptography -------------------------------------
session_root = get_session('.env', 'DB_NAME_token')
secret_key_ps = os.getenv('secret_key_ps')
ALGORITHM = os.getenv('ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES')
cookie_path= os.getenv('path_cookie')
scheme = os.getenv('cryp_scheme')
pwd_context = CryptContext(schemes=[scheme], deprecated="auto") # bcrypt is the hashing algorithm used to hash the password
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="key",auto_error=False)

#------------------------------------- session -------------------------------------

#------------------------------------- database -------------------------------------
def get_db():
    db = session_root
    try:
        yield db #yield is used to create a generator function
    except exc.SQLAlchemyError:
        traceback.print_exc()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="The database is offline, for maintenance purposes.")
    except Exception:
        traceback.print_exc()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="The database is offline, for maintenance purposes.")
    finally:
        db.close()

async def get_current_user_API(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db), raise_exception: bool = True)->bool|HTTPException:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token does not exist or is no longer valid",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    if isinstance(token, str):
        key = get_keys_by_value(db, token)
    try:
        if isinstance(key,Keys) and key.valid:
            if check_if_still_on_valid_time(key.valid_until):
                return True #the user is authenticated
    except Exception :
        traceback.print_exc()
        
    if raise_exception: 
            raise credentials_exception
    else:
        return False
    
async def get_current_user_view(request:Request, session: Session = Depends(get_db), raise_exception: bool = True)->bool|HTTPException:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token does not exist or is no longer valid",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token = await oauth2_scheme(request)
    
    if token is None:
        if raise_exception: 
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not authenticated",
                headers={"WWW-Authenticate": "Bearer"},
            )
    elif isinstance(token, str):
        key = get_keys_by_value(session, token)
    try:
        if isinstance(key,Keys) and key.valid:
            if check_if_still_on_valid_time(key.valid_until):
                return True #the user is authenticated
    except Exception :
        traceback.print_exc()
        
    if raise_exception: 
            raise credentials_exception
    else:
        return False
     
def decode_and_verify(secret: str, db: Session) -> User|bool:
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

def request_add_token(request: Request, token: str)->Request:
    new_headers = MutableHeaders(request._headers)
    new_headers["Authorization"] = f"Bearer {token}"
    request._headers = new_headers
    request.scope.update(headers=request.headers.raw)
    return request