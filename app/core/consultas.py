# core
import pandas as pd
import numpy as np
import os
import config.rutas
from PIL import Image
import shutil  # para copiar archivos sin modificar el original
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
        
def id_de(producto):
    
    for _, row in df.iterrows():
        if str(row["producto"]).lower() == producto.lower():
            return row["id"]
           
def editar_producto(producto, nuevoproducto, nuevoprecio):
    for i, row in df.iterrows():
        if (row["producto"]==producto):
            df.at[i,"producto"] = nuevoproducto
            df.at[i, "precio"]= nuevoprecio
            df.to_excel(ruta_productos, index=False)
            # Renombrar la imagen asociada, si existe
            base_path = os.path.join(config.rutas.BASE_PATH, "resources", "fotos")
            imagen_antigua = os.path.join(base_path, f"{producto}.png")
            imagen_nueva = os.path.join(base_path, f"{nuevoproducto}.png")

            if os.path.exists(imagen_antigua):
                os.rename(imagen_antigua, imagen_nueva)
                print(f"[OK] Imagen renombrada a {nuevoproducto}.png")
            else:
                print(f"[WARN] Imagen {producto}.png no encontrada para renombrar.")
            return True
    return False    



def agregar_producto_al_excel(nombre_nuevo, precio_nuevo, ruta_imagen_original=None):
    for i, row in df.iterrows():
        if pd.isna(row["id"]) and pd.isna(row["producto"]) and pd.isna(row["precio"]):
            id_nuevo = i + 1
            df.at[i, "id"] = id_nuevo
            df.at[i, "producto"] = nombre_nuevo
            df.at[i, "precio"] = precio_nuevo
            df.to_excel(ruta_productos, index=False)
            break
    else:
        id_max = df["id"].max()
        id_nuevo = int(id_max) + 1 if pd.notna(id_max) else 1
        df.loc[len(df)] = [id_nuevo, nombre_nuevo, precio_nuevo]
        df.to_excel(ruta_productos, index=False)

    base_path = os.path.join(config.rutas.BASE_PATH, "resources", "fotos")
    destino = os.path.join(base_path, f"{nombre_nuevo}.png")

    try:
        if ruta_imagen_original:
            # Copiar y convertir imagen pasada
            with Image.open(ruta_imagen_original) as img:
                img = img.convert("RGBA")
                img.save(destino, "PNG")
        else:
            # Copiar imagen genérica por defecto y renombrar
            imagen_default = os.path.join(base_path, "generica.png")
            shutil.copy(imagen_default, destino)

        print(f"[OK] Imagen guardada como {nombre_nuevo}.png")
    except Exception as e:
        print(f"[ERROR] No se pudo copiar/convertir la imagen: {e}")
        return False

    return True

    

def eliminar_producto_del_excel(id, producto, precio):

    for i, row in df.iterrows():
        if (row["id"]==id and row["producto"]==producto and row["precio"]==precio):
            # Encontró fila 
            df.at[i, "id"] = np.nan
            df.at[i, "producto"] = np.nan
            df.at[i, "precio"] = np.nan
            df.to_excel(ruta_productos, index=False)
            base_path = os.path.join(config.rutas.BASE_PATH, "resources", "fotos")
            imagen = os.path.join(base_path, f"{producto}.png")
            if os.path.exists(imagen):
                os.remove(imagen)
                print(f"[OK] Imagen eliminada a {producto}.png")
            else:
                print(f"[WARN] Imagen {producto}.png no encontrada para eliminar.")
            return True
       
        # Si no encontró la fila o no se logró borrar
    return False