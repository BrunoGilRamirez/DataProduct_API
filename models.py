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
    #columns from the table
    id = mapped_column(Text)
    all_categories = mapped_column(Text, nullable=False)
    root_cat = mapped_column(Text)
    subcategories = mapped_column(Text)
    main_category = mapped_column(Text)
    #relationships
    products: Mapped[List['Products']] = relationship('Products', uselist=True, back_populates='tree_of_categories')
    #methods
    def __init__(self, id: str, all_categories: str, root_cat: str, subcategories: str, main_category: str):
        self.id = id
        self.all_categories = all_categories
        self.root_cat = root_cat
        self.subcategories = subcategories
        self.main_category = main_category
    def __repr__(self):
        return '{'+f'id: {self.id}, all_categories: {self.all_categories}, root_cat: {self.root_cat}, subcategories: {self.subcategories}, main_category: {self.main_category}'+'}'
    def __str__(self):
        return f'id: {self.id}, all_categories: {self.all_categories}, root_cat: {self.root_cat}, subcategories: {self.subcategories}, main_category: {self.main_category}'
    def __eq__(self, other):
        return self.id == other.id and self.all_categories == other.all_categories and self.root_cat == other.root_cat and self.subcategories == other.subcategories and self.main_category == other.main_category
    def __hash__(self):
        return hash(self.id) #this method is used to compare objects in sets
    def __bool__(self):
        return bool(self.id)
    def __copy__(self):
        return TreeOfCategories(self.id, self.all_categories, self.root_cat, self.subcategories, self.main_category)
    def __getitem__(self, item):
        if item in self.__dict__:
            return self.__dict__[item]
        else:
            raise KeyError(f'Item {item} not found')
    def __setitem__(self, item, value):
        self.__dict__[item] = value
    def __contains__(self, item):
        return item in self.__dict__
    def __iter__(self):
        yield self.id
        yield self.all_categories
        yield self.root_cat
        yield self.subcategories
        yield self.main_category
    def __len__(self):
        return len(self.__dict__)
    #the subcategories are a list of names of the subcategories casted to a string
    def get_subcategories(self):
        return eval(self.subcategories)
    #also all_categories is a list of names of the categories casted to a string
    def get_all_categories(self):
        return eval(self.all_categories)
    #add the method to do .keys() and .values() to the object
    def keys(self):
        return self.__dict__.keys()
    def values(self):
        return self.__dict__.values()
    def items(self):
        return self.__dict__.items()
    def __call__(self, *args, **kwargs): #this method is used to call the object as a function
        return self.__dict__
    



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
    def __init__(self, T_id: int, types_specs: str):
        self.T_id = T_id
        self.types_specs = types_specs
    def __repr__(self):
        return '{'+f'T_id: {self.T_id}, types_specs: {self.types_specs}'+'}'
    def __str__(self):
        return f'T_id: {self.T_id}, types_specs: {self.types_specs}'
    def __eq__(self, other):
        return self.T_id == other.T_id and self.types_specs == other.types_specs
    def __hash__(self):
        return hash(self.T_id)
    def __copy__(self):
        return TypesSpecs(self.T_id, self.types_specs)
    def __getitem__(self, item):
        if item in self.__dict__:
            return self.__dict__[item]
        else:
            raise KeyError(f'Item {item} not found')
    def __setitem__(self, item, value):
        self.__dict__[item] = value
    def __contains__(self, item):
        return item in self.__dict__
    def __iter__(self):
        yield self.T_id
        yield self.types_specs
    def __len__(self):
        return len(self.__dict__)

class Products(Base):
    __tablename__ = 'products'
    __table_args__ = (
        ForeignKeyConstraint(['category'], ['tree_of_categories.id'], ondelete='CASCADE', onupdate='CASCADE', deferrable=True, initially='DEFERRED', name='Product_category_id_fk'),
        PrimaryKeyConstraint('item_id', 'name', name='products_pkey'),
        UniqueConstraint('item_id', name='products_item_id_key'),
        Index('fki_Product_category_id_fk', 'category')
    )
    #columns from the table
    item_id = mapped_column(Text, nullable=False)
    name = mapped_column(Text, nullable=False)
    itm_description = mapped_column(Text)
    category = mapped_column(Text)
    datasheet_link = mapped_column(Text)
    itms_val_in_pkg = mapped_column(Text)
    img = mapped_column(Text)
    path = mapped_column(Text)
    #relationships
    tree_of_categories: Mapped[Optional['TreeOfCategories']] = relationship('TreeOfCategories', back_populates='products')
    specs: Mapped[List['Specs']] = relationship('Specs', uselist=True, back_populates='item')
    #methods
    def __init__(self, item_id: str, name: str, itm_description: str, category: str, datasheet_link: str, itms_val_in_pkg: str, img: str, path: str):
        self.item_id = item_id
        self.name = name
        self.itm_description = itm_description
        self.category = category
        self.datasheet_link = datasheet_link
        self.itms_val_in_pkg = itms_val_in_pkg
        self.img = img
        self.path = path
    def __repr__(self):
        return '{'+f'item_id: {self.item_id}, name: {self.name}, itm_description: {self.itm_description}, category: {self.category}, datasheet_link: {self.datasheet_link}, itms_val_in_pkg: {self.itms_val_in_pkg}, img: {self.img}, path: {self.path}'+'}'
    def __str__(self):
        return f'item_id: {self.item_id}, name: {self.name}, itm_description: {self.itm_description}, category: {self.category}, datasheet_link: {self.datasheet_link}, itms_val_in_pkg: {self.itms_val_in_pkg}, img: {self.img}, path: {self.path}'
    def __eq__(self, other):
        return self.item_id == other.item_id
    def __hash__(self):
        return hash(self.item_id)
    def __bool__(self):
        return bool(self.item_id)
    def __copy__(self):
        return Products(self.item_id, self.name, self.itm_description, self.category, self.datasheet_link, self.itms_val_in_pkg, self.img, self.path)
    def __getitem__(self, item):
        if item in self.__dict__:
            return self.__dict__[item]
        else:
            raise KeyError(f'Item {item} not found')
    def __setitem__(self, item, value):
        self.__dict__[item] = value
    def __contains__(self, item):
        return item in self.__dict__
    def __iter__(self):
        yield self.item_id
        yield self.name
        yield self.itm_description
        yield self.category
        yield self.datasheet_link
        yield self.itms_val_in_pkg
        yield self.img
        yield self.path
    def __len__(self):
        return len(self.__dict__)
    def get_path(self):
        return eval(self.path)
    def keys(self):
        #drop ['_sa_instance_state'] from the keys
        return [key for key in self.__dict__.keys() if key != '_sa_instance_state']
    def values(self):
        return [value for value in self.__dict__.values() if value != '_sa_instance_state']
    def items(self):
        return [(key, value) for key, value in self.__dict__.items() if key != '_sa_instance_state']
    def __call__(self, *args, **kwargs):
        return self.__dict__

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
    def __init__(self, id: int, item_id: str, name: str, value: str, type: str):
        self.id = id
        self.item_id = item_id
        self.name = name
        self.value = value
        self.type = type
    def __repr__(self):
        return '{'+f'"id": "{self.id}", "item_id": "{self.item_id}", "{self.name}": "{self.value}", "type": "{self.type}"'+'}'
    def __str__(self):
        return f'id: {self.id}, item_id: {self.item_id}, name: {self.name}, value: {self.value}, type: {self.type}'
    def __eq__(self, other):
        return self.id == other.id
    def __hash__(self):
        return hash(self.id)
    def __bool__(self):
        return bool(self.id)
    def __copy__(self):
        return Specs(self.id, self.item_id, self.name, self.value, self.type)
    def __getitem__(self, item):
        if item in self.__dict__:
            return self.__dict__[item]
        else:
            raise KeyError(f'Item {item} not found')
    def __setitem__(self, item, value):
        self.__dict__[item] = value
    def __contains__(self, item):
        return item in self.__dict__
    def __iter__(self):
        yield self.id
        yield self.item_id
        yield self.name
        yield self.value
        yield self.type
    def __len__(self):
        return len(self.__dict__)
