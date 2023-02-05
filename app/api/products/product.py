from fastapi import APIRouter, Response
from schemas.poducts import Product
from crud.crud_products import CRUDproductsObject
from api.products.onlineShearch import getIdFromCode
from datetime import datetime
router = APIRouter()

# @router.post("/addProduct", response_model=Product)
# def addProduct(search : str) -> Product:
#     CRUDproductsObject.OpenConnection()
#     result = CRUDproductsObject.get_by_code(search)
#     CRUDproductsObject.CloseConnection()
#     return result


@router.post("/getProduct", response_model=Product)
def getProduct(search : str) -> Product:
    CRUDproductsObject.OpenConnection()
    result = CRUDproductsObject.get_by_codebars(search)
    CRUDproductsObject.CloseConnection()
    if result:
        return result
    else:
        empty = Product(key="None", code=0, codebar="", codebarInner="", codebarMaster="", unit="", description="", brand="", buy=0,retailsale=0,wholesale=0,inventory=0, min_inventory=0,department="",id=0,LastUpdate=datetime.now())
        return empty


@router.get("/searchProduct", response_model=list[Product])
def searchProduct(search : str) -> Product:
    CRUDproductsObject.OpenConnection()
    result = CRUDproductsObject.get_product(search)
    CRUDproductsObject.CloseConnection()
    if result:
        return result
    else:
        return []

@router.get("/getPDF", response_model=str)
def searchPDF(code : str) -> Product:
    id = getIdFromCode(code=code)
    if id:
        url = f'https://www.truper.com/ficha_tecnica/views/ficha-print.php?id={id}'
    else:
        url = f'https://www.truper.com/ficha_merca/ficha-print.php?code={code.strip()}'
    return url


@router.get("/image/{image_name}")
async def download_product_image(image_name: str, response: Response):
    try:
        with open(f"assets/img/{image_name}.jpg", "rb") as f:
            image = f.read()
    except FileNotFoundError:
        with open(f"assets/img/no-image.jpg", "rb") as f:
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



    