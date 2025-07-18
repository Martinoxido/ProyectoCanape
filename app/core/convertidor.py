from PIL import Image
from docx2pdf import convert
from collections import namedtuple
import os
ResultadoPDF = namedtuple('ResultadoPDF', ['exito', 'ruta_pdf'])
def convertir_png(ruta_imagen_original, destino):
    with Image.open(ruta_imagen_original) as img:
                img = img.convert("RGBA")
                img.save(destino, "PNG")
def convertir_pdf(archivo, destino=None):
    try:
        if destino:
            convert(archivo, destino)
            ruta_pdf = destino
        else:
            convert(archivo)
            os.remove(archivo)
            ruta_pdf = archivo.replace(".docx", ".pdf")
        return ResultadoPDF(True, ruta_pdf)
    except Exception as e:
        print(e)
        return ResultadoPDF(False, None)

