from fastapi import FastAPI
from fastapi.responses import FileResponse,HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from products.DB_Operations import *
from session_management import get_session
import pandas as pd
from fastapi import Depends,Request
import os
from access.extras import *
from access.schemas import *
from access.crud import *
from access.schemas import *
#---------------------General settings---------------------
#this is to get the session from the .env file
session = get_session('.env')
list_endpoints = [("/products", "Get all products id"), 
            ("/product_by_id/2674530000", "Get a product by its id"), 
            ("/product_by_name/s2c 2.5", "Get a product by its name"), 
            ("/products_by_root_category/conectividad", "Get all products by root category"), 
            ("/products_by_main_category/sai-au universal%20pro%20m8 digital", "Get all products by main category"), 
            ('/products_by_subcategories/?category=["sistemas de e/s", "i/o system ip67 - u-remote", "universal pro"]', "Get all products by subcategories"), 
            ('/products_by_any_category/?category=["sistemas de e/s", "i/o system ip67 - u-remote", "universal pro"]&root_category=automatización y software&main_category=sai-au universal pro m8 digital', "Get all products by any category"), 
            ("/categories", "Get all categories"), 
            ("/specs_by_item_id/2674530000", "Get all specs by item id"),
            ('/products_by_list_of_products/?ids=["0101700000","0103300000","0105100000","0105260000","0105620000","0105920000","0106020000","0107160000","0107260000","0110060000","0110080000"]', "Get all specs by list of products"),
            ("/product_and_specs_by_id/2674530000", "Get a product and its specs by its id"),
            ('/products_to_excel/?list_of_products=["0101700000","0103300000","0105100000","0105260000","0105620000","0105920000","0106020000","0107160000","0107260000","0110060000","0110080000"]&n=10&random=True', "Get an excel file with the products")
            ]

#create a temp directory to store the excel files
if not os.path.exists('temp'):
    os.makedirs('temp')
#-----------------------FastAPI-----------------------
#here we create an instance of FastAPI app. This is the main object of our application
wdm = FastAPI()
#wdm.mount('/beautiful_view', WSGIMiddleware(flwdm))
#this is to serve the static files and the templates
wdm.mount("/static", StaticFiles(directory="static"), name="static")
temp = Jinja2Templates(directory="templates")
#-----------------------view-----------------------

@wdm.get("/view/", response_class=HTMLResponse)
async def index(request: Request):
    return temp.TemplateResponse("index.html", {"request": request, "endpoints": list_endpoints})

@wdm.get("/view/products", response_class=HTMLResponse)
async def products(request: Request):
    products = select_n_products(session, 10, random=True)
    return temp.TemplateResponse("products.html", {"request": request, "products": products})

@wdm.get("/view/product_by_id/{product_id}", response_class=HTMLResponse)
async def product_by_id(request: Request,product_id: str):
    product = select_products_by_id(session, product_id)
    return temp.TemplateResponse("product_basic.html", {"request": request, "product": product})

@wdm.get("/view/product_by_name/{product_name}")
async def product_by_name(request: Request,product_name: str):
    product = select_products_by_name(session, product_name)
    return temp.TemplateResponse("products.html", {"request": request, "products": product})

@wdm.get("/view/products_by_root_category/{category}")
async def products_by_root_category(request: Request,category: str):
    product = select_products_by_root_category(session, category, n=10)
    return temp.TemplateResponse("products_by_root.html", {"request": request, "products": product, "root": category})

@wdm.get("/view/products_by_main_category/{category}")
async def products_by_main_category(request: Request,category: str):
    product = select_products_by_main_category(session, category)
    return temp.TemplateResponse("products_by_main.html", {"request": request, "products": product, "main": category})

@wdm.get("/view/products_by_subcategories/")
async def products_by_subcategories(request: Request,category: str = ''):
    category = request.query_params.get('category')
    category = category.replace('/', '+')
    product = select_products_by_subcategories(session, category)
    return temp.TemplateResponse("products_by_sub.html", {"request": request, "products": product, "sub": category})

@wdm.get("/view/products_by_any_category/")
async def products_by_any_category(request: Request,category: str = '', main_category: str = '', root_category: str = ''):
    category = request.query_params.get('category')
    main_category = request.query_params.get('main_category')
    root_category = request.query_params.get('root_category')
    category = category.replace('/', '+')
    product = select_products_by_any_category(session, category, main_category, root_category)
    return temp.TemplateResponse("products_by_any.html", {"request": request, "products": product, "category": category, "main_category": main_category, "root_category": root_category})

@wdm.get("/view/categories")
async def categories():
    pass

@wdm.get("/view/categories_by_root_cat/{name}")
async def categories_by_root_cat(name: str):
    pass

@wdm.get("/view/categories_by_main_category/{name}")
async def categories_by_main_category(name: str):
    pass

@wdm.get("/view/categories_by_subcategories/{root_category}")
async def categories_by_subcategories(root_category: str, subcategories: str):
    pass

@wdm.get("/view/specs")
async def specs():
    pass

@wdm.get("/view/product_and_specs_by_id/{item_id}")
async def specs_by_item_id(request: Request,item_id: str):
    product = select_products_by_id(session, item_id)
    specs = select_specs_by_item_id(session, item_id)
    print(f"\nspecs: {specs}")
    return temp.TemplateResponse("product.html", {"request": request, "product": product, "specs": specs})

#------------Endpoints_FastAPI--------------------
@wdm.get("/")
async def read_root():
    return list_endpoints
@wdm.get("/products")
async def read_products(request: Request,flag: bool = Depends(get_current_user_API)):
    #lets start counting the time it takes to open and close the session
    if flag:
        print("flag is true")
        products = select_products(session)
        return products
@wdm.get("/product_by_id/{product_id}") 
async def read_products_by_id(request: Request,product_id: str, flag: bool = Depends(get_current_user_API)):
    if flag:
        product = select_products_by_id(session, product_id)
        return product
@wdm.get("/product_by_name/{product_name}")
async def read_products_by_name(request: Request,product_name: str, flag: bool = Depends(get_current_user_API)):
    if flag:
        product = select_products_by_name(session, product_name)
        return product
@wdm.get("/products_by_root_category/{category}")
async def read_products_by_root_category(request: Request,category: str, flag: bool = Depends(get_current_user_API)):
    if flag:
        product = select_products_by_root_category(session, category)
        print (f"number of products: {len(product)}")
        return product
@wdm.get("/products_by_main_category/{category}")
async def read_products_by_main_category(request: Request,category: str, flag: bool = Depends(get_current_user_API)):
    if flag:
        print(f'category: {category}')
        product = select_products_by_main_category(session, category)
        return product
@wdm.get("/products_by_subcategories/")
async def read_products_by_subcategories(request: Request,category: str, flag: bool = Depends(get_current_user_API)):
    if flag:   
        category=category.replace('/','+')
        print(f'category: {category}')
        product = select_products_by_subcategories(session, category)
        return product
@wdm.get("/products_by_any_category/")
async def read_products_by_any_category(request: Request,category: str='', main_category: str='', root_category: str='', flag: bool = Depends(get_current_user_API)):
    if flag:
        category=category.replace('/','+')
        product = select_products_by_any_category(session, category, main_category, root_category)
        return product

# Categories endpoints
@wdm.get("/categories")
async def read_categories(request: Request,flag: bool = Depends(get_current_user_API)):
    if flag:
        all_categories = select_categories(session)
        return all_categories

@wdm.get("/categories_by_root_cat/{name}")
async def read_categories_by_root_cat(request: Request,name: str, flag: bool = Depends(get_current_user_API)):
    if flag:
        selected_categories = select_categories_by_root_cat(session, name)
        return selected_categories

@wdm.get("/categories_by_main_category/{name}")
async def read_categories_by_main_category(request: Request,name: str, flag: bool = Depends(get_current_user_API)):
    if flag:
        selected_categories = select_categories_by_main_category(session, name)
        return selected_categories

@wdm.get("/categories_by_subcategories/{root_category}")
async def read_categories_by_subcategories(request: Request,root_category: str, subcategories: str, flag: bool = Depends(get_current_user_API)):
    if flag:
        selected_categories = select_categories_by_subcategories(session, root_category, subcategories)
        return selected_categories

# Specs endpoints
@wdm.get("/specs")
async def read_specs(request: Request,flag: bool = Depends(get_current_user_API)):
    if flag:
        all_specs = select_specs(session)
        return all_specs

@wdm.get("/specs_by_item_id/{item_id}")
async def read_specs_by_item_id(request: Request,item_id: str, flag: bool = Depends(get_current_user_API)):
    if flag:
        specs = select_specs_by_item_id(session, item_id)
        return specs

# endpoints for read a list of products ids and return the specs of all of them
@wdm.get("/products_by_list_of_products/")
async def read_products_by_list_of_products(request: Request,ids: str, with_specs: bool = True, flag: bool = Depends(get_current_user_API)):
    if flag:
        ids =eval(ids)
        products = []
        if isinstance(ids, list):
            for id in ids:
                product = select_products_by_id(session, id) # read the product by its id
                if with_specs and product is not None:  # if the product exists and we want the specs
                    specs = select_specs_by_item_id(session, id)  # read the specs by the item id
                else:
                    specs = "No specs"
                    product= "Not found"
                products.append({"product": product, "specs": specs})
        return products
# TypesSpecs endpoints
@wdm.get("/types_specs")
async def read_types_specs(request: Request, flag: bool = Depends(get_current_user_API)):
    if flag:
        all_types_specs = select_types_specs(session)
        return all_types_specs

@wdm.get("/types_specs_by_name/{name}")
async def read_types_specs_by_name(request: Request,name: str, flag: bool = Depends(get_current_user_API)):
    if flag:
        types_specs = select_types_specs_by_name(session, name)
        return types_specs

#get a product and specs by its id
@wdm.get("/product_and_specs_by_id/{product_id}")
async def read_product_and_specs_by_id(request: Request,product_id: str, flag: bool = Depends(get_current_user_API)):
    if flag:
        product=select_products_by_id(session, product_id)
        specs=select_specs_by_item_id(session, product_id)
        product_and_specs = {"product":product, "specs":specs}
        return product_and_specs
#get an excel file with the products
@wdm.get("/products_to_excel/")
async def read_products_to_excel(request: Request,list_of_products: str = None, n: int = 10, random: bool = True, flag: bool = Depends(get_current_user_API)):
    if flag:
        if list_of_products:
            list_of_products = eval(list_of_products)
            products = select_products_by_list_of_products(session, list_of_products)
            #sort the products by the list of products
            products = sorted(products, key=lambda x: list_of_products.index(x['item_id']))
        else:
            products = select_n_products(session, n, random=random)
        products = [dict(product) for product in products]
        df = pd.DataFrame.from_records(products)
        #gives a timestamp compatible with the file name format<
        timestamp = pd.Timestamp.now().strftime('%Y-%m-%d_%H-%M-%S')
        filename = f'products{timestamp}.xlsx'
        df.to_excel(("temp/"+filename), index=False)
        return FileResponse(("temp/"+filename), filename=filename)
@wdm.get("/products_with_specs_to_excel/")
async def read_products_with_specs_to_excel(request: Request,list_of_products: str, flag: bool = Depends(get_current_user_API)):
    if flag:
        if list_of_products:
            list_of_products = eval(list_of_products)
            products = select_all_collumns_join_products_and_specs(session, list_of_products)
            print(f"products: {products[0]}")
            #sort the products by the list of products
        products = [dict(product) for product in products]
        df = pd.DataFrame.from_records(products)
        #gives a timestamp compatible with the file name format
        timestamp = pd.Timestamp.now().strftime('%Y-%m-%d_%H-%M-%S')
        filename = f'products_with_specs{timestamp}.xlsx'
        df.to_excel(("temp/"+filename), index=False)
        return FileResponse(("temp/"+filename), filename=filename)
