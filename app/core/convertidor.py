from PIL import Image
from docx2pdf import convert
import os
def convertir_png(ruta_imagen_original, destino):
    with Image.open(ruta_imagen_original) as img:
                img = img.convert("RGBA")
                img.save(destino, "PNG")
def convertir_pdf (archivo, destino=None):
    try:
        if(destino is not None):
            convert(archivo, destino)
        else:
            convert(archivo)
            os.remove(archivo)
        return True
    except Exception as e:
        print(e)
        return False

