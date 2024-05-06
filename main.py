from fastapi import FastAPI
from fastapi.responses import FileResponse,HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from products.DB_Operations import *
from session_management import get_session
import pandas as pd
from fastapi import Depends,Request
from access.extras import *
from access.schemas import *
from access.crud import *
from access.schemas import *
from starlette.middleware.sessions import SessionMiddleware
import os
#---------------------General settings---------------------
#this is to get the session from the .env file
session = get_session('.env')
list_endpoints = [ ("/products/?n=10", "Obtener todos los productos", "/products", "Opcional: número entero por ejemplo \"/?n=10\""), 
            ("/product_by_id/2674530000", "Obtener producto por Código SAP o ID","/product_by_id/", "Cadena numérica de 10 dígitos"), 
            ("/product_by_name/?name=s2c 2.5&n=10", "Obtener producto por nombre","/product_by_name/", "Cadena de texto"), 
            ("/products_by_root_category/?category=conectividad&n=10", "Obtener productos por categoría Raíz","/products_by_root_category/", "Cadena de texto"), 
            ("/products_by_main_category/?category=sai-au universal%20pro%20m8 digital&n=10", "Obtener productos por categoría principal ","/products_by_main_category/", "Cadena de texto"), 
            ('/products_by_subcategories/?subcategories=["sistemas de e/s", "i/o system ip67 - u-remote", "universal pro"]&n=10', "Obtener productos por sub-categorías","/products_by_subcategories/", "Cadena de texto en forma de lista de sub-categorías separadas por coma [\"subcat1\", \"subcat2\", \"subcat3\"]"), 
            ('/products_by_any_category/?category=["sistemas de e/s", "i/o system ip67 - u-remote", "universal pro"]&root_category=automatización y software&main_category=sai-au universal pro m8 digital&n=10', "Obtener productos por cualquier categoría","/products_by_any_category/", "Cadena de texto en forma de lista de sub-categorías separadas por coma [\"subcat1\", \"subcat2\", \"subcat3\"]"), 
            ("/categories", "Obtener todas las categorías", "/categories", "Sin parámetros"), 
            ("/specs_by_item_id/2674530000", "Obtener especificaciones por ID de producto", "/specs_by_item_id/", "Cadena numérica de 10 dígitos"),
            ('/products_by_list_of_products/?ids=["0101700000","0103300000","0105100000","0105260000","0105620000","0105920000","0106020000","0107160000","0107260000","0110060000","0110080000"]', "Obtener productos y especificaciones por lista de productos", "/products_by_list_of_products/", "Cadena de texto en forma de lista de ID de productos separadas por coma [\"0000000000\", \"0000000001\", \"0000000002\"]"),
            ("/product_and_specs_by_id/2674530000", "Obtener producto y especificaciones por ID de producto", "/product_and_specs_by_id/", "Cadena numérica de 10 dígitos"),
            ('/products_to_excel/?list_of_products=["0101700000","0103300000","0105100000","0105260000","0105620000","0105920000","0106020000","0107160000","0107260000","0110060000","0110080000"]', "Obtener productos en formato Excel", "/products_to_excel/", "Cadena de texto en forma de lista de ID de productos separadas por coma [\"0000000000\", \"0000000001\", \"0000000002\"] y número entero"),
            ]

#create a temp directory to store the excel files
if not os.path.exists('temp'):
    os.makedirs('temp')
#-----------------------FastAPI-----------------------
#here we create an instance of FastAPI app. This is the main object of our application
wdm = FastAPI()
#this is to serve the static files and the templates
wdm.mount("/static", StaticFiles(directory="static"), name="static")
wdm.add_middleware(SessionMiddleware, secret_key=os.getenv('SECRET_KEY_sessions'), https_only=True)
temp = Jinja2Templates(directory="templates")

#--------------------------- icons --------------------------------
@wdm.get('/favicon.ico', include_in_schema=False)
async def favicon():
    file_name = "icons/favicon.ico"
    file_path = os.path.join(wdm.root_path, "static", file_name)
    return FileResponse(path=file_path, headers={"Content-Disposition": "attachment; filename=" + file_name})


#------------Endpoints_FastAPI--------------------
@wdm.get("/")
async def read_root(request: Request, db: Session = Depends(get_db)):
    token= request.session.get('api_token')
    if token:
        request_add_token(request, token)
    flag = await get_current_user_view(request=request, session=db, raise_exception=False)
    if flag:
        return list_endpoints
    else:
        if token:
            request.session.pop('api_token')
        return RedirectResponse(url='/view/')
@wdm.get("/products/")
async def read_products(request: Request,n:int=None, flag: bool = Depends(get_current_user_API)):
    #lets start counting the time it takes to open and close the session
    if flag:
        products = select_products(session, n)
        return products
@wdm.get("/product_by_id/{product_id}") 
async def read_products_by_id(request: Request,product_id: str, flag: bool = Depends(get_current_user_API)):
    if flag:
        product = select_products_by_id(session, product_id)

        return product
@wdm.get("/product_by_name/{name}")
@wdm.get("/product_by_name/")
async def read_products_by_name(request: Request,name: str,n:int=None, flag: bool = Depends(get_current_user_API)):
    if flag:
        product = select_products_by_name(session, name, n)
        return product
@wdm.get("/products_by_root_category/{category}")
@wdm.get("/products_by_root_category/")
async def read_products_by_root_category(request: Request,category: str,n:int=None, flag: bool = Depends(get_current_user_API)):
    if flag:
        product = select_products_by_root_category(session, category, n)
        return product
@wdm.get("/products_by_main_category/{category}")
@wdm.get("/products_by_main_category/")
async def read_products_by_main_category(request: Request,category: str, n:int=None,flag: bool = Depends(get_current_user_API)):
    if flag:
        product = select_products_by_main_category(session, category, n)
        return product
@wdm.get("/products_by_subcategories/{subcategories}")
@wdm.get("/products_by_subcategories/")
async def read_products_by_subcategories(request: Request,subcategories: str, n:int=None,flag: bool = Depends(get_current_user_API)):
    if flag:   
        subcategories=subcategories.replace('/','+')
        product = select_products_by_subcategories(session, subcategories, n)
        return product
@wdm.get("/products_by_any_category/")
async def read_products_by_any_category(request: Request,n:int=None,category: str=None, main_category: str=None, root_category: str=None, flag: bool = Depends(get_current_user_API)):
    if flag:
        category=category.replace('/','+')
        product = select_products_by_any_category(session, n, category, main_category, root_category)
        return product

# -----------------Categories endpoints-----------------
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

@wdm.get("/categories_by_subcategories/{subcategories}")
@wdm.get("/categories_by_subcategories/")
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
            products = select_products(session, n, random=random)
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
            products = select_all_columns_join_products_and_specs(session, list_of_products)
            #sort the products by the list of products
        products = [dict(product) for product in products]
        df = pd.DataFrame.from_records(products)
        #gives a timestamp compatible with the file name format
        timestamp = pd.Timestamp.now().strftime('%Y-%m-%d_%H-%M-%S')
        filename = f'products_with_specs{timestamp}.xlsx'
        df.to_excel(("temp/"+filename), index=False)
        return FileResponse(("temp/"+filename), filename=filename)

#-----------------------view-----------------------
@wdm.get("/view")
@wdm.post("/view")
async def view(request: Request, db: Session = Depends(get_db)):
    flag=False
    token = None
    if request.method == "POST":
        form = await request.form()
        token = form.get('token')
        request.session['api_token'] = token
    if request.method == "GET":
        token = request.session.get('api_token')
    if token:
        request_add_token(request, token)
        flag= await get_current_user_view(request=request, session=db, raise_exception=False)
    if flag:
        return RedirectResponse(url='/view/home', status_code=status.HTTP_302_FOUND)
    else:
        if token:
            request.session.pop('api_token')
        return temp.TemplateResponse("view.html", {"request": request})
    
@wdm.get("/view/home", response_class=HTMLResponse, include_in_schema=False)
async def index(request: Request, db: Session = Depends(get_db)):
    token = request.session.get('api_token')
    flag=False
    if token:
        request_add_token(request, token)
        flag= await get_current_user_view(request=request, session=db, raise_exception=False)
    if flag:
        return temp.TemplateResponse("index.html", {"request": request, "endpoints": list_endpoints, "token": token})
    else:
        if token:
            request.session.pop('api_token')
        return RedirectResponse(url='/view')

@wdm.get("/view/products", response_class=HTMLResponse, include_in_schema=False)
async def Products(request: Request, db: Session = Depends(get_db)):
    token = request.session.get('api_token')
    flag=False
    if token:
        request_add_token(request, token)
        flag= await get_current_user_view(request=request, session=db, raise_exception=False)
    if flag:
        products = select_products(session, 10, random=True)
        return temp.TemplateResponse("products.html", {"request": request, "products": products})
    else: 
        if token:
            request.session.pop('api_token')
        return RedirectResponse(url='/view')

@wdm.get("/view/product_by_id/{product_id}", response_class=HTMLResponse, include_in_schema=False)
async def product_by_id(request: Request,product_id: str, db: Session = Depends(get_db)):
    token = request.session.get('api_token')
    flag=False
    if token:
        request_add_token(request, token)
        flag= await get_current_user_view(request=request, session=db, raise_exception=False)
    if flag:
        product = select_products_by_id(session, product_id)
        return temp.TemplateResponse("product_basic.html", {"request": request, "product": product})
    else: 
        if token:
            request.session.pop('api_token')
        return RedirectResponse(url='/view')

@wdm.get("/view/product_by_name/{name}", response_class=HTMLResponse, include_in_schema=False)
@wdm.get("/view/product_by_name/", response_class=HTMLResponse, include_in_schema=False)
async def product_by_name(request: Request,name: str, db: Session = Depends(get_db)):
    token = request.session.get('api_token')
    flag=False
    if token:
        request_add_token(request, token)
        flag= await get_current_user_view(request=request, session=db, raise_exception=False)
    if flag:
        product = select_products_by_name(session, name)
        return temp.TemplateResponse("products_by_name.html", {"request": request, "products": product, "name":name})
    else: 
        if token:
            request.session.pop('api_token')
        return RedirectResponse(url='/view')

@wdm.get("/view/products_by_root_category/{category}", response_class=HTMLResponse, include_in_schema=False)
@wdm.get("/view/products_by_root_category/", response_class=HTMLResponse, include_in_schema=False)
async def products_by_root_category(request: Request,category: str, db: Session = Depends(get_db)):
    token = request.session.get('api_token')
    flag=False
    if token:
        request_add_token(request, token)
        flag= await get_current_user_view(request=request, session=db, raise_exception=False)
    if flag:
        product = select_products_by_root_category(session, category, n=10)
        return temp.TemplateResponse("products_by_root.html", {"request": request, "products": product, "root": category})
    else: 
        if token:
            request.session.pop('api_token')
        return RedirectResponse(url='/view')

@wdm.get("/view/products_by_main_category/{category}", response_class=HTMLResponse, include_in_schema=False)
@wdm.get("/view/products_by_main_category/", response_class=HTMLResponse, include_in_schema=False)
async def products_by_main_category(request: Request,category: str, db: Session = Depends(get_db)):
    token = request.session.get('api_token')
    flag=False
    if token:
        request_add_token(request, token)
        flag= await get_current_user_view(request=request, session=db, raise_exception=False)
    if flag:
        product = select_products_by_main_category(session, category)
        return temp.TemplateResponse("products_by_main.html", {"request": request, "products": product, "main": category})
    else: 
        if token:
            request.session.pop('api_token')
        return RedirectResponse(url='/view')
@wdm.get("/view/products_by_subcategories/{subategories}", response_class=HTMLResponse, include_in_schema=False)
@wdm.get("/view/products_by_subcategories/", response_class=HTMLResponse, include_in_schema=False)
async def products_by_subcategories(request: Request, subcategories: str, db: Session = Depends(get_db)):
    token = request.session.get('api_token')
    flag=False
    if token:
        request_add_token(request, token)
        flag= await get_current_user_view(request=request, session=db, raise_exception=False)
    if flag:
        subcategories = subcategories.replace('/', '+')
        product = select_products_by_subcategories(session, subcategories)
        return temp.TemplateResponse("products_by_sub.html", {"request": request, "products": product, "sub": subcategories})
    else: 
        if token:
            request.session.pop('api_token')
        return RedirectResponse(url='/view')

@wdm.get("/view/products_by_any_category/", response_class=HTMLResponse, include_in_schema=False)
async def products_by_any_category(request: Request, n:int=None,category: str = '', main_category: str = '', root_category: str = '', db: Session = Depends(get_db)):
    token = request.session.get('api_token')
    flag=False
    if token:
        request_add_token(request, token)
        flag= await get_current_user_view(request=request, session=db, raise_exception=False)
    if flag:
        category = request.query_params.get('category')
        main_category = request.query_params.get('main_category')
        root_category = request.query_params.get('root_category')
        category = category.replace('/', '+')
        product = select_products_by_any_category(session, n, category, main_category, root_category)
        return temp.TemplateResponse("products_by_any.html", {"request": request, "products": product, "category": category, "main_category": main_category, "root_category": root_category})
    else: 
        if token:
            request.session.pop('api_token')
        return RedirectResponse(url='/view')
    
@wdm.get("/view/categories", response_class=HTMLResponse, include_in_schema=False)
async def TreeOfCategories():
    pass

@wdm.get("/view/categories_by_root_cat/{name}", response_class=HTMLResponse, include_in_schema=False)
async def categories_by_root_cat(name: str):
    pass

@wdm.get("/view/categories_by_main_category/{name}", response_class=HTMLResponse, include_in_schema=False)
async def categories_by_main_category(name: str):
    pass

@wdm.get("/view/categories_by_subcategories/{root_category}", response_class=HTMLResponse, include_in_schema=False)
async def categories_by_subcategories(root_category: str, subcategories: str):
    pass

@wdm.get("/view/specs")
async def Specs():
    pass

@wdm.get("/view/product_and_specs_by_id/{item_id}", response_class=HTMLResponse, include_in_schema=False)
async def specs_by_item_id(request: Request,item_id: str, db: Session = Depends(get_db)):
    token = request.session.get('api_token')
    flag=False
    if token:
        request_add_token(request, token)
        flag= await get_current_user_view(request=request, session=db, raise_exception=False)
    if flag:
        product = select_products_by_id(session, item_id)
        specs = select_specs_by_item_id(session, item_id)
        return temp.TemplateResponse("product.html", {"request": request, "product": product, "specs": specs})
    else:
        if token:
            request.session.pop('api_token')
        return RedirectResponse(url='/view')