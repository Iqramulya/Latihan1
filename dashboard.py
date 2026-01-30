import streamlit as st
import pandas as pd


def show_dashboard():
    st.title("📊 Dashboard Stok Obat – Kepala Farmasi")

    st.caption(
        "Ringkasan kondisi stok dan hasil prediksi kebutuhan obat "
        "berdasarkan analisis data historis."
    )

    # ===============================
    # VALIDASI DATA
    # ===============================
    if "hasil_prediksi" not in st.session_state:
        st.warning(
            "Belum ada data prediksi.\n\n"
            "Silakan unggah data pada halaman **Upload & Prediksi**."
        )
        return

    hasil = st.session_state["hasil_prediksi"].copy()

    # ===============================
    # HITUNG STATUS
    # ===============================
    aman = (hasil["Status_Stok"] == "Aman").sum()
    waspada = (hasil["Status_Stok"] == "Waspada").sum()
    kritis = (hasil["Status_Stok"] == "Kritis").sum()

    col1, col2, col3 = st.columns(3)
    col1.metric("🟢 Aman", aman)
    col2.metric("🟡 Waspada", waspada)
    col3.metric("🔴 Kritis", kritis)

    st.markdown("---")

    # ===============================
    # REKOMENDASI
    # ===============================
    if kritis > 0:
        st.error(
            f"⚠️ Terdapat **{kritis} obat** dalam kondisi **kritis**.\n"
            "Direkomendasikan segera dilakukan pengadaan."
        )
    elif waspada > 0:
        st.warning(
            f"⚠️ Terdapat **{waspada} obat** dalam kondisi **waspada**.\n"
            "Perlu pemantauan stok."
        )
    else:
        st.success(
            "✅ Seluruh obat berada dalam kondisi **aman**."
        )

    st.markdown("---")
    st.subheader("📋 Hasil Analisis & Prediksi")

    # Urutkan status
    urutan = {"Kritis": 0, "Waspada": 1, "Aman": 2}
    hasil["__order"] = hasil["Status_Stok"].map(urutan)
    hasil = hasil.sort_values("__order").drop(columns="__order")

    st.dataframe(hasil, use_container_width=True)

    if "last_update" in st.session_state:
        st.caption(f"Terakhir diperbarui: {st.session_state['last_update']}")
    st.caption(
        "Catatan: Sistem ini digunakan sebagai **pendukung pengambilan keputusan** "
        "dan tidak menggantikan kebijakan atau pertimbangan klinis. "
        "Gunakan hasil ini sebagai referensi bersama pengambilan keputusan."
    )

