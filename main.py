import streamlit as st
import pandas as pd
import pymongo
from datetime import datetime
import beritaPage

client = pymongo.MongoClient("mongodb://localhost:27017/")  # sok diganti dengan alamat db 
db = client["DE_NoLimit"]  # sok diganti dengan nama databasenya
collection = db["Scrape"]  # sok diganti dengan nama collectionnya

st.title('Scraper Berita')

# Opsi untuk memilih tipe pencarian berita
option = st.radio('Pilih Tipe Pencarian Berita:', ('Berita Terbaru', 'Berita Berdasarkan Tanggal'))

output = []

if option == 'Berita Terbaru':
    url = "https://www.bisnis.com/index?categoryId=0&type=indeks&date=&type=indeks"
    if st.button('Scrape Berita'):
        output = beritaPage.navigate_many_page(url)
        if output:
            df = pd.DataFrame(output)
            st.dataframe(df)  # Menampilkan hasil dalam bentuk tabel

elif option == 'Berita Berdasarkan Tanggal':
    start_date = st.date_input('Tanggal Mulai:')
    end_date = st.date_input('Tanggal Akhir:')
    if st.button('Scrape Berita Berdasarkan Tanggal'):
        output = beritaPage.scrape_by_date_range(start_date, end_date)
        if output:
            df = pd.DataFrame(output)
            st.dataframe(df)  # Menampilkan hasil dalam bentuk tabel

# Jika output tersedia, tampilkan opsi untuk menyimpan data
if output:
    # Input untuk nama file yang diinginkan
    file_name = st.text_input('Masukkan nama file (tanpa ekstensi):', 'scraped_berita')
    
    # Tombol untuk menyimpan sebagai CSV
    csv = df.to_csv(index=False)
    st.download_button(
        label="Download CSV",
        data=csv,
        file_name=f"{file_name}.csv",
        mime="text/csv"
    )
    
    # Tombol untuk menyimpan sebagai JSON
    json_data = df.to_json(orient='records')
    st.download_button(
        label="Download JSON",
        data=json_data,
        file_name=f"{file_name}.json",
        mime="application/json"
    )
    
    # Tombol untuk memasukkan data ke MongoDB
    if st.button('Simpan ke MongoDB'):
        try:
            # Menambahkan data ke MongoDB
            collection.insert_many(output)
            st.success('Data berhasil disimpan ke MongoDB!')
        except Exception as e:
            st.error(f"Terjadi kesalahan saat menyimpan data ke MongoDB: {str(e)}")
