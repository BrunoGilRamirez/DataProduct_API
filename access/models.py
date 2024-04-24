from typing import List

from sqlalchemy import BigInteger,Boolean, Column, Date, DateTime, ForeignKeyConstraint, Index, Integer, Numeric, PrimaryKeyConstraint, Text, Time, UniqueConstraint
from sqlalchemy.orm import Mapped, declarative_base, mapped_column, relationship
from sqlalchemy.orm.base import Mapped

Base = declarative_base()


class Companies(Base):
    __tablename__ = 'companies'
    __table_args__ = (
        PrimaryKeyConstraint('id', 'name', name='companies_pkey'),
        UniqueConstraint('id', name='unique_com_id'),
        {'schema': 'private'}
    )

    id = mapped_column(BigInteger, nullable=False)
    name = mapped_column(Text, nullable=False)
    phone_number = mapped_column(Numeric(10, 0), nullable=False)
    registry = mapped_column(Date, nullable=False)
    email = mapped_column(Text)

    users: Mapped[List['Users']] = relationship('Users', uselist=True, back_populates='companies')
    #------------------------------------- methods -------------------------------------
    def __repr__(self):
        return f'Company(id={self.id}, name={self.name}, phone_number={self.phone_number}, registry={self.registry}, email={self.email})'
    def __str__(self):
        return f'Company(id={self.id}, name={self.name}, phone_number={self.phone_number}, registry={self.registry}, email={self.email})'
    def to_dict(self):
        return {'id': self.id, 'name': self.name, 'phone_number': self.phone_number, 'registry': self.registry, 'email': self.email}

class SecurityWordCompanies(Companies):
    __tablename__ = 'security_word_companies'
    __table_args__ = (
        ForeignKeyConstraint(['owner'], ['private.companies.id'], ondelete='CASCADE', onupdate='CASCADE', name='owner'),
        PrimaryKeyConstraint('owner', name='security_word_companies_pkey'),
        UniqueConstraint('owner', name='Unq_owner'),
        {'schema': 'private'}
    )

    owner = mapped_column(Integer)
    value = mapped_column(Text, nullable=False)

class Users(Base):
    __tablename__ = 'users'
    __table_args__ = (
        ForeignKeyConstraint(['employer'], ['private.companies.id'], name='employer_fk'),
        PrimaryKeyConstraint('id', 'email', 'secret', name='users_pkey'),
        UniqueConstraint('email', name='email_unique'),
        UniqueConstraint('id', name='id_unique'),
        UniqueConstraint('secret', name='secret_unique'),
        Index('fki_employer_fk', 'employer'),
        {'schema': 'private'}
    )

    id = mapped_column(Integer, nullable=False)
    name = mapped_column(Text, nullable=False)
    role = mapped_column(Text, nullable=False)
    email = mapped_column(Text, nullable=False)
    employer = mapped_column(Integer, nullable=False)
    secret = mapped_column(Text, nullable=False)

    companies: Mapped['Companies'] = relationship('Companies', back_populates='users')
    keys: Mapped[List['Keys']] = relationship('Keys', uselist=True, back_populates='users')
    passwords: Mapped['Passwords'] = relationship('Passwords', uselist=False, back_populates='users')
    security_words: Mapped[List['SecurityWords']] = relationship('SecurityWords', uselist=True, back_populates='users')
    sessions: Mapped[List['Sessions']] = relationship('Sessions', uselist=True, back_populates='users')
    #------------------------------------- methods -------------------------------------
    def __repr__(self):
        return f'User(id={self.id}, name={self.name}, role={self.role}, email={self.email}, employer={self.employer}, secret={self.secret})'
    def __str__(self):
        return f'User(id={self.id}, name={self.name}, role={self.role}, email={self.email}, employer={self.employer}, secret={self.secret})'
    def to_dict(self):
        return {'id': self.id, 'name': self.name, 'role': self.role, 'email': self.email, 'employer': self.employer, 'secret': self.secret}
    
class Keys(Base):
    __tablename__ = 'keys'
    __table_args__ = (
        ForeignKeyConstraint(['owner'], ['private.users.secret'], ondelete='CASCADE', onupdate='CASCADE', name='owner'),
        PrimaryKeyConstraint('id', name='keys_pkey'),
        Index('fki_owner', 'owner'),
        {'schema': 'private'}
    )

    id = mapped_column(BigInteger)
    value = mapped_column(Text, nullable=False)
    valid_until = mapped_column(DateTime, nullable=False)
    owner = mapped_column(Text, nullable=False)
    registry = mapped_column(DateTime, nullable=False)
    valid = mapped_column(Boolean, nullable=False)
    metadata_ = mapped_column('metadata', Text)

    users: Mapped['Users'] = relationship('Users', back_populates='keys')    #------------------------------------- methods -------------------------------------
    def __repr__(self):
        return f'Key(id={self.id}, owner={self.owner}, value={self.value}, registry={self.registry}, valid_until={self.valid_until}, valid={self.valid})'
    def __str__(self):
        return f'Key(id={self.id}, owner={self.owner}, value={self.value}, registry={self.registry}, valid_until={self.valid_until}, valid={self.valid})'
    def to_dict(self):
        return {'id': self.id, 'owner': self.owner, 'value': self.value, 'registry': self.registry, 'valid_until': self.valid_until, 'valid': self.valid}


class Passwords(Base):
    __tablename__ = 'passwords'
    __table_args__ = (
        ForeignKeyConstraint(['owner'], ['private.users.secret'], ondelete='CASCADE', onupdate='CASCADE', name='owner_fk'),
        PrimaryKeyConstraint('id', 'owner', name='passwords_pkey'),
        UniqueConstraint('id', name='id_u'),
        UniqueConstraint('owner', name='owner_unique'),
        {'schema': 'private'}
    )

    value = mapped_column(Text, nullable=False)
    id = mapped_column(Integer, nullable=False)
    owner = mapped_column(Text, nullable=False)

    users: Mapped['Users'] = relationship('Users', back_populates='passwords')

class SecurityWords(Base):
    __tablename__ = 'security_words'
    __table_args__ = (
        ForeignKeyConstraint(['owner'], ['private.users.secret'], ondelete='CASCADE', onupdate='CASCADE', name='owner_fkey'),
        PrimaryKeyConstraint('id', name='security_words_pkey'),
        Index('fki_owner_fkey', 'owner'),
        {'schema': 'private'}
    )

    word = mapped_column(Text, nullable=False)
    owner = mapped_column(Text, nullable=False)
    id = mapped_column(Integer)

    users: Mapped['Users'] = relationship('Users', back_populates='security_words')

class Sessions(Base):
    __tablename__ = 'sessions'
    __table_args__ = (
        ForeignKeyConstraint(['owner'], ['private.users.secret'], ondelete='CASCADE', onupdate='CASCADE', name='owner'),
        PrimaryKeyConstraint('id', name='sessions_pkey'),
        {'schema': 'private'}
    )

    id = mapped_column(BigInteger)
    owner = mapped_column(Text, nullable=False)
    registry = mapped_column(DateTime, nullable=False)
    valid_until = mapped_column(DateTime, nullable=False)
    valid = mapped_column(Boolean, nullable=False)
    metadata_ = mapped_column('metadata', Text, nullable=False)
    value = mapped_column(Text, nullable=False)

    users: Mapped['Users'] = relationship('Users', back_populates='sessions')