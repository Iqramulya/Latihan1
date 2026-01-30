import streamlit as st
from pages.dashboard import show_dashboard
from pages.upload_prediksi import show_upload_page

# ===============================
# KONFIGURASI HALAMAN
# ===============================
st.set_page_config(
    page_title="Prediksi Kebutuhan Stok Obat RS",
    page_icon="💊",
    layout="wide"
)

# ===============================
# SIDEBAR
# ===============================
st.sidebar.title("💊 Sistem Farmasi RS")

menu = st.sidebar.radio(
    "Menu Utama",
    ["Dashboard", "Upload & Prediksi"]
)

st.sidebar.markdown("---")
st.sidebar.caption(
    "Aplikasi pendukung keputusan\n"
    "untuk kepala farmasi."
)

# ===============================
# NAVIGASI PAGE
# ===============================
if menu == "Dashboard":
    show_dashboard()
elif menu == "Upload & Prediksi":
    show_upload_page()
