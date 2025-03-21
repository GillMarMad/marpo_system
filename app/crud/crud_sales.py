from datetime import datetime
import psycopg2


from core.config import settings
from schemas.products import Product as ProductSchema
from crud.crud_products import CRUDproductsObject
from schemas.sale import SaleSchema as SaleSchema
from schemas.sale import SaleDetail as SaleDetailSchema
# from schemas.sale import SellProduct as SellProductSchema
# from models.products import Product as ProductModel
# from models.sells import Sells as SellModel


class CRUDSells():
    def __init__(self):
        self.connected = False
        self.conn = None
        self.cursor = None
        self.headers_sale = ["id", "sale_id", "product_id", "quantity", "total_price", "created_at", "updated_at", "sell_price", "buy_price"]
        self.crudeProducts = CRUDproductsObject

    def OpenConnection(self):
        self.conn = psycopg2.connect(database=settings.POSTGRES_DB,
                                     host=settings.POSTGRES_SERVER,
                                     user=settings.POSTGRES_USER,
                                     password=settings.POSTGRES_PASSWORD,
                                     port=settings.POSTGRES_PORT)
        self.cursor = self.conn.cursor()
        self.connected = True

    def create_sale(self, sale: SaleSchema):
        for s in sale.products:
            self.cursor.execute(f"SELECT * FROM products WHERE id='{s.product_id}'")
            obj_out = self.cursor.fetchone()
            if obj_out:
                obj_out = {x: y for x, y in zip(self.crudeProducts.headers, obj_out)}
                obj_out = ProductSchema(**obj_out)
            else:
                return "Producto no encontrado"
            if obj_out.inventory < s.quantity:
                return f"Producto {obj_out.description} sin stock suficiente"

        sale_query = f"INSERT INTO sales (seller,costumer,total,date) VALUES ('{sale.seller}','{sale.costumer}','{sale.total}','{datetime.now()}')"
        self.cursor.execute(sale_query)
        self.conn.commit()
        self.cursor.execute("SELECT MAX(id) FROM sales")
        last_id = self.cursor.fetchone()[0]
        if not last_id:
            return "No se encontró el id de la venta"
        # self.crudeProducts.OpenConnection()
        for s in sale.products:
            self.cursor.execute(f"SELECT * FROM products WHERE id='{s.product_id}'")
            obj_out = self.cursor.fetchone()
            if obj_out:
                obj_out = {x: y for x, y in zip(self.crudeProducts.headers, obj_out)}
                obj_out = ProductSchema(**obj_out)
            sale_detail_query = f"""
            INSERT INTO sales_details (sale_id,product_id,quantity,sell_price,buy_price,total_price,created_at,updated_at) 
            VALUES ('{last_id}','{obj_out.id}','{s.quantity}','{s.sell_price}','{obj_out.buy}','{s.quantity*s.sell_price}','{datetime.now()}','{datetime.now()}')
            """
            try:
                self.cursor.execute(sale_detail_query)
            except:
                return "Error creando detalle de venta"

            self.conn.commit()
            update_stock = self.crudeProducts.update_stock(s.product_id, -s.quantity)
            if not update_stock:
                return "Error updating stock"
        # self.crudeProducts.CloseConnection()
        return SaleSchema(**sale.dict())

    def get_sell(self, id_sell: int) -> list[SaleDetailSchema]:
        self.cursor.execute(f"SELECT * FROM sales_details WHERE sale_id='{id_sell}'")
        sells = []
        if self.cursor and self.cursor.rowcount > 0:
            obj_out = self.cursor.fetchall()
            if obj_out:
                for product in obj_out:
                    p = {x: y for x, y in zip(self.headers_sale, product)}
                    p = SaleDetailSchema(**p)
                    sells.append(p)
        return sells

        # consulta= f"""
        # SELECT p.*
        # FROM product p
        # JOIN sells c ON p.key = c.id_producto
        # WHERE c.id_compra = {id_sell};
        # """
        # self.cursor.execute(consulta)
        # products = []
        # if self.cursor and self.cursor.rowcount > 0:
        #     obj_out = self.cursor.fetchall()
        #     if obj_out:
        #         for product in obj_out:
        #             p = {x:y for x,y in zip(self.headers_product, product)}
        #             p = ProductSchema(**p)
        #             products.append(p)
        # return products

    def CloseConnection(self):
        self.conn.rollback()
        self.cursor.close()
        self.conn.close()
        self.conn = None
        self.cursor = None
        self.connected = False


CRUDsellsObject = CRUDSells()
