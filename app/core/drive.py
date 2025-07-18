from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
import os
import config.rutas as rt

TOKEN_PATH = os.path.join(rt.BASE_PATH, "resources", "secret", "token.json")
CLIENT_SECRET_PATH = os.path.join(rt.BASE_PATH, "resources", "secret", "pepito.json")  # debe ser JSON, no XLSX

def autenticar_drive():
    gauth = GoogleAuth()
    gauth.LoadClientConfigFile(CLIENT_SECRET_PATH)

    if os.path.exists(TOKEN_PATH):
        try:
            gauth.LoadCredentialsFile(TOKEN_PATH)
        except Exception:
            os.remove(TOKEN_PATH)  # eliminar token corrupto si existe

    if not gauth.credentials or gauth.access_token_expired:
        gauth.LocalWebserverAuth()
        gauth.SaveCredentialsFile(TOKEN_PATH)

    return GoogleDrive(gauth)

def subir_a_drive(ruta_archivo, nombre_archivo=None):
    try:
        drive = autenticar_drive()

        if not nombre_archivo:
            nombre_archivo = os.path.basename(ruta_archivo)

        archivo_drive = drive.CreateFile({'title': nombre_archivo})
        archivo_drive.SetContentFile(ruta_archivo)
        archivo_drive.Upload()

        print(f"✅ Archivo '{nombre_archivo}' subido correctamente a Drive.")
        return True
    except Exception as e:
        print(f"❌ Error al subir a Drive: {e}")
        return False
