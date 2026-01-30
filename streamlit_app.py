import streamlit as st
import pages.dashboard as dashboard
import pages.upload_prediksi as upload

# ===============================
# KONFIGURASI HALAMAN (HANYA SEKALI)
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
    dashboard.show_dashboard()
elif menu == "Upload & Prediksi":
    upload.show_upload_page()
