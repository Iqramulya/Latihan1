import streamlit as st
import pandas as pd

def show_dashboard():
    st.title("📊 Dashboard Stok Obat – Kepala Farmasi")

    st.caption(
        "Ringkasan kondisi stok dan hasil prediksi kebutuhan obat "
        "berdasarkan data historis yang diunggah."
    )

    # ===============================
    # VALIDASI DATA PREDIKSI
    # ===============================
    if "hasil_prediksi" not in st.session_state:
        st.warning(
            "Belum ada data prediksi. "
            "Silakan unggah data pada halaman **Upload & Prediksi**."
        )
        return

    hasil = st.session_state["hasil_prediksi"].copy()

    # ===============================
    # HITUNG RINGKASAN STATUS
    # ===============================
    count_aman = (hasil["Status_Stok"] == "Aman").sum()
    count_waspada = (hasil["Status_Stok"] == "Waspada").sum()
    count_kritis = (hasil["Status_Stok"] == "Kritis").sum()

    # ===============================
    # RINGKASAN STATUS (KPI)
    # ===============================
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("🟢 Aman", count_aman)

    with col2:
        st.metric("🟡 Waspada", count_waspada)

    with col3:
        st.metric("🔴 Kritis", count_kritis)

    # ===============================
    # REKOMENDASI SINGKAT
    # ===============================
    if count_kritis > 0:
        st.error(
            f"Terdapat **{count_kritis} obat** dalam kondisi **kritis** "
            "dan direkomendasikan untuk segera dilakukan pengadaan."
        )
    elif count_waspada > 0:
        st.warning(
            f"Terdapat **{count_waspada} obat** dalam kondisi **waspada**. "
            "Perlu pemantauan stok."
        )
    else:
        st.success(
            "Seluruh obat berada dalam kondisi **aman**. "
            "Tidak diperlukan pengadaan dalam waktu dekat."
        )

    # ===============================
    # TABEL HASIL PREDIKSI
    # ===============================
    st.subheader("📋 Ringkasan Hasil Prediksi")

    # Urutkan: Kritis → Waspada → Aman
    urutan_status = {"Kritis": 0, "Waspada": 1, "Aman": 2}
    hasil["__order"] = hasil["Status_Stok"].map(urutan_status)
    hasil = hasil.sort_values("__order").drop(columns="__order")

    st.dataframe(
        hasil,
        use_container_width=True
    )

    # ===============================
    # CATATAN BAWAH (AKADEMIK & PRAKTIS)
    # ===============================
    st.caption(
        "Catatan: Prediksi dilakukan untuk jangka pendek (maksimal 7 hari) "
        "berdasarkan data historis. "
        "Hasil digunakan sebagai **pendukung pengambilan keputusan**, "
        "bukan pengganti kebijakan manajerial."
    )
