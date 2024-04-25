from typing import List

from sqlalchemy import BigInteger, Boolean, Column, Date, DateTime, ForeignKeyConstraint, Index, Integer, Numeric, PrimaryKeyConstraint, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, declarative_base, mapped_column, relationship
from sqlalchemy.orm.base import Mapped

Base = declarative_base()


class companies(Base):
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

    users: Mapped[List['users']] = relationship('Users', uselist=True, back_populates='companies')


class securitywordcompanies(companies):
    __tablename__ = 'security_word_companies'
    __table_args__ = (
        ForeignKeyConstraint(['owner'], ['private.companies.id'], ondelete='CASCADE', onupdate='CASCADE', name='owner'),
        PrimaryKeyConstraint('owner', name='security_word_companies_pkey'),
        UniqueConstraint('owner', name='Unq_owner'),
        {'schema': 'private'}
    )

    owner = mapped_column(Integer)
    value = mapped_column(Text, nullable=False)


class users(Base):
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
    valid = mapped_column(Boolean, nullable=False)

    companies: Mapped['companies'] = relationship('Companies', back_populates='users')
    keys: Mapped[List['keys']] = relationship('Keys', uselist=True, back_populates='users')
    passwords: Mapped['passwords'] = relationship('Passwords', uselist=False, back_populates='users')
    security_words: Mapped[List['securitywords']] = relationship('SecurityWords', uselist=True, back_populates='users')
    sessions: Mapped[List['sessions']] = relationship('Sessions', uselist=True, back_populates='users')


class codes(users):
    __tablename__ = 'codes'
    __table_args__ = (
        ForeignKeyConstraint(['owner'], ['private.users.secret'], ondelete='CASCADE', onupdate='CASCADE', name='owner_fk'),
        PrimaryKeyConstraint('owner', name='codes_pkey'),
        {'schema': 'private'}
    )

    owner = mapped_column(Text)
    value = mapped_column(Text, nullable=False)


class keys(Base):
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

    users: Mapped['users'] = relationship('Users', back_populates='keys')


class passwords(Base):
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

    users: Mapped['users'] = relationship('Users', back_populates='passwords')


class securitywords(Base):
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

    users: Mapped['users'] = relationship('Users', back_populates='security_words')


class sessions(Base):
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

    users: Mapped['users'] = relationship('Users', back_populates='sessions')
