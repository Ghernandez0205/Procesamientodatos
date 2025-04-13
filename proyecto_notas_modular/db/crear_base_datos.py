
import sqlite3

def crear_base_datos(ruta_db="notas.sqlite"):
    conn = sqlite3.connect(ruta_db)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS notas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            categoria TEXT,
            subcategoria TEXT,
            contenido TEXT,
            etiquetas TEXT,
            fecha TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS citas_apa (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nota_id INTEGER,
            tipo_fuente TEXT,
            autor TEXT,
            anio TEXT,
            titulo TEXT,
            revista TEXT,
            doi TEXT,
            editorial TEXT,
            ciudad TEXT,
            FOREIGN KEY(nota_id) REFERENCES notas(id)
        )
    """)

    conn.commit()
    conn.close()
