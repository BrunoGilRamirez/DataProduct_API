from .schemas import *
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException, status, Request
from .crud import *
from session_management import get_session
from fastapi.security import OAuth2PasswordBearer
from starlette.datastructures import MutableHeaders
from starlette.middleware.sessions import SessionMiddleware
import os

#------------------------------------- cryptography -------------------------------------
secret_key_ps = os.getenv('secret_key_ps')
ALGORITHM = os.getenv('ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES')
cookie_path= os.getenv('path_cookie')
scheme = os.getenv('cryp_scheme')
pwd_context = CryptContext(schemes=[scheme], deprecated="auto") # bcrypt is the hashing algorithm used to hash the password
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="key")

#------------------------------------- session -------------------------------------
session_root = get_session('.env', 'DB_NAME_token', remote_hosting=True)

#------------------------------------- database -------------------------------------
def get_db():
    db = session_root
    try:
        yield db #yield is used to create a generator function
    finally:
        db.close()

#------------------------------------- security ------------------------------------------
def generate_user_secret(name:str, role:str, email:str, employer:str, security:str):
    #generate a hash of the user data dictionary
    data = {'name':name, 'role':role, 'email':email, 'employer':employer, 'security':security}
    return pwd_context.hash(str(data))
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)
def get_password_hash(password):
    return pwd_context.hash(password)
def check_if_still_on_valid_time(valid_until: str)->bool:
    if datetime.now() < valid_until:
        return True
    else:
        return False

#------------------------------------- User utilities -------------------------------------
async def register_user(request: Request, session: Session = Depends(get_db)) -> bool|str:
    form_data = await request.form()
    username = form_data['name']
    role = form_data['role']
    email = form_data['email']
    employer = form_data['employer']
    security_word = form_data['security']
    password = get_password_hash(form_data['password'])
    employer_id = get_companies_by_name(session, employer)
    if not employer_id:
        create_company(session, CompanyCreate(name=employer, phone_number=0, registry=datetime.now().strftime('%Y-%m-%d'), email='not given'))
        employer_id = get_companies_by_name(session, employer)
    secret=generate_user_secret(username, role, email, employer, security_word)
    user = UserCreate(name=username, role=role, email=email, employer=employer_id, secret=secret)
    sec_word=SecurityWordCreate(owner=secret, word=security_word)
    
    if not user_exists(session, user):
        if create_user(session, user) and create_password(session, PasswordCreate(value=password, owner=user.secret)) and create_security_word(session, sec_word):
            return True
        else:
            return False
    else:
        return "User already exists"
def authenticate_user(session: Session, username: str, password: str)-> bool:
    user = get_user_by_email(session, username)
    if not user:
        return False
    if not verify_password(password, get_password_by_owner(session, user.secret).value):
        return False
    return user
async def get_current_user_API(token: str = Depends(oauth2_scheme), session: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token does not exist or is no longer valid",
        headers={"WWW-Authenticate": "Bearer"},
    )
    key = get_keys_by_value(session, token)
    try:
        print(key)
        if isinstance(key,Keys) and key.valid:
            if check_if_still_on_valid_time(key.valid_until) is False:
                raise credentials_exception
            else:
                user = decode_and_verify(key.owner, session)
                print(type(user))
                if isinstance(user, User):
                    return True #the user is authenticated
    except:
        raise credentials_exception
    

async def get_current_user(request: Request, session: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        token = await oauth2_scheme(request)
    except:
        raise credentials_exception
    try:
        key = get_keys_by_value(session, token)
    except:
        pass
    try:
        key = get_session_by_value(session, token)
    except:
        pass
    if key and key.valid and check_if_still_on_valid_time(key.valid_until):
        return decode_and_verify(key.owner, session)
    else:
        raise credentials_exception
    
def decode_and_verify(secret: str, db: Session):
    try:
        user= get_all_user_info(db, secret=secret)
        return user
    except JWTError:
        return False
def encrypt_data(data: dict, expires_delta: timedelta):
    expire = datetime.now(timezone.utc) + expires_delta
    data.update({"exp": expire})
    encoded = jwt.encode(data, secret_key_ps, algorithm=ALGORITHM)
    encrypted = pwd_context.hash(encoded)
    return encrypted, expire
#------------------------------------- token utilities -------------------------------------
def create_access_token(session: Session,data: dict, expires_delta: timedelta, request: Request=None) -> str:
    if request:
        meta=request.headers.items()
        meta.append(("client", str(request.client._asdict())))
    else:
        meta=None
    to_encode = data.copy()
    encoded_jwt, expire = encrypt_data(to_encode, expires_delta)
    Key_ = KeyCreate(value=encoded_jwt, 
                     valid_until=expire.strftime('%d/%m/%Y, %H:%M:%S'),
                     owner=data.get("sub"), 
                     registry=datetime.now().strftime('%d/%m/%Y, %H:%M:%S'),
                     valid=True, 
                     metadata_=str(meta)
                    )
    if create_key(session, Key_):
        return encoded_jwt
    else:
        return False
def validate_token(token: str|None, session: Session) -> bool:
    if isinstance(token, str):
        key = get_keys_by_value(session, token)
        if key:
            payload = jwt.decode(token, secret_key_ps, algorithms=[ALGORITHM])
            secret: str = payload.get("sub")
            user= get_all_user_info(session, secret=secret)
            return user
        else:
            return False
    else:
        return False
def request_add_token(request: Request, token: str):
    new_headers = MutableHeaders(request._headers)
    new_headers["Authorization"] = f"Bearer {token}"
    request._headers = new_headers
    request.scope.update(headers=request.headers.raw)
    return request
def request_remove_token(request: Request):
    new_headers = MutableHeaders(request._headers)
    new_headers.pop("Authorization")
    request._headers = new_headers
    request.scope.update(headers=request.headers.raw)
    return request
#------------------------------------- session utilities -------------------------------------
def validate_user_session(request: Request, db: Session) -> bool:
    token = request.session.get("access_token")
    if token:
        return get_session_by_value(db, token)
    else:
        return False
def delete_user_session(request: Request, db: Session) -> bool:
    token = request.session.get("access_token")
    if token:
        return delete_session(db, token)
    else:
        return False
#------------------------------------- validate token or session -------------------------------------
def validate_token_or_session(token: str, session: Session) -> bool|Keys:
    try:
        key = get_keys_by_value(session, token)
    except:
        pass
    try:
        key = get_session_by_value(session, token)
    except:
        pass
    if key and key.valid and check_if_still_on_valid_time(key.valid_until):
        return decode_and_verify(key.owner, session)