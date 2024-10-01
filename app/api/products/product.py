from fastapi import APIRouter, Response, HTTPException
from schemas.products import Product
from crud.crud_products import CRUDproductsObject
from api.products.onlineShearch import getIdFromCode, getProductInfo
from datetime import datetime
from typing import List
router = APIRouter()

# @router.post("/addProduct", response_model=Product)
# def addProduct(search : str) -> Product:
#     CRUDproductsObject.OpenConnection()
#     result = CRUDproductsObject.get_by_code(search)
#     CRUDproductsObject.CloseConnection()
#     return result


@router.post("/getProduct", response_model=Product)
def getProduct(search: str) -> Product:
    result = CRUDproductsObject.get_by_codebars(search)
    if result:
        return result
    else:
        empty = Product(key="None", code=0, codebar="", codebarInner="", codebarMaster="", unit="", description="", brand="", buy=0,
                        retailsale=0, wholesale=0, inventory=0, min_inventory=0, department="", id=0, box=0, master=0, lastUpdate=datetime.now())
        return empty


@router.get("/searchProduct", response_model=List[Product])
async def search_product(search: str) -> List[Product]:
    try:
        # Realiza la consulta de forma asíncrona
        result = CRUDproductsObject.get_product(search)
    except Exception as e:
        raise HTTPException(status_code=500, detail=result)
        print(f"Error en la consulta: {e}")
        result = []

    if result:
        return result
    else:
        return []


@router.get("/getPDF", response_model=str)
def searchPDF(code: str) -> str:
    url = getProductInfo(code)
    if url:
        return url
    else:
        id = getIdFromCode(code=code)
        if id:
            url = f'https://www.truper.com/ficha_tecnica/views/ficha-print.php?id={id}'
        else:
            url = f'https://www.truper.com/ficha_merca/ficha-print.php?code={code.strip()}'
    return url


@router.get("/lastUpdatedProducts", response_model=list[Product])
def lastestProducts() -> Product:
    result = CRUDproductsObject.get_lastest_products()
    if result:
        return result
    else:
        return []


@router.get("/image/{image_name}")
async def download_product_image(image_name: str, response: Response):
    try:
        with open(f"assets/img/{image_name}.jpg", "rb") as f:
            image = f.read()
    except FileNotFoundError:
        with open(f"assets/img/shopping-cart.png", "rb") as f:
            image = f.read()
    response.body = image
    response.headers["Content-Type"] = "image/jpeg"
    response.status_code = 200
    return response


@router.get("/image/brand/{image_name}")
async def download_brand_image(image_name: str, response: Response):
    try:
        with open(f"assets/brands/{image_name}.png", "rb") as f:
            image = f.read()
        response.headers["Content-Type"] = "image/png"
    except FileNotFoundError:
        with open(f"assets/img/no-image.jpg", "rb") as f:
            image = f.read()
        response.headers["Content-Type"] = "image/jpeg"
    response.body = image
    response.status_code = 200
    return response



