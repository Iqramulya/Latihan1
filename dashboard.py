import streamlit as st
import pandas as pd


def show_dashboard():
    st.title("📊 Dashboard Stok Obat – Kepala Farmasi")

    st.caption(
        "Ringkasan kondisi stok dan hasil prediksi kebutuhan obat "
        "berdasarkan data historis yang telah diproses oleh sistem."
    )

    # ===============================
    # VALIDASI DATA PREDIKSI
    # ===============================
    if "hasil_prediksi" not in st.session_state:
        st.warning(
            "Belum ada data prediksi.\n\n"
            "Silakan unggah data pada halaman **Upload & Prediksi** "
            "untuk melihat hasil analisis."
        )
        return

    hasil = st.session_state["hasil_prediksi"].copy()

    # ===============================
    # RINGKASAN STATUS STOK
    # ===============================
    count_aman = (hasil["Status_Stok"] == "Aman").sum()
    count_waspada = (hasil["Status_Stok"] == "Waspada").sum()
    count_kritis = (hasil["Status_Stok"] == "Kritis").sum()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("🟢 Aman", count_aman)

    with col2:
        st.metric("🟡 Waspada", count_waspada)

    with col3:
        st.metric("🔴 Kritis", count_kritis)

    # ===============================
    # REKOMENDASI SISTEM
    # ===============================
    st.markdown("---")

    if count_kritis > 0:
        st.error(
            f"⚠️ **{count_kritis} obat** berada pada kondisi **kritis**.\n\n"
            "Direkomendasikan untuk **segera dilakukan pengadaan** "
            "guna mencegah kehabisan stok."
        )
    elif count_waspada > 0:
        st.warning(
            f"⚠️ **{count_waspada} obat** berada pada kondisi **waspada**.\n\n"
            "Perlu dilakukan pemantauan dan perencanaan pengadaan."
        )
    else:
        st.success(
            "✅ Seluruh obat berada pada kondisi **aman**.\n\n"
            "Tidak diperlukan pengadaan dalam waktu dekat."
        )

    # ===============================
    # TABEL HASIL PREDIKSI
    # ===============================
    st.markdown("---")
    st.subheader("📋 Ringkasan Hasil Prediksi Kebutuhan Obat")

    urutan_status = {"Kritis": 0, "Waspada": 1, "Aman": 2}
    hasil["__order"] = hasil["Status_Stok"].map(urutan_status)
    hasil = hasil.sort_values("__order").drop(columns="__order")

    st.dataframe(
        hasil,
        use_container_width=True
    )

    # ===============================
    # INFO TAMBAHAN (AKADEMIK)
    # ===============================
    if "last_update" in st.session_state:
        st.caption(
            f"Terakhir diperbarui: {st.session_state['last_update']}"
        )

    st.caption(
        "Catatan: Sistem ini digunakan sebagai **pendukung pengambilan keputusan**. "
        "Hasil prediksi bersifat jangka pendek (maksimal 7 hari) "
        "dan tidak menggantikan kebijakan manajerial rumah sakit."
    )
