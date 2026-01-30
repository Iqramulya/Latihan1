import streamlit as st
import pandas as pd
import math


def show_dashboard():
    # ======================================================
    # HEADER
    # ======================================================
    st.markdown(
        """
        <h1 style='margin-bottom:0;'>📊 Dashboard Farmasi</h1>
        <p style='font-size:16px;color:#555;'>
        Ringkasan eksekutif kondisi stok obat dan rekomendasi pengadaan
        </p>
        """,
        unsafe_allow_html=True
    )

    # ======================================================
    # VALIDASI DATA
    # ======================================================
    if "hasil_prediksi" not in st.session_state:
        st.info(
            "📌 **Belum ada data analisis**\n\n"
            "Silakan unggah data pemakaian obat pada menu "
            "**Upload & Analisis** untuk melihat kondisi stok."
        )
        return

    df = st.session_state["hasil_prediksi"].copy()

    # ======================================================
    # HITUNG METRIK TAMBAHAN
    # ======================================================
    df["Estimasi_Hari_Habis"] = df.apply(
        lambda x: math.ceil(
            x["Sisa Stok"] / (x["Rata-rata Pemakaian/Hari"] + 1e-6)
        ) if x["Rata-rata Pemakaian/Hari"] > 0 else None,
        axis=1
    )

    total_obat = len(df)
    kritis = (df["Status_Stok"] == "Kritis").sum()
    waspada = (df["Status_Stok"] == "Waspada").sum()
    aman = (df["Status_Stok"] == "Aman").sum()
    perlu_pengadaan = kritis
    rata_hari_aman = round(df["Estimasi_Hari_Habis"].mean(), 1)

    # ======================================================
    # KPI UTAMA (PALING ATAS)
    # ======================================================
    col1, col2, col3, col4, col5 = st.columns(5)

    col1.metric("📦 Total Obat", total_obat)
    col2.metric("🟢 Aman", aman)
    col3.metric("🟡 Waspada", waspada)
    col4.metric("🔴 Kritis", kritis)
    col5.metric("⏳ Rata-rata Hari Aman", rata_hari_aman)

    st.markdown("---")

    # ======================================================
    # ALERT & REKOMENDASI GLOBAL
    # ======================================================
    if kritis > 0:
        st.error(
            f"🚨 **{kritis} obat perlu pengadaan ≤ 3 hari**\n\n"
            "Segera lakukan proses pengadaan untuk mencegah kekosongan stok."
        )
    elif waspada > 0:
        st.warning(
            f"⚠️ **{waspada} obat perlu pemantauan minggu ini**\n\n"
            "Disarankan menyiapkan rencana pengadaan."
        )
    else:
        st.success(
            "✅ **Kondisi stok aman**\n\n"
            "Tidak ada obat yang membutuhkan pengadaan segera."
        )

    st.markdown(
        "<a href='#tabel_prioritas'>⬇️ Lihat Detail Prioritas</a>",
        unsafe_allow_html=True
    )

    # ======================================================
    # TABEL PRIORITAS (SMART TABLE)
    # ======================================================
    st.markdown("---")
    st.markdown("<h3 id='tabel_prioritas'>🚨 Tabel Prioritas Pengadaan</h3>", unsafe_allow_html=True)

    status_filter = st.selectbox(
        "Filter Status",
        ["Semua", "Kritis", "Waspada", "Aman"]
    )

    search = st.text_input("🔍 Cari Nama Obat")

    table = df.copy()

    if status_filter != "Semua":
        table = table[table["Status_Stok"] == status_filter]

    if search:
        table = table[table["Nama Obat"].str.contains(search, case=False)]

    urutan = {"Kritis": 0, "Waspada": 1, "Aman": 2}
    table["__order"] = table["Status_Stok"].map(urutan)
    table = table.sort_values("__order").drop(columns="__order")

    table["Rekomendasi"] = table["Status_Stok"].map({
        "Kritis": "Segera lakukan pengadaan",
        "Waspada": "Pantau & siapkan pengadaan",
        "Aman": "Tidak perlu tindakan"
    })

    st.dataframe(
        table[[
            "Nama Obat",
            "Prediksi Kebutuhan",
            "Sisa Stok",
            "Estimasi_Hari_Habis",
            "Status_Stok",
            "Rekomendasi"
        ]],
        use_container_width=True
    )

    # ======================================================
    # RINGKASAN REKOMENDASI TINDAKAN
    # ======================================================
    st.markdown("---")
    st.subheader("📝 Ringkasan Rekomendasi Tindakan")

    kritis_list = df[df["Status_Stok"] == "Kritis"]["Nama Obat"].tolist()
    waspada_list = df[df["Status_Stok"] == "Waspada"]["Nama Obat"].tolist()

    if kritis_list:
        st.markdown(
            f"**Segera lakukan pengadaan:** {', '.join(kritis_list)}"
        )

    if waspada_list:
        st.markdown(
            f"**Pantau ketersediaan:** {', '.join(waspada_list)}"
        )

    export_col1, export_col2 = st.columns(2)

    export_col1.download_button(
        "⬇️ Export CSV",
        df.to_csv(index=False).encode("utf-8"),
        file_name="rekomendasi_farmasi_rs.csv",
        mime="text/csv"
    )

    # ======================================================
    # INFORMASI KONTEKS
    # ======================================================
    st.markdown("---")
    horizon = st.session_state.get("horizon", "1–7 hari")

    st.caption(
        f"Periode prediksi: **{horizon}** | "
        f"Terakhir diperbarui: **{st.session_state.get('last_update', '-') }**\n\n"
        "Catatan: Sistem ini merupakan **pendukung pengambilan keputusan**, "
        "bukan pengganti kebijakan manajerial."
    )
