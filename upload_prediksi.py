import streamlit as st
import pandas as pd
from utils_model import preprocess_uploaded_file, predict_n_days


def show_upload_page():
    st.title("📤 Upload Data & Prediksi Kebutuhan Obat")

    st.caption(
        "Unggah data historis pemakaian obat untuk menghasilkan "
        "prediksi kebutuhan jangka pendek."
    )

    uploaded_file = st.file_uploader(
        "Upload file CSV / Excel",
        type=["csv", "xlsx"]
    )

    if uploaded_file is None:
        st.info(
            "Format kolom wajib:\n"
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
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        st.subheader("📄 Preview Data")
        st.dataframe(df.head(), use_container_width=True)

        # ===============================
        # PREPROCESS
        # ===============================
        df_ready = preprocess_uploaded_file(df)
        st.success("Data berhasil diproses")

        # ===============================
        # PARAMETER
        # ===============================
        horizon = st.slider(
            "Prediksi untuk berapa hari ke depan?",
            min_value=1,
            max_value=7,
            value=7
        )

        # ===============================
        # PROSES PREDIKSI
        # ===============================
        if st.button("🔍 Proses Prediksi"):
            with st.spinner("Sedang memproses analisis..."):
                hasil = predict_n_days(df_ready, horizon)

                st.session_state["hasil_prediksi"] = hasil
                st.session_state["last_update"] = pd.Timestamp.now()

            st.success("Analisis & prediksi berhasil")

            st.subheader("📊 Hasil Prediksi")
            st.dataframe(hasil, use_container_width=True)

            st.caption(
                "Hasil ini otomatis tersimpan dan dapat dilihat "
                "di halaman **Dashboard**."
            )

    except Exception as e:
        st.error(f"Terjadi kesalahan: {e}")
