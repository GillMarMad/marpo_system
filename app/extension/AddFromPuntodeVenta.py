import time
from datetime import datetime
import pandas as pd

from crud.crud_products import CRUDproductsObject
from schemas.products import Product as ProductSchema


def addData():
    db = CRUDproductsObject

    # cursor.execute("DELETE FROM product *")
    # conn.commit()

    file_path = "C:/Users/gilis/Downloads/respaldo28julio2024.csv"
    data = pd.read_csv(file_path)
    start_time = time.time()

    for index, row in data.iterrows():
        db.OpenConnection()
        # print(row['Codigo'] + " " + row['Descripcion'])

        r = db.get_by_codebar(row['Codigo'])
        if r:
            # pass
            aux = r
            aux.min_inventory = int(row['Inv. Minimo'])
            aux.retailsale = float(row['Precio Venta'])
            aux.wholesale = float(row['Precio Mayoreo'])
            if row['Inv. Minimo'] == 'nan':
                print(row['Inv. Minimo'])
            else:
                # print(f"No es nan {row['Inv. Minimo']}")
                aux.inventory = row['Inv. Minimo']
            aux.lastUpdate = datetime.now
            update = db.update_product(row['Codigo'], aux)
            if update:
                print("Product updated")
                print(f"Product: {row['Codigo']} - {row['Descripcion']} - {row['Precio Venta']} - {row['Precio Mayoreo']} - {row['Inv. Minimo']}")
        else:
            p = ProductSchema(id=0, key=str(row['Codigo']), code=str(row['Codigo']),
                              codebar=str(row['Codigo']), codebarInner=str(f"{row['Codigo']}6"),
                              codebarMaster=str(f"{row['Codigo']}12"), unit="Pieza",
                              description=str(row['Descripcion']), brand="",
                              buy=float(row['Precio Costo']), retailsale=float(row['Precio Venta']),
                              wholesale=float(row['Precio Mayoreo']),
                              inventory=int(row['Inv. Minimo']), min_inventory=0,
                              department=str(row['Departamento']), box=int(0), master=int(0),
                              lastUpdate=datetime.now(),
                              origin_id=int(0),
                              )
            create = db.create_product(obj_in=p)
            if create:
                print("Product added")
                print(f"Product: {row['Codigo']} - {row['Descripcion']} - {row['Precio Venta']} - {row['Precio Mayoreo']} - {row['Inv. Minimo']}")

        db.CloseConnection()

    print(f"----- Uploading Data to DB Finished ----- {time.time() - start_time} s")
