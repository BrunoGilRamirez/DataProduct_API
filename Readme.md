![Marca](https://github.com/BrunoGilRamirez/weidmuller_ProductDB_API/assets/106723899/0a3eeed8-49e4-49bd-b5d1-86b3731f5aee)

### API for Product Data Retrieval

This API provides access to WeidMuller product data, focused on product distributors. Built with FastAPI and utilizing a PostgreSQL database, it offers a user-friendly interface for querying various product-related information.

## Starting the Server

To start the UVicorn server, run the following command:

```bash
uvicorn main:wdm --reload
```

The server will start running on `http://127.0.0.1:8000`.

## Endpoints

- `/products`: Get all products.
- `/product_by_id/{product_id}`: Get a product by ID.
- `/product_by_name/{product_name}`: Get products by name.
- `/products_by_root_category/{category}`: Get products by root category.
- `/products_by_main_category/{category}`: Get products by main category.
- `/products_by_subcategories/{category}`: Get products by subcategories.
- `/products_by_any_category/{category}`: Get products by any category.

- `/categories`: Get all categories.
- `/categories_by_root_cat/{name}`: Get categories by root category.
- `/categories_by_main_category/{name}`: Get categories by main category.
- `/categories_by_subcategories/{root_category}`: Get categories by subcategories.

- `/specs`: Get all specifications.
- `/specs_by_item_id/{item_id}`: Get specifications by item ID.
- `/specs_by_list_of_products`: Get specifications by list of products.

- `/types_specs`: Get all types specifications.
- `/types_specs_by_name/{name}`: Get types specifications by name.

## Examples

### Get all products

```bash
curl http://localhost:8000/products
```

This will return a list of all products in the table Products.

### Get a product by ID

```bash
curl http://localhost:8000/product_by_id/1938600000
```

### Get products by name

```bash
curl http://localhost:8000/product_by_name/SAI-AU M8 SB 8DI
```
Or **%20** for space in the name of the product
```bash
curl http://localhost:8000/product_by_name/SAI-AU%20M8%20SB%208DI
```

### Get products by root category

```bash
curl http://localhost:8000/products_by_root_category/electronics
```

### Get products by main category

```bash
curl http://localhost:8000/products_by_main_category/conectividad
```

### Get products by subcategories

```bash
curl http://localhost:8000/products_by_subcategories/sistemas%20de%20e+s
```

### Get products by any category

```bash
curl http://localhost:8000/products_by_any_category/["sistemas%20de%20e+s",%20"i+o%20system%20ip67%20-%20u-remote",%20"universal%20pro"]
```

## Authentication

This API currently does not support authentication. Ensure your server is properly secured before deploying it in production.


#### Additional Information

- The API offers various endpoints for retrieving product data based on different criteria, including product ID, name, category, and specifications.
- Ensure that you have the necessary permissions to access the PostgreSQL database where the product data is stored.
- This API is designed to facilitate the retrieval of WeidMuller product data for distributors and other interested parties.

---

Feel free to reach out for further assistance or inquiries regarding the API functionality or implementation details!
