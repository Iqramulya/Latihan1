import streamlit as st
import pandas as pd


def show_dashboard():
    st.markdown(
        """
        <h1>📊 Dashboard Farmasi</h1>
        <p style='font-size:16px;'>
        Ringkasan kondisi stok obat dan rekomendasi pengadaan
        untuk mendukung pengambilan keputusan manajerial.
        </p>
        """,
        unsafe_allow_html=True
    )

    # ===============================
    # VALIDASI DATA
    # ===============================
    if "hasil_prediksi" not in st.session_state:
        st.info(
            "📌 **Belum ada data analisis.**\n\n"
            "Silakan unggah data pemakaian obat pada menu "
            "**Upload & Prediksi** untuk melihat kondisi stok."
        )
        return

    hasil = st.session_state["hasil_prediksi"].copy()

    # ===============================
    # KPI UTAMA (YANG DIBUTUHKAN KEPALA FARMASI)
    # ===============================
    total_obat = len(hasil)
    kritis = (hasil["Status_Stok"] == "Kritis").sum()
    waspada = (hasil["Status_Stok"] == "Waspada").sum()
    aman = (hasil["Status_Stok"] == "Aman").sum()

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("📦 Total Obat", total_obat)
    col2.metric("🔴 Kritis", kritis)
    col3.metric("🟡 Waspada", waspada)
    col4.metric("🟢 Aman", aman)

    st.markdown("---")

    # ===============================
    # REKOMENDASI UTAMA (DECISION BOX)
    # ===============================
    if kritis > 0:
        st.error(
            f"🚨 **PERLU TINDAKAN SEGERA**\n\n"
            f"Terdapat **{kritis} obat** dalam kondisi **kritis** "
            "dan direkomendasikan untuk **segera dilakukan pengadaan**."
        )
    elif waspada > 0:
        st.warning(
            f"⚠️ **PERLU PERHATIAN**\n\n"
            f"Terdapat **{waspada} obat** dalam kondisi **waspada**. "
            "Disarankan melakukan perencanaan pengadaan."
        )
    else:
        st.success(
            "✅ **KONDISI STOK AMAN**\n\n"
            "Seluruh obat berada dalam batas aman. "
            "Tidak diperlukan pengadaan dalam waktu dekat."
        )

    # ===============================
    # TABEL PRIORITAS (KHUSUS KEPALA FARMASI)
    # ===============================
    st.markdown("---")
    st.subheader("🚨 Daftar Prioritas Pengadaan Obat")

    prioritas = hasil[hasil["Status_Stok"] != "Aman"]

    if prioritas.empty:
        st.success("Tidak ada obat yang perlu diprioritaskan saat ini.")
    else:
        st.dataframe(
            prioritas.sort_values("Status_Stok"),
            use_container_width=True
        )

    # ===============================
    # TABEL LENGKAP
    # ===============================
    st.markdown("---")
    st.subheader("📋 Rekapitulasi Seluruh Obat")

    urutan = {"Kritis": 0, "Waspada": 1, "Aman": 2}
    hasil["__order"] = hasil["Status_Stok"].map(urutan)
    hasil = hasil.sort_values("__order").drop(columns="__order")

    st.dataframe(hasil, use_container_width=True)

    # ===============================
    # INFO TAMBAHAN
    # ===============================
    if "last_update" in st.session_state:
        st.caption(f"🕒 Terakhir diperbarui: {st.session_state['last_update']}")

    st.caption(
        "Catatan: Sistem ini bersifat **pendukung keputusan** "
        "dan digunakan oleh Kepala Instalasi Farmasi RS Bhayangkara "
        "untuk perencanaan kebutuhan obat jangka pendek."
    )
