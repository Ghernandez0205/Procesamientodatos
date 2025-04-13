
import streamlit as st
import os
from datetime import datetime
from db.guardar_en_sqlite import guardar_en_sqlite
from export.generar_pdf import generar_pdf
from export.exportar_zip import exportar_a_zip

# --- CONFIGURACIÓN GENERAL ---
st.set_page_config(page_title="Gestor de Notas y Citas APA", layout="centered")
st.title("📚 Gestor de Notas y Citas APA")

# --- SELECCIÓN DE CATEGORÍA Y SUBCATEGORÍA ---
categoria = st.selectbox("Selecciona la categoría principal:", [
    "Paper académico", "Novela", "Investigación", "Reflexión personal", "Otra"
])

subcategoria = st.selectbox("Selecciona el tipo de nota:", [
    "Análisis", "Cita APA", "Lluvia de ideas", "Observación metodológica", "Otro"
])

# --- FORMULARIO CONDICIONAL PARA CITA APA ---
cita_data = None
if subcategoria == "Cita APA":
    st.subheader("📖 Detalles de la cita APA")
    tipo_fuente = st.selectbox("Tipo de fuente:", ["Artículo", "Libro", "Otro"])
    autor = st.text_input("Autor/es (Apellido, Inicial):")
    anio = st.text_input("Año de publicación:")
    titulo = st.text_input("Título del artículo o libro:")
    revista, doi, editorial, ciudad = "", "", "", ""

    if tipo_fuente == "Artículo":
        revista = st.text_input("Nombre de la revista:")
        doi = st.text_input("DOI:")
    elif tipo_fuente == "Libro":
        editorial = st.text_input("Editorial:")
        ciudad = st.text_input("Ciudad de publicación:")

    cita_data = {
        "tipo_fuente": tipo_fuente,
        "autor": autor,
        "anio": anio,
        "titulo": titulo,
        "revista": revista,
        "doi": doi,
        "editorial": editorial,
        "ciudad": ciudad
    }

# --- CAMPO DE TEXTO PARA NOTA ---
st.subheader("📝 Contenido de la nota")
contenido = st.text_area("Escribe aquí tu nota:", height=200)

# --- ETIQUETAS MULTIPLES ---
st.subheader("🏷️ Etiquetas")
etiquetas_raw = st.text_input("Agrega etiquetas separadas por coma (ej. educación, ciencia, novela)")
etiquetas = ", ".join([e.strip() for e in etiquetas_raw.split(",") if e.strip()])

# --- ARCHIVOS MULTIMEDIA ---
st.subheader("📎 Archivos multimedia (opcional)")
archivos_subidos = st.file_uploader("Sube imágenes, videos o audios:", type=["png", "jpg", "jpeg", "mp4", "mp3", "m4a", "wav"], accept_multiple_files=True)

# --- GUARDAR NOTA ---
if st.button("💾 Guardar nota"):
    if not contenido and subcategoria != "Cita APA":
        st.warning("⚠️ Por favor, escribe algo en la nota.")
    else:
        try:
            contenido_final = contenido if subcategoria != "Cita APA" else titulo
            nota_id = guardar_en_sqlite(categoria, subcategoria, contenido_final, etiquetas, cita_data)
            st.success(f"✅ Nota guardada correctamente con ID: {nota_id}")

            if archivos_subidos:
                media_path = f"media/nota_{nota_id}"
                os.makedirs(media_path, exist_ok=True)
                for archivo in archivos_subidos:
                    with open(os.path.join(media_path, archivo.name), "wb") as f:
                        f.write(archivo.getbuffer())
                st.info(f"📁 Archivos guardados en carpeta: media/nota_{nota_id}")
        except Exception as e:
            st.error(f"❌ Error al guardar la nota: {e}")

# --- EXPORTAR TODO EN ZIP ---
st.markdown("---")
if st.button("📦 Exportar todo en ZIP"):
    try:
        pdf = generar_pdf()
        archivo_zip = exportar_a_zip(pdf)
        with open(archivo_zip, "rb") as f:
            st.download_button("⬇️ Descargar archivo ZIP", f, file_name=archivo_zip, mime="application/zip")
        st.success("✅ Exportación completada con éxito.")
    except Exception as e:
        st.error(f"❌ Error durante la exportación: {e}")
