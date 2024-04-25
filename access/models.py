from typing import List

from sqlalchemy import BigInteger,Boolean, Column, Date, DateTime, ForeignKeyConstraint, Index, Integer, Numeric, PrimaryKeyConstraint, Text, Time, UniqueConstraint
from sqlalchemy.orm import Mapped, declarative_base, mapped_column, relationship
from sqlalchemy.orm.base import Mapped
from access import origin_models

class Companies(origin_models.companies):
    
    #------------------------------------- methods -------------------------------------
    def __repr__(self):
        return f'Company(id={self.id}, name={self.name}, phone_number={self.phone_number}, registry={self.registry}, email={self.email})'
    def __str__(self):
        return f'Company(id={self.id}, name={self.name}, phone_number={self.phone_number}, registry={self.registry}, email={self.email})'
    def to_dict(self):
        return {'id': self.id, 'name': self.name, 'phone_number': self.phone_number, 'registry': self.registry, 'email': self.email}

class SecurityWordCompanies(origin_models.securitywordcompanies):
    #------------------------------------- methods -------------------------------------
    def __repr__(self):
        return f'SecurityWordCompany(id={self.id}, word={self.word}, owner={self.owner})'
    def __str__(self):
        return f'SecurityWordCompany(id={self.id}, word={self.word}, owner={self.owner})'
    def to_dict(self):
        return {'id': self.id, 'word': self.word, 'owner': self.owner}

class Users(origin_models.users):
    #------------------------------------- methods -------------------------------------
    def __repr__(self):
        return f'User(id={self.id}, name={self.name}, role={self.role}, email={self.email}, employer={self.employer}, secret={self.secret})'
    def __str__(self):
        return f'User(id={self.id}, name={self.name}, role={self.role}, email={self.email}, employer={self.employer}, secret={self.secret})'
    def to_dict(self):
        return {'id': self.id, 'name': self.name, 'role': self.role, 'email': self.email, 'employer': self.employer, 'secret': self.secret}
    
class Codes(origin_models.codes):
    #------------------------------------- methods -------------------------------------
    def __repr__(self):
        return f'Code(id={self.id}, owner={self.owner}, value={self.value}, registry={self.registry}, valid_until={self.valid_until}, valid={self.valid})'
    def __str__(self):
        return f'Code(id={self.id}, owner={self.owner}, value={self.value}, registry={self.registry}, valid_until={self.valid_until}, valid={self.valid})'
    def to_dict(self):
        return {'id': self.id, 'owner': self.owner, 'value': self.value, 'registry': self.registry, 'valid_until': self.valid_until, 'valid': self.valid}

class Keys(origin_models.keys):
    #------------------------------------- methods -------------------------------------
    def __repr__(self):
        return f'Key(id={self.id}, owner={self.owner}, value={self.value}, registry={self.registry}, valid_until={self.valid_until}, valid={self.valid})'
    def __str__(self):
        return f'Key(id={self.id}, owner={self.owner}, value={self.value}, registry={self.registry}, valid_until={self.valid_until}, valid={self.valid})'
    def to_dict(self):
        return {'id': self.id, 'owner': self.owner, 'value': self.value, 'registry': self.registry, 'valid_until': self.valid_until, 'valid': self.valid}


class Passwords(origin_models.passwords):
    pass

class SecurityWords(origin_models.securitywords):
    pass
    

class Sessions(origin_models.sessions):
    pass


