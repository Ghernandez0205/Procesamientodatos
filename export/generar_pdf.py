
from fpdf import FPDF
import sqlite3
from datetime import datetime

def generar_pdf(nombre_archivo="resumen_notas.pdf", db_path="notas.sqlite"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "Resumen de Notas", ln=True, align="C")
    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 10, f"Generado el {datetime.now().strftime('%d/%m/%Y %H:%M')}", ln=True)

    pdf.ln(10)
    cursor.execute("SELECT id, categoria, subcategoria, contenido, etiquetas, fecha FROM notas")
    notas = cursor.fetchall()

    for nota in notas:
        id_, cat, subcat, cont, etiq, fecha = nota
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 10, f"[{cat} | {subcat}] - {fecha}", ln=True)
        pdf.set_font("Arial", "", 11)
        pdf.multi_cell(0, 8, f"{cont}\nEtiquetas: {etiq}")
        pdf.ln(4)

        cursor.execute("SELECT tipo_fuente, autor, anio, titulo, revista, doi, editorial, ciudad FROM citas_apa WHERE nota_id=?", (id_,))
        cita = cursor.fetchone()
        if cita:
            tipo, autor, anio, titulo, revista, doi, editorial, ciudad = cita
            pdf.set_font("Arial", "I", 11)
            pdf.set_text_color(80, 80, 80)
            if tipo == "Artículo":
                pdf.multi_cell(0, 7, f"{autor} ({anio}). {titulo}. *{revista}*. https://doi.org/{doi}")
            else:
                pdf.multi_cell(0, 7, f"{autor} ({anio}). {titulo}. {ciudad}: {editorial}")
            pdf.set_text_color(0, 0, 0)
            pdf.ln(4)

    pdf.output(nombre_archivo)
    conn.close()
    return nombre_archivo
