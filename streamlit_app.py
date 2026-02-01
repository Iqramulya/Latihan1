import streamlit as st
import dashboard
import upload_prediksi as upload

# ===============================
# KONFIGURASI HALAMAN
# ===============================
st.set_page_config(
    page_title="Sistem Farmasi RS Adi Sucipto",
    page_icon="💊",
    layout="wide"
)

# ===============================
# SIDEBAR
# ===============================
st.sidebar.markdown(
    """
    <h2 style='text-align:center;'>🏥 RS Adi Sucipto</h2>
    <p style='text-align:center; font-size:14px;'>
    Sistem Pendukung Keputusan<br>
    Kebutuhan Stok Obat
    </p>
    """,
    unsafe_allow_html=True
)

st.sidebar.markdown("---")

menu = st.sidebar.radio(
    "📌 Menu Utama",
    ["Dashboard", "Upload & Prediksi"]
)

st.sidebar.markdown("---")
st.sidebar.caption(
    "Digunakan oleh:\n"
    "**Kepala Instalasi Farmasi**"
)

if menu == "Dashboard":
    dashboard.show_dashboard()
elif menu == "Upload & Prediksi":
    upload.show_upload_page()
