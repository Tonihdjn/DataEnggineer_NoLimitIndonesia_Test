
# Aplikasi Scraper Berita Bisnis.com

Aplikasi **Scraper Berita** ini dirancang untuk mengambil berita terbaru dari **Bisnis.com** secara otomatis dan menyimpan data artikel tersebut dalam format yang mudah digunakan. Pengguna dapat memilih untuk mengambil berita terbaru atau memfilter berita berdasarkan rentang tanggal yang diinginkan. Setelah data diambil, pengguna dapat melihatnya, mengunduhnya dalam format CSV atau JSON, atau menyimpannya ke dalam basis data MongoDB.

Dengan aplikasi ini, pengguna dapat mengakses data berita secara lebih efisien tanpa harus mengunjungi situs berita secara manual setiap saat.

## Fitur Utama

- **Standard Scraping**: Aplikasi ini memungkinkan pengguna untuk mengambil berita terbaru yang dipublikasikan di Bisnis.com secara otomatis.
- **Backtrack Scraping**: Pengguna dapat memilih rentang tanggal tertentu untuk memfilter berita yang diinginkan.
- **Tampilan Tabel yang Mudah Dibaca**: Data yang diambil ditampilkan dalam format tabel yang mudah dibaca menggunakan **Streamlit**.
- **Opsi Unduhan**: Pengguna dapat mengunduh data berita yang telah di-scrape dalam format CSV atau JSON untuk analisis lebih lanjut.
- **Simpan ke MongoDB**: Pengguna dapat menyimpan data berita langsung ke dalam basis data **MongoDB** untuk digunakan di aplikasi atau sistem lain.

## Instalasi

Ikuti langkah-langkah berikut untuk menginstal dan menjalankan aplikasi ini:

### Persyaratan

- Python 3.x
- Streamlit
- BeautifulSoup
- Requests
- Pandas
- Pymongo
- MongoDB (untuk menyimpan data)

Install semua dependensi yang diperlukan dengan menjalankan perintah berikut:
```bash
pip install streamlit beautifulsoup4 requests pandas pymongo
```

### Menjalankan Aplikasi

1. Pastikan **MongoDB** berjalan di mesin lokal Anda. Jika tidak, sesuaikan koneksi MongoDB di file `main.py` sesuai dengan pengaturan Anda.
2. Jalankan aplikasi **Streamlit** dengan perintah:
   ```bash
   streamlit run main.py
   ```
3. Akses aplikasi melalui browser Anda (biasanya di `http://localhost:8501`).
4. Pilih opsi pencarian berita (Terbaru atau Berdasarkan Tanggal).
5. Klik tombol **Scrape Berita** untuk mulai mengambil data.
6. Setelah data diambil, Anda dapat:
   - Melihat data dalam bentuk tabel.
   - Mengunduh data dalam format CSV atau JSON.
   - Menyimpan data ke dalam MongoDB dengan mengklik **Simpan ke MongoDB**.

## Deskripsi File

### 1. **`beritaPage.py`**

File ini berisi logika scraping dari halaman Bisnis.com. Berikut adalah fungsi-fungsi utama yang terdapat dalam file ini:

- **`get_soup(url)`**: Mengambil konten HTML dari halaman web yang diberikan.
- **`get_judul(soup)`**: Mengambil judul artikel dari halaman.
- **`get_tgl(soup)`**: Mengambil tanggal artikel dan memformatnya sesuai standar ISO 8601.
- **`clean_text(text)`**: Membersihkan teks artikel dari karakter-karakter yang tidak diinginkan.
- **`get_isi(soup)`**: Mengambil isi artikel dan membersihkannya.
- **`get_all(url)`**: Mengambil semua data artikel (judul, isi, tanggal) dari URL yang diberikan.
- **`one_page(output, soupOne)`**: Mengambil semua artikel dari satu halaman dan menambahkannya ke dalam list output.
- **`navigate_many_page(url)`**: Menangani pagination untuk mengambil data dari banyak halaman.
- **`generate_url(date)`**: Membuat URL dinamis berdasarkan tanggal.
- **`scrape_by_date_range(start_date, end_date)`**: Melakukan scraping berdasarkan rentang tanggal yang diberikan.

### 2. **`main.py`**

File ini membuat antarmuka pengguna berbasis **Streamlit** untuk aplikasi ini. Berikut adalah fitur-fitur utama dalam file ini:

- **Antarmuka Pengguna (UI)**: Memungkinkan pengguna memilih apakah mereka ingin mengambil berita terbaru atau berdasarkan rentang tanggal.
- **Pengunduhan Data**: Menyediakan tombol untuk mengunduh data yang telah di-scrape dalam format CSV atau JSON.
- **Integrasi MongoDB**: Menyimpan data yang diambil ke dalam koleksi MongoDB untuk digunakan lebih lanjut.

## Pengaturan MongoDB

Aplikasi ini disiapkan untuk menyimpan data yang diambil dalam koleksi MongoDB `Scrape` di dalam database `DE_NoLimit`. Anda dapat mengganti nama database atau koleksi sesuai dengan kebutuhan Anda di file `main.py`.

## Pemecahan Masalah

- **Error 404 atau Tidak Ada Data**: Jika terjadi kesalahan atau tidak ada data yang ditemukan, pastikan bahwa URL yang digunakan masih valid dan struktur halaman Bisnis.com belum berubah.
- **Masalah Koneksi MongoDB**: Jika ada masalah dengan koneksi MongoDB, pastikan MongoDB berjalan di mesin Anda dan string koneksi diatur dengan benar di `main.py`.


