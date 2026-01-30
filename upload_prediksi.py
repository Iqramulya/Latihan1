import streamlit as st
import pandas as pd
import joblib
from utils_model import preprocess_uploaded_file, predict_n_days

# ===============================
# LOAD MODEL (TIDAK RETRAIN)
# ===============================
model = joblib.load("model_prediksi_obat.pkl")

def show_upload_page():
    st.title("📤 Upload Data & Prediksi Kebutuhan Obat")

    st.caption(
        "Unggah file Excel/CSV berisi data historis pemakaian obat. "
        "Sistem akan memproses data dan menghasilkan prediksi kebutuhan jangka pendek."
    )

    # ===============================
    # UPLOAD FILE
    # ===============================
    uploaded_file = st.file_uploader(
        "Upload file Excel / CSV",
        type=["csv", "xlsx"]
    )

    if not uploaded_file:
        st.info(
            "Format kolom yang dibutuhkan:\n"
            "- tanggal\n"
            "- kode_obat\n"
            "- nama_obat\n"
            "- jumlah_keluar\n"
            "- stok_saat_ini\n"
            "- stok_minimum"
        )
        return

    try:
        # ===============================
        # BACA FILE
        # ===============================
        if uploaded_file.name.endswith(".csv"):
            df_upload = pd.read_csv(uploaded_file)
        else:
            df_upload = pd.read_excel(uploaded_file)

        st.subheader("📄 Preview Data")
        st.dataframe(df_upload.head(), use_container_width=True)

        # ===============================
        # PREPROCESSING
        # ===============================
        df_ready = preprocess_uploaded_file(df_upload)

        # ===============================
        # PARAMETER PREDIKSI
        # ===============================
        st.subheader("⚙️ Parameter Prediksi")
        horizon = st.slider(
            "Prediksi untuk berapa hari ke depan?",
            min_value=1,
            max_value=7,
            value=7
        )

        # ===============================
        # TOMBOL PROSES
        # ===============================
        if st.button("🔍 Proses Prediksi"):
            with st.spinner("Sedang memproses prediksi..."):
                hasil = predict_n_days(df_ready, model, horizon)

                # simpan ke session_state agar tampil di Page 1
                st.session_state["hasil_prediksi"] = hasil
                st.session_state["last_update"] = pd.Timestamp.now()

            st.success("Prediksi berhasil dibuat")

            st.subheader("📊 Hasil Prediksi")
            st.dataframe(hasil, use_container_width=True)

            st.caption(
                "Hasil prediksi disimpan dan dapat dilihat kembali "
                "pada halaman **Dashboard**."
            )

    except Exception as e:
        st.error(f"Terjadi kesalahan: {e}")
