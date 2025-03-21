from datetime import datetime
from psycopg2 import sql
from fastapi.encoders import jsonable_encoder
from typing import Optional, List

from schemas.products import Product as ProductSchema
from models.products import Product as ProductModel
from crud.db import get_connection, release_connection


class CRUDProducts:
    def __init__(self):
        self.headers = [
            "id", "key", "code", "codebar", "codebarInner", "codebarMaster", "unit", "description",
            "brand", "buy", "retailsale", "wholesale", "inventory", "min_inventory",
            "department", "origin_id", "box", "master", "lastUpdate",
        ]

    def create_product(self, obj_in: ProductSchema):
        obj_in_data = jsonable_encoder(obj_in)
        conn = get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT MAX(id) FROM products")
                max_id = cursor.fetchone()[0] or 0
                obj_in_data["id"] = max_id + 1
                db_obj = [v for x, v in obj_in_data.items()]
                db_obj = tuple(db_obj)
                insert_query = """
                    INSERT INTO products (
                        id, key, code, codebar, codebarInner, codebarMaster, unit, description, brand, buy,
                        retailsale, wholesale, inventory, min_inventory, department, box, master, origin_id, lastupdate
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                """
                cursor.execute(insert_query, db_obj)
                conn.commit()
                return db_obj
        except Exception as e:
            conn.rollback()
            print(f"Error creando producto: {e}")
            raise
        finally:
            release_connection(conn)

    def get_product_by_id(self, id: int) -> Optional[ProductSchema]:
        conn = get_connection()
        try:
            with conn.cursor() as cursor:
                query = "SELECT * FROM products WHERE id = %s"
                cursor.execute(query, (id,))
                obj_out = cursor.fetchone()
                if obj_out:
                    obj_out = {x: y for x, y in zip(self.headers, obj_out)}
                    return ProductSchema(**obj_out)
                return None
        except Exception as e:
            print(f"Error obteniendo producto por ID: {e}")
            raise
        finally:
            release_connection(conn)

    def update_stock(self, id: int, quantity: float):
        conn = get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT inventory FROM products WHERE id = %s", (id,))
                result = cursor.fetchone()
                if result is None:
                    print(f"No se encontró el producto con ID {id}")
                    return False
                inventory = result[0] + quantity
                update_query = "UPDATE products SET inventory = %s, lastupdate = %s WHERE id = %s"
                cursor.execute(update_query, (inventory, datetime.now(), id))
                conn.commit()
                return True
        except Exception as e:
            conn.rollback()
            print(f"Error actualizando stock: {e}")
            return False
        finally:
            release_connection(conn)

    def get_by_codebars(self, search: str) -> Optional[ProductSchema]:
        conn = get_connection()
        try:
            with conn.cursor() as cursor:
                query = """
                    SELECT * FROM products 
                    WHERE codebar = %s OR codebarinner = %s OR codebarmaster = %s
                """
                cursor.execute(query, (search, search, search))
                obj_out = cursor.fetchone()
                if obj_out:
                    obj_out = {x: y for x, y in zip(self.headers, obj_out)}
                    return ProductSchema(**obj_out)
                return None
        except Exception as e:
            print(f"Error obteniendo producto por codebars: {e}")
            raise
        finally:
            release_connection(conn)

    def get_by_codebar(self, search: str) -> Optional[ProductSchema]:
        conn = get_connection()
        try:
            with conn.cursor() as cursor:
                query = "SELECT * FROM products WHERE codebar = %s"
                cursor.execute(query, (search,))
                obj_out = cursor.fetchone()
                if obj_out:
                    obj_out = {x: y for x, y in zip(self.headers, obj_out)}
                    return ProductSchema(**obj_out)
                return None
        except Exception as e:
            print(f"Error obteniendo producto por codebar: {e}")
            raise
        finally:
            release_connection(conn)

    def get_product(self, search: str) -> List[ProductSchema]:
        conn = get_connection()
        try:
            with conn.cursor() as cursor:
                query = sql.SQL("""
                    -- Crear extensión unaccent si no existe
                    CREATE EXTENSION IF NOT EXISTS unaccent;

                    -- Consulta de búsqueda
                    WITH ranked_products AS (
                        SELECT *,
                            ts_rank_cd(
                                to_tsvector('spanish', unaccent(description)),
                                phraseto_tsquery('spanish', unaccent(%s) || ':*')
                            ) AS rank
                        FROM products
                        WHERE to_tsvector('spanish', unaccent(description)) @@ phraseto_tsquery('spanish', unaccent(%s) || ':*')
                            OR code = %s
                            OR key = UPPER(%s)
                            OR key = LOWER(%s)
                    )
                    SELECT *
                    FROM ranked_products
                    ORDER BY
                        rank DESC,
                        CASE
                            WHEN unaccent(description) ILIKE unaccent(%s || '%%') THEN 0
                            WHEN unaccent(description) ILIKE unaccent('%%' || %s) THEN 1
                            WHEN unaccent(description) ILIKE unaccent('%%' || %s || '%%') THEN 2
                            ELSE 3
                        END;
                """)
                params = (search, search, search, search, search, search, search, search)
                cursor.execute(query, params)
                products = []
                if cursor.rowcount > 0:
                    obj_out = cursor.fetchall()
                    for product in obj_out:
                        p = {x: y for x, y in zip(self.headers, product)}
                        p = ProductSchema(**p)
                        products.append(p)
                return products
        except Exception as e:
            conn.rollback()
            print(f"Error obteniendo productos: {e}")
            raise
        finally:
            release_connection(conn)

    def get_latest_products(self) -> List[ProductSchema]:
        conn = get_connection()
        try:
            with conn.cursor() as cursor:
                query = """
                    SELECT *
                    FROM products
                    ORDER BY LastUpdate DESC
                    LIMIT 50;
                """
                cursor.execute(query)
                products = []
                if cursor.rowcount > 0:
                    obj_out = cursor.fetchall()
                    for product in obj_out:
                        p = {x: y for x, y in zip(self.headers, product)}
                        p = ProductSchema(**p)
                        products.append(p)
                return products
        except Exception as e:
            print(f"Error obteniendo últimos productos: {e}")
            raise
        finally:
            release_connection(conn)

    def update_product(self, codebar: str, obj_in: ProductSchema) -> Optional[ProductModel]:
        conn = get_connection()
        try:
            with conn.cursor() as cursor:
                update_query = """
                    UPDATE products
                    SET key = %s,
                        code = %s,
                        codebarInner = %s,
                        codebarMaster = %s,
                        unit = %s,
                        brand = %s,
                        buy = %s,
                        retailsale = %s,
                        wholesale = %s,
                        inventory = %s,
                        min_inventory = %s
                    WHERE codebar = %s;
                """
                values = (
                    obj_in.key,
                    obj_in.code,
                    obj_in.codebarInner,
                    obj_in.codebarMaster,
                    obj_in.unit,
                    obj_in.brand,
                    obj_in.buy,
                    obj_in.retailsale,
                    obj_in.wholesale,
                    obj_in.inventory,
                    obj_in.min_inventory,
                    codebar
                )
                cursor.execute(update_query, values)
                conn.commit()
                print(f"Product updated: {obj_in.code}")
                return None  # Ajusta según tu lógica
        except Exception as e:
            conn.rollback()
            print(f"Error actualizando producto: {e}")
            raise
        finally:
            release_connection(conn)


CRUDproductsObject = CRUDProducts()
