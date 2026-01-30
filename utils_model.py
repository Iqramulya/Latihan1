import pandas as pd


def preprocess_uploaded_file(df):
    required_columns = [
        "tanggal",
        "kode_obat",
        "nama_obat",
        "jumlah_keluar",
        "stok_saat_ini",
        "stok_minimum"
    ]

    for col in required_columns:
        if col not in df.columns:
            raise ValueError(f"Kolom '{col}' tidak ditemukan")

    df["tanggal"] = pd.to_datetime(df["tanggal"])
    return df


def predict_n_days(df, horizon):
    hasil = []

    for nama_obat, group in df.groupby("nama_obat"):
        rata_pakai = group["jumlah_keluar"].mean()
        stok = group["stok_saat_ini"].iloc[-1]
        stok_min = group["stok_minimum"].iloc[-1]

        prediksi_kebutuhan = rata_pakai * horizon
        sisa_stok = stok - prediksi_kebutuhan

        if sisa_stok <= stok_min:
            status = "Kritis"
        elif sisa_stok <= stok_min * 1.5:
            status = "Waspada"
        else:
            status = "Aman"

        hasil.append({
            "Nama Obat": nama_obat,
            "Rata-rata Pemakaian/Hari": round(rata_pakai, 2),
            "Prediksi Kebutuhan": round(prediksi_kebutuhan, 2),
            "Sisa Stok": round(sisa_stok, 2),
            "Status_Stok": status
        })

    return pd.DataFrame(hasil)
