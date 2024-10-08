from fastapi import APIRouter, Response, HTTPException
from schemas.sale import Sale, SaleSchema
from crud.crud_sales import CRUDsellsObject
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
def getSell(id_sell: str) -> list[Sale]:
    result = CRUDsellsObject.get_sell(id_sell=id_sell)
    if result:
        return result
    else:
        return []


@router.post("/postSale", response_model=SaleSchema)
def postSale(sale: SaleSchema) -> SaleSchema:
    result = CRUDsellsObject.create_sale(sale=sale)
    if type(result) is SaleSchema:
        return result
    else:
        raise HTTPException(status_code=500, detail=result)
