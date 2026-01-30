import streamlit as st
import dashboard
import upload_prediksi as upload

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
# NAVIGASI
# ===============================
if menu == "Dashboard":
    dashboard.show_dashboard()
elif menu == "Upload & Prediksi":
    upload.show_upload_page()
