from datetime import datetime
import psycopg2
from fastapi.encoders import jsonable_encoder
from typing import Optional


from core.config import settings
from schemas.poducts import Product as ProductSchema
from models.products import Product as ProductModel


class CRUDSells():
    def __init__(self):
        self.connected = False
        self.conn = None
        self.cursor = None
        self.headers_sell = ["id_compra","id_producto","cantidad","date",]
        self.headers_product = ["key","code","codebar","codebarInner","codebarMaster","unit","description",
        "brand","buy","retailsale","wholesale","inventory","min_inventory","department","id","box","master","lastUpdate",]

    def OpenConnection(self):
        self.conn = psycopg2.connect(database=settings.POSTGRES_DB,
                        host=settings.POSTGRES_SERVER,
                        user=settings.POSTGRES_USER,
                        password=settings.POSTGRES_PASSWORD,
                        port=settings.POSTGRES_PORT)
        self.cursor = self.conn.cursor()
        self.connected = True

    def create_sell(self, products_key: dict[str]):
        try:
            products = {'SUD-GD-G':{'retail':True, 'amount':1},'SOT-250CL':{'retail':True, 'amount':1},'SOMU-250X':{'retail':True, 'amount':1},'SET-73':{'retail':True, 'amount':1},'ROTO-1/2N6':{'retail':True, 'amount':1}}
            prices = {}
            for p in products.keys:
                self.cursor.execute(f"SELECT * FROM product WHERE key='{p}'")
                obj_out = self.cursor.fetchone()
                if obj_out: 
                    obj_out = {x:y for x,y in zip(self.headers, obj_out)}
                    obj_out = ProductSchema(**obj_out)
                prices[p] = {'amount':products[p]['amount'],
                             'sell_price': obj_out.retailsale if products[p]['retail'] else obj_out.wholesale,
                             'buy_price' : obj_out.buy,
                             }
            consulta = "INSERT INTO sells (id_sell,id_product, amount, sell_price,buy_price,total,date) VALUES "
            id_generated = int(datetime.now().timestamp())
            print(id_generated)
            valores = ", ".join([f"('{id_generated}','{p}', '{prices[p]['amount']}', '{prices[p]['sell_price']}', '{prices[p]['buy_price']}','{prices[p]['amount']*prices[p]['sell_price']}','{datetime.now()}')" for p in prices.keys()])
            consulta += valores + ";"
            self.cursor.execute(consulta)
            self.conn.commit()
            return {"mensaje": "Sell send succesfully", "status_code": 200}
        except:
             return {"mensaje": "Error", "status_code": 404}

    def get_sell(self, id_sell: int) -> list[ProductSchema]:
        consulta = f"""
        SELECT p.*
        FROM product p
        JOIN sells c ON p.key = c.id_producto
        WHERE c.id_compra = {id_sell};
        """
        self.cursor.execute(consulta)
        products = []
        if self.cursor and self.cursor.rowcount > 0:
            obj_out = self.cursor.fetchall()
            if obj_out:
                for product in obj_out:
                    p = {x:y for x,y in zip(self.headers_product, product)}
                    p = ProductSchema(**p)
                    products.append(p)
        return products
    
    
    
    
    
    def get_by_codebars(self, search: str) -> Optional[ProductSchema]:
        self.cursor.execute(f"SELECT * FROM product WHERE codebar='{search}' OR codebarinner='{search}' OR codebarmaster='{search}'")
        obj_out = self.cursor.fetchone()
        if obj_out: 
            obj_out = {x:y for x,y in zip(self.headers, obj_out)}
            obj_out = ProductSchema(**obj_out)
        return obj_out
    
    def get_by_codebar(self, search: str) -> Optional[ProductSchema]:
        self.cursor.execute(f"SELECT * FROM product WHERE codebar='{search}'")
        obj_out = self.cursor.fetchone()
        if obj_out: 
            obj_out = {x:y for x,y in zip(self.headers, obj_out)}
            obj_out = ProductSchema(**obj_out)
        return obj_out
    
    
    def get_product(self, search: str) -> list[ProductSchema]:
        query = f"""
        CREATE EXTENSION IF NOT EXISTS unaccent;
        SELECT *
        FROM product
        WHERE code='{search}' OR key=UPPER('{search}') OR key=LOWER('{search}') OR unaccent(description) ILIKE unaccent('%{search}%')
        ORDER BY
            CASE
                WHEN unaccent(description) ILIKE unaccent('{search}%')THEN 0
                WHEN unaccent(description) ILIKE unaccent('%{search}')THEN 1
                WHEN unaccent(description) ILIKE unaccent('%{search}%') THEN 2
                ELSE 3
            END,
            similarity(description, unaccent('{search}')) DESC;
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
        FROM product
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
               UPDATE product
               SET key='{obj_in.key}',code={obj_in.code},codebarInner={obj_in.codebarInner},codebarMaster={obj_in.codebarMaster},unit='{obj_in.unit}',brand='{obj_in.brand}',buy={obj_in.buy},
               retailsale={obj_in.retailsale},wholesale={obj_in.wholesale},inventory={obj_in.inventory},min_inventory={obj_in.min_inventory}
               WHERE codebar='{codebar}';
               """
        try:
            self.cursor.execute(x)
        except:
            print(x)
        self.conn.commit()
    
    def CloseConnection(self):
        self.conn.rollback()
        self.cursor.close()
        self.conn.close()
        self.conn = None
        self.cursor = None
        self.connected = False

CRUDsellsObject = CRUDSells()