from products.models import  Products, Specs, TypesSpecs 
from products.models import Categories
from sqlalchemy.orm import sessionmaker, exc

#------------------------------------------PRODUCTS------------------------------------------
#________________SELECT Functions____________________
def select_products( session: sessionmaker, n: int=None, random: bool = False):
    '''This function returns the first n products in the database as a list of objects of the class Products.'''
    #make a join with the categories table to get the main_category and root_category and subcategories
    if random:
        All_products = session.query(Products).order_by(Products.item_id).limit(n).all()
    else:
        All_products = session.query(Products).limit(n).all()
    return All_products
def select_products_by_any_category( session: sessionmaker, n: int=None, category: type [list | str] = '', main_category: str = '', root_category: str = '') -> dict:
    '''This function returns a dictionary with all the products in the database that belong to the any type of category given as an argument.
    If the category is a number, it will be used to filter the products by category_id.
    If the category is a string or a list of strings, it will be used to filter the products by subcategory.
    If the main_category is a string, it will be used to filter the products by main_category in subcategory seach.
    If the root_category is a string, it will be used to filter the products by root_category in subcategory seach.
    If the main_category and root_category are strings, it will be used to filter the products by both main_category and root_category in subcategory seach.
    '''
    products = {}
    if isinstance(category, list):
        category = str(category).replace("'", '"')
    if category.isnumeric():
        products = session.query(Products).filter(Products.category == category).limit(n).all()
    else:
        category = category.strip()
        category = category.lower()
        try:
            aux=session.query(Products).join(Categories).filter(Categories.root_cat == category).limit(n).all()
            if aux:
                products['by root_category'] = aux
                print('Obtained products by the root category', category)
        except exc.NoResultFound:
            pass
        try:
            aux=session.query(Products).join(Categories).filter(Categories.main_category == category).limit(n).all()
            if aux:
                products['by main_category'] = aux
                print('Obtained products by the main category', category)
        except exc.NoResultFound:
            pass
        if root_category is not None:
            #(where root_cat = root_category and subcategories like '%category%')
            root_category = root_category.strip()
            root_category = root_category.lower()
            try:
                aux=session.query(Products).join(Categories).filter(Categories.root_cat == root_category).filter(Categories.subcategories.like(f'%{category}%')).limit(n).all()
                if aux:
                    products['by_subcategories_and_root_category'] = aux
                    print('Obtained products by the root category', root_category)
            except exc.NoResultFound:
                pass
        if main_category is not None:
            #(where main_cat = main_category and subcategories like '%category%')
            main_category = main_category.strip()
            main_category = main_category.lower()
            try:
                aux=session.query(Products).join(Categories).filter(Categories.main_category == main_category).filter(Categories.subcategories.like(f'%{category}%')).limit(n).all()
                if aux:
                    products['by_subcategories_and_main_category'] = aux
                    print('Obtained products by the main category', main_category)
            except exc.NoResultFound:
                pass
        if main_category is not None and root_category is not None:
            #(where main_cat = main_category and root_cat = root_category and subcategories like '%category%')
            main_category = main_category.strip()
            main_category = main_category.lower()
            root_category = root_category.strip()
            root_category = root_category.lower()
            try:
                aux=session.query(Products).join(Categories).filter(Categories.main_category == main_category).filter(Categories.root_cat == root_category).filter(Categories.subcategories.like(f'%{category}%')).limit(n).all()
                if aux:
                    products['by_subcategories_and_main_and_root_category'] = aux
                    print('Obtained products by the main and root category', main_category, root_category)
            except exc.NoResultFound:
                pass
        else:
            try:
                aux=session.query(Products).join(Categories).filter(Categories.subcategories.like(f'%{category}%')).all()
                if aux:
                    products['by_subcategories'] = aux
                    print('Obtained products by the sub category', category)
            except exc.NoResultFound:
                pass
        if not products:
            print('No products found by that category', category)
    return products
def select_products_by_main_category( session: sessionmaker, category: str, n: int|None=None) -> list:
    '''This function returns all the products in the database that belong to the main category given as an argument.'''
    products = []
    category = category.strip()
    category = category.lower()
    try:
        products = session.query(Products).join(Categories).filter(Categories.main_category == category).limit(n).all()
    except exc.NoResultFound:
        print('No products found by that category', category)
    return products
def select_products_by_root_category( session: sessionmaker, category: str,n: int|None=None) -> list:
    '''This function returns all the products in the database that belong to the root category given as an argument.'''
    products = []
    category = category.strip()
    category = category.lower()
    try:
        products = session.query(Products).join(Categories).filter(Categories.root_cat == category).limit(n).all()
    except exc.NoResultFound:
        print('No products found by that category', category)
    return products
def select_products_by_subcategories( session: sessionmaker, category: type [list | str],n: int|None=None) -> list:
    '''This function returns all the products in the database that belong to the sub category given as an argument. it can be a list of subcategories or a string with the name of the subcategory. 
    IMPORTANT: The order of the subcategories in the list will be taken into account for a specific search.'''
    products = []
    category = category.strip()
    category = category.lower()
    try:
        products = session.query(Products).join(Categories).filter(Categories.subcategories.like(f'%{category}%')).limit(n).all()
    except exc.NoResultFound:
        print('No products found by that category', category)
    return products
def select_products_by_name( session: sessionmaker,name: str, n: int=None) -> list[Products]:
    '''This function returns all the products in the database that have the name given as an argument.'''
    name = name.strip()
    name = name.lower()
    products = session.query(Products).filter(Products.name.ilike(f'%{name}%')).limit(n).all()
    return products
def select_products_by_id( session: sessionmaker, id: str)-> type [Products | None]:
    '''This function returns the product in the database that has the id given as an argument.'''
    product = None
    id = id.strip()
    if id.isnumeric():
        product = session.query(Products).filter(Products.item_id == id).first()
    else:
        product = None
    return product
def select_products_by_list_of_products( session: sessionmaker, products: list[str])-> list[Products]:
    '''This function returns a list of products given as an argument.'''
    products = session.query(Products).filter(Products.item_id.in_(products)).all()
    return products
#------------------------------------------categories------------------------------------------
#________________SELECT Functions____________________
def select_categories( session: sessionmaker): 
    '''This function returns all the categories in the database as a list of objects of the class categories.'''
    All_categories = session.query(Categories).all()
    return All_categories
def select_categories_by_root_cat( session: sessionmaker, name: str): 
    '''This function returns all the categories in the database that belong to the root category given as an argument.'''
    name = name.strip()
    name = name.lower()
    selected_categories = session.query(Categories).filter(Categories.root_cat == name).all()
    return selected_categories
def select_categories_by_main_category( session: sessionmaker, name: str):
    '''This function returns all the categories in the database that belong to the main category given as an argument.'''
    name = name.strip()
    name = name.lower()
    selected_categories = session.query(Categories).filter(Categories.main_category == name).all()
    return selected_categories
def select_categories_by_subcategories( session: sessionmaker, root_category: str, subcategories: type [list | str], main_category: str=None):
    '''This function returns all the categories in the database that belong to the subcategories given as an argument.'''
    selected_categories = []
    if isinstance(subcategories, list):
        subcategories =str(subcategories); subcategories = subcategories.replace("'", '"')
        subcategories = subcategories.strip();subcategories = subcategories.lower()
        root_category = root_category.strip();root_category = root_category.lower()
        if main_category is not None:
            main_category = main_category.strip();main_category = main_category.lower()
            selected_categories = session.query(Categories).filter(Categories.root_cat == root_category).filter(Categories.main_category == main_category).filter(Categories.subcategories.like(subcategories)).all()
        else:
            selected_categories = session.query(Categories).filter(Categories.root_cat == root_category).filter(Categories.subcategories.like(subcategories)).all()
    return selected_categories
#------------------------------------------SPECS------------------------------------------
#________________SELECT Functions____________________
def select_specs( session: sessionmaker):
    '''This function returns all the specs in the database as a list of objects of the class Specs.'''
    All_specs = session.query(Specs).all()
    return All_specs
def select_specs_by_item_id( session: sessionmaker, item_id: str):
    '''This function returns all the specs in the database that belong to the item_id given as an argument.'''
    specs = session.query(Specs).filter(Specs.item_id == item_id).all()
    ind_specs = {spec['type']:[] for spec in specs}
    for spec in specs:
        ind_specs[spec['type']].append(spec)
    return ind_specs
def select_specs_by_list_of_products( session: sessionmaker, products: list):
    '''This function returns a list of dictionaries with the specs of the products given as an argument.'''
    specs = {}
    for product in products:
        if isinstance(product, Products):
            specs[product.item_id] = session.query(Specs).filter(Specs.item_id == product.item_id).all()
    return specs
def select_specs_by_list_of_ids( session: sessionmaker, ids: list):
    """
    """
    specs = session.query(Specs).filter(Specs.item_id.in_(ids)).all()
    ind_specs = {spec['item_id']:[] for spec in specs}
    for spec in specs:
        ind_specs[spec['item_id']].append(spec)
    return ind_specs

def select_all_columns_join_products_and_specs( session: sessionmaker, list_of_products: list):
    '''This function returns a list of dictionaries with the specs of the products given as an argument.'''
    specs = []
    for product in list_of_products:
        specs.append(session.query(Products, Specs, *Products.__table__.columns, *Specs.__table__.columns).join(Specs).filter(Products.item_id == Specs.item_id).filter(Products.item_id == product).all())
    return specs
#------------------------------------------TYPES_SPECS------------------------------------------
#________________SELECT Functions____________________
def select_types_specs( session: sessionmaker):
    All_types_specs = session.query(TypesSpecs).all()
    return All_types_specs
def select_types_specs_by_name( session: sessionmaker, name: str):
    types_specs = session.query(TypesSpecs).filter(TypesSpecs.types_specs == name).all()
    return types_specs