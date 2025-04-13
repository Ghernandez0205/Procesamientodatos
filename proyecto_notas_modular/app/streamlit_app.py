import streamlit as st

st.set_page_config(page_title="Gestor de Notas", layout="centered")

st.title("📚 Gestor de Notas y Citas APA")
st.markdown("""
Bienvenido a tu entorno de captura de notas, citas y recursos multimedia.

Este proyecto incluye:
- ✍️ Notas por categoría
- 📖 Citas en formato APA
- 📎 Archivos multimedia (imágenes, video, audio)
- 🧾 Exportación como PDF y ZIP
""")

if st.button("🚀 Confirmar que Streamlit funciona"):
    st.success("¡Streamlit está corriendo correctamente!")
