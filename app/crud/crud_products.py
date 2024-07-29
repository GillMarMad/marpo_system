from datetime import datetime
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
        self.headers = ["id","key","code","codebar","codebarInner","codebarMaster","unit","description",
        "brand","buy","retailsale","wholesale","inventory","min_inventory","department","origin_id","box","master","lastUpdate",]

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
        self.cursor.execute("SELECT MAX(id) FROM products")
        obj_in_data["id"] = self.cursor.fetchone()[0] + 1
        db_obj = [v for x,v in obj_in_data.items()]
        db_obj = tuple(db_obj)
        self.cursor.execute("""
               INSERT INTO products (id,key,code,codebar,codebarInner,codebarMaster,unit,description,brand,buy,
               retailsale,wholesale,inventory,min_inventory,department,box,master,origin_id,LastUpdate) 
               VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);
               """,
               db_obj)
        self.conn.commit()
        return db_obj
    
    def get_product_by_id(self, id: int) -> Optional[ProductSchema]:
        self.cursor.execute(f"SELECT * FROM products WHERE id={id}")
        obj_out = self.cursor.fetchone()
        if obj_out: 
            obj_out = {x:y for x,y in zip(self.headers, obj_out)}
            obj_out = ProductSchema(**obj_out)
        return obj_out
    
    def upgdate_stock(self, id:int, quantity:float):
        try:
            self.cursor.execute(f"SELECT inventory FROM products WHERE id={id}")
            inventory = self.cursor.fetchone()[0]
            inventory += quantity
            query = "UPDATE products SET inventory = %s, lastupdate = %s WHERE id = %s"
            values = (inventory, datetime.now(), id)
            self.cursor.execute(query, values)
            self.conn.commit()
            return True
        except:
            print("Error updating stock")
            return None

    
    def get_by_codebars(self, search: str) -> Optional[ProductSchema]:
        self.cursor.execute(f"SELECT * FROM products WHERE codebar='{search}' OR codebarinner='{search}' OR codebarmaster='{search}'")
        obj_out = self.cursor.fetchone()
        if obj_out: 
            obj_out = {x:y for x,y in zip(self.headers, obj_out)}
            obj_out = ProductSchema(**obj_out)
        return obj_out
    
    def get_by_codebar(self, search: str) -> Optional[ProductSchema]:
        self.cursor.execute(f"SELECT * FROM products WHERE codebar='{search}'")
        obj_out = self.cursor.fetchone()
        if obj_out: 
            obj_out = {x:y for x,y in zip(self.headers, obj_out)}
            obj_out = ProductSchema(**obj_out)
        return obj_out
    
    
    def get_product(self, search: str) -> list[ProductSchema]:
        query = f"""
        -- Crear extensión unaccent si no existe
        CREATE EXTENSION IF NOT EXISTS unaccent;

        -- Consulta de búsqueda
        WITH ranked_products AS (
            SELECT *,
                ts_rank_cd(to_tsvector('spanish', unaccent(description)), plainto_tsquery('spanish', unaccent('{search}'))) AS rank
            FROM products
            WHERE to_tsvector('spanish', unaccent(description)) @@ plainto_tsquery('spanish', unaccent('{search}'))
                OR code = '{search}'
                OR key = UPPER('{search}')
                OR key = LOWER('{search}')
        )
        SELECT *
        FROM ranked_products
        ORDER BY
            rank DESC,
            CASE
                WHEN unaccent(description) ILIKE unaccent('{search}' || '%') THEN 0
                WHEN unaccent(description) ILIKE unaccent('%' || '{search}') THEN 1
                WHEN unaccent(description) ILIKE unaccent('%' || '{search}' || '%') THEN 2
                ELSE 3
            END;

        """
        self.cursor.execute(query=query)
        products = []
        if self.cursor and self.cursor.rowcount > 0:
            obj_out = self.cursor.fetchall()
            if obj_out:
                for product in obj_out:
                    p = {x:y for x,y in zip(self.headers, product)}
                    p = ProductSchema(**p)
                    products.append(p)
        return products
    
    def get_lastest_products(self) -> list[ProductSchema]:
        query = f"""
        SELECT *
        FROM products
        ORDER BY LastUpdate DESC
        LIMIT 50;
        """
        self.cursor.execute(query=query)
        products = []
        if self.cursor and self.cursor.rowcount > 0:
            obj_out = self.cursor.fetchall()
            if obj_out:
                for product in obj_out:
                    p = {x:y for x,y in zip(self.headers, product)}
                    p = ProductSchema(**p)
                    products.append(p)
        return products

    
    def update_product(self, codebar:str, obj_in:ProductSchema) -> Optional[ProductModel]:
        x = f"""
               UPDATE products
               SET key='{obj_in.key}',code={obj_in.code},codebarInner={obj_in.codebarInner},codebarMaster={obj_in.codebarMaster},unit='{obj_in.unit}',brand='{obj_in.brand}',buy={obj_in.buy},
               retailsale={obj_in.retailsale},wholesale={obj_in.wholesale},inventory={obj_in.inventory},min_inventory={obj_in.min_inventory}
               WHERE codebar='{codebar}';
               """
        try:
            self.cursor.execute(x)
            print(f"Product updated: {obj_in.code}")
        except:
            print(x)
        self.conn.commit()
        print(f"Product updated: {obj_in.code}")
    
    def CloseConnection(self):
        self.conn.rollback()
        self.cursor.close()
        self.conn.close()
        self.conn = None
        self.cursor = None
        self.connected = False

CRUDproductsObject = CRUDProducts()