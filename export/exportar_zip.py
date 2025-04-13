
import zipfile
import os
from datetime import datetime

def exportar_a_zip(pdf_path="resumen_notas.pdf", db_path="notas.sqlite", media_folder="media"):
    fecha = datetime.now().strftime("%Y-%m-%d")
    nombre_zip = f"exportacion_{fecha}.zip"

    with zipfile.ZipFile(nombre_zip, "w", zipfile.ZIP_DEFLATED) as zipf:
        zipf.write(db_path, arcname="notas.sqlite")
        zipf.write(pdf_path, arcname="resumen_notas.pdf")

        for carpeta_raiz, subdirs, archivos in os.walk(media_folder):
            for archivo in archivos:
                ruta_completa = os.path.join(carpeta_raiz, archivo)
                ruta_dentro_zip = os.path.relpath(ruta_completa, start=media_folder)
                zipf.write(ruta_completa, arcname=f"media/{ruta_dentro_zip}")

    return nombre_zip
