import psycopg2
from fastapi.encoders import jsonable_encoder
from typing import Optional


from core.config import settings
from schemas.poducts import Product as ProductSchema
from models.products import Product as ProductModel


class CRUDProducts():
    def __init__(self):
        self.connected = False
        self.conn = None
        self.cursor = None
        self.headers = ["key","code","codebar","codebarInner","codebarMaster","unit","description",
        "brand","buy","retailsale","wholesale","inventory","min_inventory","department","id","LastUpdate",]

    def OpenConnection(self):
        self.conn = psycopg2.connect(database=settings.POSTGRES_DB,
                        host=settings.POSTGRES_SERVER,
                        user=settings.POSTGRES_USER,
                        password=settings.POSTGRES_PASSWORD,
                        port=settings.POSTGRES_PORT)
        self.cursor = self.conn.cursor()
        self.connected = True

    def create_product(self, obj_in: ProductSchema):
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = [v for x,v in obj_in_data.items()]
        db_obj = tuple(db_obj)
        self.cursor.execute("""
               INSERT INTO product (key,code,codebar,codebarInner,codebarMaster,unit,description,brand,buy,
               retailsale,wholesale,inventory,min_inventory,department,id,LastUpdate) 
               VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);
               """,
               db_obj)
        self.conn.commit()
        return db_obj

    def get_by_codebars(self, search: str) -> Optional[ProductSchema]:
        self.cursor.execute(f"SELECT * FROM product WHERE codebar='{search}' OR codebarinner='{search}' OR codebarmaster='{search}'")
        obj_out = self.cursor.fetchone()
        if obj_out: 
            obj_out = {x:y for x,y in zip(self.headers, obj_out)}
            obj_out = ProductSchema(**obj_out)
        return obj_out
    
    
    def get_product(self, search: str) -> Optional[ProductSchema]:
        self.cursor.execute(f"SELECT * FROM product WHERE key='{search}' OR codebarinner='{search}' OR codebarmaster='{search}' OR description LIKE '{search}' OR department='{search}'")
        obj_out = self.cursor.fetchone()
        if obj_out: 
            obj_out = {x:y for x,y in zip(self.headers, obj_out)}
            obj_out = ProductSchema(**obj_out)
        return obj_out

    def update_acutal_by_id(self, id:str, actual:str) -> Optional[ProductModel]:
        self.cursor.execute(f"""
               UPDATE economiccalendar 
               SET actual='{actual}'
               WHERE id={id}
               """)
        self.conn.commit()
    
    def CloseConnection(self):
        self.cursor.close()
        self.conn.close()
        self.conn = None
        self.cursor = None
        self.connected = False

CRUDproductsObject = CRUDProducts()