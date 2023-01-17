from fastapi import APIRouter
from schemas import poducts

router = APIRouter()

@router.post("/addProduct", response_model=poducts.Product)
def addProduct():
    pass