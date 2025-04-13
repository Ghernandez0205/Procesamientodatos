
import sqlite3
from datetime import datetime

def guardar_en_sqlite(categoria, subcategoria, contenido, etiquetas, cita_data=None, ruta_db="notas.sqlite"):
    conn = sqlite3.connect(ruta_db)
    cursor = conn.cursor()

    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("INSERT INTO notas (categoria, subcategoria, contenido, etiquetas, fecha) VALUES (?, ?, ?, ?, ?)",
                   (categoria, subcategoria, contenido, etiquetas, fecha))
    nota_id = cursor.lastrowid

    if cita_data:
        cursor.execute("""
            INSERT INTO citas_apa (nota_id, tipo_fuente, autor, anio, titulo, revista, doi, editorial, ciudad)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            nota_id,
            cita_data.get("tipo_fuente"),
            cita_data.get("autor"),
            cita_data.get("anio"),
            cita_data.get("titulo"),
            cita_data.get("revista"),
            cita_data.get("doi"),
            cita_data.get("editorial"),
            cita_data.get("ciudad")
        ))

    conn.commit()
    conn.close()
    return nota_id
