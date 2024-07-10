from fastapi import APIRouter, Response
from schemas.sale import Sale
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


# @router.post("/postSell", response_model=dict)
# def SetSell(products : list[SellProduct]) -> dict:
#     CRUDsellsObject.OpenConnection()
#     result = CRUDsellsObject.create_sell(products=products)
#     CRUDsellsObject.CloseConnection()
#     return result



@router.post("/getSell", response_model=list[Sale])
def getSell(id_sell : str) -> list[Sale]:
    CRUDsellsObject.OpenConnection()
    result = CRUDsellsObject.get_sell(id_sell=id_sell)
    CRUDsellsObject.CloseConnection()
    if result:
        return result
    else:
        return []



    