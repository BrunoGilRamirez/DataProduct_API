from typing import List, Optional

from sqlalchemy import BigInteger, Column, ForeignKeyConstraint, Index, PrimaryKeyConstraint, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, declarative_base, mapped_column, relationship
from sqlalchemy.orm.base import Mapped

Base = declarative_base()


class TreeOfCategories(Base):
    __tablename__ = 'tree_of_categories'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='tree_of_cathegories_pkey'),
        UniqueConstraint('all_categories', name='tree_of_cathegories_all_categories_key'),
        UniqueConstraint('id', name='tree_of_cathegories_id_key')
    )

    id = mapped_column(Text)
    all_categories = mapped_column(Text, nullable=False)
    root_cat = mapped_column(Text)
    subcategories = mapped_column(Text)
    main_category = mapped_column(Text)

    products: Mapped[List['Products']] = relationship('Products', uselist=True, back_populates='tree_of_categories')


class TypesSpecs(Base):
    __tablename__ = 'types_specs'
    __table_args__ = (
        PrimaryKeyConstraint('T_id', 'types_specs', name='types_specs_pkey'),
        UniqueConstraint('T_id', name='types_specs_T_id_key'),
        UniqueConstraint('types_specs', name='types_specs_types_specs_key')
    )

    T_id = mapped_column(BigInteger, nullable=False)
    types_specs = mapped_column(Text, nullable=False)

    specs: Mapped[List['Specs']] = relationship('Specs', uselist=True, back_populates='types_specs')


class Products(Base):
    __tablename__ = 'products'
    __table_args__ = (
        ForeignKeyConstraint(['category'], ['tree_of_categories.id'], ondelete='CASCADE', onupdate='CASCADE', deferrable=True, initially='DEFERRED', name='Product_category_id_fk'),
        PrimaryKeyConstraint('item_id', 'name', name='products_pkey'),
        UniqueConstraint('item_id', name='products_item_id_key'),
        Index('fki_Product_category_id_fk', 'category')
    )

    item_id = mapped_column(Text, nullable=False)
    name = mapped_column(Text, nullable=False)
    itm_description = mapped_column(Text)
    category = mapped_column(Text)
    datasheet_link = mapped_column(Text)
    itms_val_in_pkg = mapped_column(Text)
    img = mapped_column(Text)
    path = mapped_column(Text)

    tree_of_categories: Mapped[Optional['TreeOfCategories']] = relationship('TreeOfCategories', back_populates='products')
    Visual_resources: Mapped[List['VisualResources']] = relationship('VisualResources', uselist=True, back_populates='item')
    specs: Mapped[List['Specs']] = relationship('Specs', uselist=True, back_populates='item')


class VisualResources(Base):
    __tablename__ = 'Visual_resources'
    __table_args__ = (
        ForeignKeyConstraint(['item_id'], ['products.item_id'], ondelete='CASCADE', onupdate='CASCADE', deferrable=True, initially='DEFERRED', name='item_id_vr_fk'),
        PrimaryKeyConstraint('id', 'item_id', 'link', name='Visual_resources_pkey'),
        UniqueConstraint('id', name='Visual_resources_id_key')
    )

    id = mapped_column(BigInteger, nullable=False)
    item_id = mapped_column(Text, nullable=False)
    link = mapped_column(Text, nullable=False)

    item: Mapped['Products'] = relationship('Products', back_populates='Visual_resources')


class Specs(Base):
    __tablename__ = 'specs'
    __table_args__ = (
        ForeignKeyConstraint(['item_id'], ['products.item_id'], ondelete='CASCADE', onupdate='CASCADE', deferrable=True, initially='DEFERRED', name='Product_key_fk'),
        ForeignKeyConstraint(['type'], ['types_specs.types_specs'], ondelete='CASCADE', onupdate='CASCADE', deferrable=True, initially='DEFERRED', name='Type_spec_typespec_fk'),
        PrimaryKeyConstraint('id', 'item_id', name='specs_pkey'),
        UniqueConstraint('id', name='specs_spec_id_key'),
        Index('fki_Product_key_fk', 'item_id'),
        Index('fki_Type_spec_typespec_fk', 'type')
    )

    id = mapped_column(BigInteger, nullable=False)
    item_id = mapped_column(Text, nullable=False)
    name = mapped_column(Text, nullable=False)
    value = mapped_column(Text, nullable=False)
    type = mapped_column(Text, nullable=False)

    item: Mapped['Products'] = relationship('Products', back_populates='specs')
    types_specs: Mapped['TypesSpecs'] = relationship('TypesSpecs', back_populates='specs')
