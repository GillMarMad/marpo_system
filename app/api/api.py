from fastapi import APIRouter
from .products import product
from .sells import sells

api_router = APIRouter()
api_router.include_router(product.router, tags=["products"])
api_router.include_router(sells.router, tags=["sells"])