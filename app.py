import streamlit as st
import pandas as pd
import io

# ===================================================================
# FUNGSI LOGIKA ANDA (diambil dari skrip sebelumnya)
# ===================================================================
def proses_data_aging(df):
    """
    Fungsi ini menerima DataFrame, memprosesnya, dan mengembalikannya.
    """
    # Identifikasi kolom bucket secara otomatis
    bucket_cols = [col for col in df.columns if 'Bucket_' in col]
    
    if not bucket_cols:
        st.warning("Peringatan: Tidak ada kolom 'Bucket_' yang ditemukan dalam file.")
        return df

    def buat_kategori_bucket(row):
        kategori_terisi = []
        for col in bucket_cols:
            # Menggunakan try-except untuk menangani jika nilai di sel bukan angka
            try:
                if pd.notna(row[col]) and float(row[col]) != 0:
                    nama_bucket = col.split('_')[1]
                    kategori_terisi.append(nama_bucket)
            except (ValueError, TypeError):
                # Abaikan sel yang tidak bisa diubah menjadi angka
                pass
        return '-'.join(kategori_terisi)

    df['Kategori_Aging'] = df.apply(buat_kategori_bucket, axis=1)
    return df

# ===================================================================
# TAMPILAN APLIKASI WEB STREAMLIT
# ===================================================================

st.set_page_config(page_title="Aplikasi Kategori Aging", layout="wide")
st.title("🚀 Aplikasi Pembuat Kategori Aging Otomatis")

st.write(
    "Selamat datang! Aplikasi ini akan membantu Anda membuat kolom kategori aging secara otomatis."
    " Cukup unggah file Excel atau CSV Anda untuk memulai."
)

uploaded_file = st.file_uploader(
    "Pilih file Excel atau CSV", 
    type=['csv', 'xlsx']
)

if uploaded_file is not None:
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        st.success(f"✅ File '{uploaded_file.name}' berhasil diunggah!")
        st.subheader("Cuplikan Data Asli Anda:")
        st.dataframe(df.head())

        if st.button("Proses Data Sekarang", type="primary"):
            # V-- Tambahkan baris ini
            with st.spinner('Harap tunggu, sedang memproses file besar...'):
                # V-- Beri spasi/indentasi pada baris ini
                df_hasil = proses_data_aging(df.copy()) 
            
            # Baris ini akan berjalan setelah spinner selesai
            st.success("🎉 Proses Selesai!")    
            
            st.subheader("🎉 Hasil Setelah Diproses:")
            st.dataframe(df_hasil.head())

            # ===================================================================
            # BAGIAN BARU: STATISTIK PEMROSESAN
            # ===================================================================
            st.subheader("📊 Ringkasan Pemrosesan")

            # Hitung statistik
            total_rows = len(df_hasil)
            gagal_rows_df = df_hasil[df_hasil['Kategori_Aging'] == '']
            jumlah_gagal = len(gagal_rows_df)
            jumlah_berhasil = total_rows - jumlah_gagal
            persentase_berhasil = (jumlah_berhasil / total_rows) * 100 if total_rows > 0 else 0

            # Tampilkan metrik dalam kolom
            col1, col2, col3 = st.columns(3)
            col1.metric("✔️ Baris Berhasil", f"{jumlah_berhasil}")
            col2.metric("❌ Baris Gagal (Kosong)", f"{jumlah_gagal}")
            col3.metric("📈 Persentase Berhasil", f"{persentase_berhasil:.2f}%")
            
            # Tampilkan baris yang gagal jika ada
            if jumlah_gagal > 0:
                with st.expander(f"Lihat {jumlah_gagal} baris yang gagal dikategorikan (hasilnya kosong)"):
                    st.dataframe(gagal_rows_df)
            else:
                st.success("Sempurna! Semua baris berhasil dikategorikan.")


            # --- Tombol Download ---
            output_csv = df_hasil.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Unduh Hasil sebagai CSV",
                data=output_csv,
                file_name=f"hasil_{uploaded_file.name.split('.')[0]}.csv",
                mime='text/csv',
            )
            
    except Exception as e:
        st.error(f"Terjadi kesalahan saat memproses file: {e}")