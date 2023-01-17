from fastapi import APIRouter
from .products import product

api_router = APIRouter()
api_router.include_router(product.router, tags=["product"])