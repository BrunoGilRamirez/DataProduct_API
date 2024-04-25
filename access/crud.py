from sqlalchemy.orm import Session
from .models import *
from .schemas import *

def get_keys_by_value(db: Session, value: str) -> Keys|bool:
    return db.query(Keys).filter(Keys.value == value).first()

    
def get_all_user_info(db: Session, user: UserCreate|None=None, secret: str|None=None) -> User|bool:
    if user is not None:
        user = db.query(Users).filter(Users.name == user.name, Users.email == user.email, Users.employer == user.employer).first()
    else:
        user = db.query(Users).filter(Users.secret == secret).first()
    employer = db.query(Companies).filter(Companies.id == user.employer).first()
    if user and employer:
        employer_schema = Company(id=employer.id,name=employer.name, phone_number=employer.phone_number, registry=str(employer.registry), email=employer.email)
        return User( id=user.id, name=user.name,role=user.role, email=user.email, employer=user.employer, secret=user.secret, companies=employer_schema, valid=user.valid)
    else:
        return False