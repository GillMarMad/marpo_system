import psycopg2
from fastapi.encoders import jsonable_encoder
from typing import Optional


from app.core.config import settings
from app.schemas.poducts import ProductSchema
from app.models.products import ProductModel


class CRUDProducts():
    def __init__(self):
        self.connected = False
        self.conn = None
        self.cursor = None
        self.headers = ["id","date","time","zone","currency","importance","event","actual","forecast","previous","timezone"]

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
               INSERT INTO economiccalendar (id, date, time, zone, currency, importance, event, actual, forecast, previous, timezone) 
               VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);
               """,
               db_obj)
        self.conn.commit()
        return db_obj

    def get_by_id(self, id: str) -> Optional[ProductModel]:
        self.cursor.execute(f"SELECT * FROM economiccalendar WHERE id={id}")
        obj_out = self.cursor.fetchone()
        if obj_out:
            obj_out = {x:y for x,y in zip(self.headers, obj_out)}
            obj_out = ProductModel(**obj_out)
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

products = CRUDProducts()