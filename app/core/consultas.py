# core
import pandas as pd
import numpy as np
import os
import config.rutas
base_dir = os.path.dirname(os.path.abspath(__file__))
ruta_productos = os.path.join(config.rutas.BASE_PATH,"resources","datos","Productos.xlsx")
df = pd.read_excel(ruta_productos)

def listar_productos_excel():
    productos = []
    for _, row in df.iterrows():
        producto = {
            "id": row["id"],
            "nombre": row["producto"],
            "precio": row["precio"]
        }
        productos.append(producto)
    return productos

def precio_de(producto):
    
    for _, row in df.iterrows():
        if str(row["producto"]).lower() == producto.lower():
            return row["precio"]
           
def editar_precio_de(producto, precio):
    for i, row in df.iterrows():
        if (row["producto"]==producto):
            df.at[i, "precio"]= precio
            return True
    return False    

def agregar_producto_al_excel(nombre_nuevo, precio_nuevo):

    for i, row in df.iterrows():
        if pd.isna(row["id"]) and pd.isna(row["producto"]) and pd.isna(row["precio"]):
            # Encontró fila vacía completa
            
            df.at[i, "id"] = i+1
            df.at[i, "producto"] = nombre_nuevo
            df.at[i, "precio"] = precio_nuevo
            df.to_excel(ruta_productos, index=False)
            return True
        else:
            # Si no encontró fila vacía, agregar al final
            id_max = df["id"].max()
            id_nuevo = int(id_max) + 1 if pd.notna(id_max) else 1
            df.loc[len(df)] = [id_nuevo, nombre_nuevo, precio_nuevo]
            df.to_excel(ruta_productos, index=False)
            return True
    return False
    

def eliminar_producto_del_excel(id, producto, precio):

    for i, row in df.iterrows():
        if (row["id"]==id and row["producto"]==producto and row["precio"]==precio):
            # Encontró fila 
            df.at[i, "id"] = np.nan
            df.at[i, "producto"] = np.nan
            df.at[i, "precio"] = np.nan
            df.to_excel(ruta_productos, index=False)
            return True
       
        # Si no encontró la fila o no se logró borrar
    return False