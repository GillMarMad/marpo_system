from fastapi import APIRouter, Response
from schemas.sells import Sell
from crud.crud_sells import CRUDsellsObject
from api.products.onlineShearch import getIdFromCode
from datetime import datetime
router = APIRouter()

# @router.post("/addProduct", response_model=Product)
# def addProduct(search : str) -> Product:
#     CRUDproductsObject.OpenConnection()
#     result = CRUDproductsObject.get_by_code(search)
#     CRUDproductsObject.CloseConnection()
#     return result


@router.post("/postSell", response_model=None)
def SetSell() -> str:
    CRUDsellsObject.OpenConnection()
    result = CRUDsellsObject.create_sell([])
    CRUDsellsObject.CloseConnection()
    return result



@router.post("/getSell", response_model=list[Sell])
def getSell(id_sell : str) -> list[Sell]:
    CRUDsellsObject.OpenConnection()
    result = CRUDsellsObject.get_sell(id_sell=id_sell)
    CRUDsellsObject.CloseConnection()
    if result:
        return result
    else:
        return []



    