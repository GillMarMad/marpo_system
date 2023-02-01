from fastapi import APIRouter
from schemas.poducts import Product
from crud.crud_products import CRUDproductsObject
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


@router.post("/searchProduct", response_model=list[Product])
def searchProduct(search : str) -> Product:
    CRUDproductsObject.OpenConnection()
    result = CRUDproductsObject.get_product(search)
    CRUDproductsObject.CloseConnection()
    if result:
        return result
    else:
        return []

