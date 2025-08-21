import pandas as pd
import numpy as np
import random

# Data dasar
data = {
    'Invoice_ID': [f'INV-10{i}' for i in range(1, 11)],
    'Nama_Pelanggan': [
        'PT Sejahtera', 'CV Maju Jaya', 'UD Berkah', 'PT Cemerlang', 'CV Abadi',
        'PT Sukses Selalu', 'UD Mandiri', 'CV Makmur', 'PT Gemilang', 'Toko Barokah'
    ]
}
df = pd.DataFrame(data)

# Daftar bucket yang mungkin
buckets = [30, 60, 90, 120]
bucket_cols = [f'Bucket_{b}' for b in buckets]

# Membuat kolom bucket dan mengisinya dengan nilai acak atau kosong (NaN)
for index, row in df.iterrows():
    # Pilih secara acak 1 sampai 3 bucket untuk diisi per baris
    num_buckets_to_fill = random.randint(1, 3)
    buckets_to_fill = random.sample(buckets, num_buckets_to_fill)
    
    for b in buckets:
        col_name = f'Bucket_{b}'
        if b in buckets_to_fill:
            # Isi dengan jumlah tagihan acak
            df.loc[index, col_name] = random.randint(500000, 15000000)
        else:
            # Biarkan kosong
            df.loc[index, col_name] = np.nan

# Simpan ke file Excel
nama_file_output = 'data_aging_multi_column.xlsx'
df.to_excel(nama_file_output, index=False)

print(f"✅ File Excel dummy bernama '{nama_file_output}' berhasil dibuat!")