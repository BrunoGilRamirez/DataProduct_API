from pydantic import BaseModel
from typing import List, Optional

class TreeOfCategorie(BaseModel):
    id: str
    all_categories: str
    root_cat: str
    subcategories: str
    main_category: str
    products: list['Product']=[]

class TypesSpec(BaseModel):
    T_id: int
    types_specs: str
    specs: list['Spec']=[]

class Product(BaseModel):
    item_id: str
    name: str
    itm_description: str
    category: str
    datasheet_link: str
    itms_val_in_pkg: str
    img: str
    path: str
    tree_of_categories: TreeOfCategorie= None
    specs: list['Spec']=[]

class Spec(BaseModel):
    id: int
    item_id: str
    name: str
    value: str
    type: str
    item: Product= None
    types_spec: TypesSpec= None     
