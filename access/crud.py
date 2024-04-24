from sqlalchemy.orm import Session
from .models import *
from .schemas import *
from pydantic import ValidationError
#------------------- Companies -------------------
def create_company(db: Session, company: CompanyCreate) -> Companies|bool:
    try:
        new_company = Companies(**company.model_dump())
        db.add(new_company)
        db.commit()
        return new_company
    except Exception as e:
        db.rollback()
        return False
def get_company(db: Session, company_id: int):
    return db.query(Companies).filter(Companies.id == company_id).first()
def get_companies(db: Session):
    return db.query(Companies).all()
def get_companies_by_name(db: Session, name: str):
    companies = db.query(Companies).filter(Companies.name == name).first()
    if companies:
        return companies.id
    else:
        return False
def update_company(db: Session, company_id: int, company: CompanyCreate) -> Companies|bool:
    try:
        db.query(Companies).filter(Companies.id == company_id).update(company.model_dump())
        db.commit()
        return get_company(db, company_id)
    except Exception as e:
        db.rollback()
        return False
def delete_company(db: Session, company_id: int) -> bool:
    try:
        company = get_company(db, company_id)
        db.delete(company)
        db.commit()
        return True
    except Exception as e:
        db.rollback()
        return False
def user_exists(db: Session, user: UserCreate) -> bool:
    user = db.query(Users).filter(Users.name == user.name, Users.email == user.email, Users.employer == user.employer).first()
    if user:
        return True
    else:
        return False
#------------------- Users -------------------
def create_user(db: Session, user: UserCreate) -> bool:
    new_user = Users(**user.model_dump())
    try:
        db.add(new_user)
        db.commit()
        #db.refresh(new_user)
        return True
    except Exception as e:
        db.rollback()
        return False
def get_user_by_user(db: Session, user: UserCreate) -> Users|bool:
    user = db.query(Users).filter(Users.name == user.name, Users.email == user.email, Users.employer == user.employer).first()
    if user:
        return user
    else:
        return False         
def get_user_by_secret(db: Session, secret: str) -> Users|bool:
    user = db.query(Users).filter(Users.secret == secret).first()
    if user:
        return user
    else:
        return False
def get_user_by_email(db: Session, email: str) -> Users|bool:
    user = db.query(Users).filter(Users.email == email).first()
    if user:
        return user
    else:
        return False
def get_all_user_info(db: Session, user: UserCreate|None=None, secret: str|None=None) -> User|bool:
    if user is not None:
        user = db.query(Users).filter(Users.name == user.name, Users.email == user.email, Users.employer == user.employer).first()
    else:
        user = db.query(Users).filter(Users.secret == secret).first()
        id= user.id
    employer = db.query(Companies).filter(Companies.id == user.employer).first()
    if user and employer:
        employer_schema = Company(id=employer.id,name=employer.name, phone_number=employer.phone_number, registry=str(employer.registry), email=employer.email)
        return User( id=user.id, name=user.name,role=user.role, email=user.email, employer=user.employer, secret=user.secret, companies=employer_schema)
        
    else:
        return False

def update_user(db: Session, user_id: int, user: UserCreate)-> Users|bool:
    try:
        db.query(Users).filter(Users.id == user_id).update(user.model_dump())
        db.commit()
        return get_user_by_email(db, user.email)
    except Exception as e:
        db.rollback()
        return False
def delete_user(db: Session, user_id: int):
    try:
        user = (db, user_id)
        db.delete(user)
        db.commit()
        return user
    except Exception as e:
        db.rollback()
        return False

#------------------- Keys -------------------
def create_key(db: Session, key: KeyCreate) -> bool:
    new_key = Keys(**key.model_dump())
    db.add(new_key)
    try:
        db.commit()
        #db.refresh(new_key)
        return True
    except Exception as e:
        db.rollback()
        return False
def get_keys_by_owner(db: Session, owner: str) -> Keys|bool:
    return db.query(Keys).filter(Keys.owner == owner).all()
def get_keys_by_value(db: Session, value: str) -> Keys|bool:
    return db.query(Keys).filter(Keys.value == value).first()
def get_key(db: Session, key_id: int):
    return db.query(Keys).filter(Keys.id == key_id).first()
def get_keys(db: Session):
    return db.query(Keys).all()
def update_key(db: Session, key_id: int, key: KeyCreate):
    try:
        db.query(Keys).filter(Keys.id == key_id).update(key.model_dump())
        db.commit()
        return get_key(db, key_id)
    except Exception as e:
        db.rollback()
        return False
def delete_key(db: Session, key_id: int):
    key = get_key(db, key_id)
    try:
        db.delete(key)
        db.commit()
        return True
    except Exception as e:
        db.rollback()
        return False

#------------------- Passwords -------------------
def create_password(db: Session, password: PasswordCreate) -> bool:
    new_password = Passwords(**password.model_dump())
    try:
        db.add(new_password)
        db.commit()
        return True if get_password_by_owner(db, password.owner) else False
    except:
        db.rollback()
        return False
def update_password(db: Session, password_id: int, password: PasswordCreate):
    try:
        db.query(Passwords).filter(Passwords.id == password_id).update(password.model_dump())
        db.commit()
        return True
    except Exception as e:
        db.rollback()
        return False
def get_password_by_owner(db: Session, owner: str) -> Passwords|bool:
    password = db.query(Passwords).filter(Passwords.owner == owner).first()
    if password:
        return password
    else:
        return False
def get_password_by_id(db: Session, password_id: int):
    return db.query(Passwords).filter(Passwords.id == password_id).first()

#------------------- SecurityWords -------------------
def create_security_word(db: Session, security_word: SecurityWordCreate) -> bool:
    new_security_word = SecurityWords(**security_word.model_dump())
    try:
        db.add(new_security_word)
        db.commit()
        return True
    except Exception as e:
        print(f"\n\n\n{e}\n\n\n")
        db.rollback()
        return False
def get_security_word_by_owner(db: Session, owner: str) -> SecurityWords|bool:
    security_word = db.query(SecurityWords).filter(SecurityWords.owner == owner).first()
    if security_word:
        return security_word
    else:
        return False

def update_security_word(db: Session, owner: str, security_word: SecurityWordCreate) -> SecurityWords|bool:
    try:
        db.query(SecurityWords).filter(SecurityWords.owner == owner).update(security_word.model_dump())
        db.commit()
        return get_security_word_by_owner(db, owner)
    except Exception as e:
        db.rollback()
        return False
#------------------- Sessions -------------------
def create_session(db: Session, session: SessionCreate) -> bool:
    new_session = Sessions(**session.model_dump())
    try:
        db.add(new_session)
        db.commit()
        return True
    except Exception as e:
        db.rollback()
        return False
def get_sessions_by_owner(db: Session, owner: str) -> Sessions|bool:
    session = db.query(Sessions).filter(Sessions.owner == owner)
    if session:
        return session
    else:
        return False
def get_session_by_value(db: Session, value: str) -> Sessions|bool:
    session = db.query(Sessions).filter(Sessions.value == value).first()
    if session:
        return session
    else:
        return False
def delete_session(db: Session, value: str):
    try:
        session = get_session_by_value(db, value)
        db.delete(session)
        db.commit()
        return True
    except Exception as e:
        db.rollback()
        return False
    
