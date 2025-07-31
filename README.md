# 🗺️ Pengaturan Server Routing Lokal Valhalla
### Analisis Jarak dan Durasi dengan Data Peta Lokal

[![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/) [![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)

Dokumentasi ini memandu Anda melalui proses lengkap untuk menyiapkan server routing Valhalla secara lokal menggunakan Docker. Setelah server berjalan, Anda akan dapat menghitung jarak dan durasi perjalanan secara massal untuk data koordinat kustom Anda sendiri menggunakan skrip Python.

---

## Daftar Isi
- [Prasyarat](#prasyarat-⚙️)
- [Langkah 1: Menjalankan Layanan Routing Valhalla](#langkah-1-menjalankan-layanan-routing-valhalla-🚀)
  - [1.1 Siapkan Struktur Proyek](#11-siapkan-struktur-proyek)
  - [1.2 Siapkan File-File Penting](#12-siapkan-file-file-penting)
  - [1.3 Jalankan Layanan](#13-jalankan-layanan)
  - [1.4 Pantau Kesiapan Layanan](#14-pantau-kesiapan-layanan)
- [Langkah 2: Menjalankan Analisis Jarak](#langkah-2-menjalankan-analisis-jarak-🐍)
  - [2.1 Instalasi Library Python](#21-instalasi-library-python)
  - [2.2 Siapkan Data Input](#22-siapkan-data-input)
  - [2.3 Buat Skrip Python](#23-buat-skrip-python)
  - [2.4 Jalankan Skrip](#24-jalankan-skrip)

---

## Prasyarat ⚙️
Sebelum memulai, pastikan perangkat Anda telah terinstal:
- **Docker dan Docker Compose**: Diperlukan untuk menjalankan layanan Valhalla. Pastikan layanan Docker sedang berjalan di sistem Anda.
- **Python 3**: Diperlukan untuk menjalankan skrip pemrosesan data.
- **File Peta OpenStreetMap**: Anda harus sudah memiliki file `indonesia-latest.osm.pbf` yang diunduh secara lokal.

---

## Langkah 1: Menjalankan Layanan Routing Valhalla 🚀
Langkah ini bertujuan untuk menyiapkan server Valhalla yang akan memproses permintaan pencarian rute.

### 1.1 Siapkan Struktur Proyek
Buat struktur direktori berikut untuk menjaga agar semua file tetap terorganisir.
```
/routing_valhalla
├── custom_files/
├── input/
└── output/
└── docker-compose.yml
└── search_route.py
```


### 1.2 Siapkan File-File Penting

1.  **Pindahkan File Peta**: Letakkan file `indonesia-latest.osm.pbf` Anda ke dalam direktori `custom_files`.

    ```
    /routing_valhalla
    └── custom_files/
        └── indonesia-latest.osm.pbf  <-- File Peta di sini
    ```
    file dapat di download pada
    ```bash
    https://download.geofabrik.de/asia/indonesia-latest.osm.pbf
    ```

3.  **Buat File `docker-compose.yml`**: Di dalam direktori utama (`routing_valhalla`), buat file bernama `docker-compose.yml` dan isi dengan konfigurasi berikut.

    ```yaml
    version: '3.8'

    services:
      valhalla:
        image: ghcr.io/nilsnolde/docker-valhalla/valhalla:latest
        container_name: valhalla_indonesia_local
        ports:
          - "8002:8002"
        volumes:
          - ./custom_files:/custom_files
        restart: unless-stopped
    ```

### 1.3 Jalankan Layanan
Buka terminal di direktori utama (`routing_valhalla`) dan jalankan perintah di bawah ini untuk memulai layanan dalam mode *detached* (-d).
```bash
docker-compose up -d
```

### 1.4 Pantau Kesiapan Layanan
Proses inisialisasi server akan memakan waktu sangat lama (bisa berjam-jam) karena Valhalla perlu membangun graf routing dari data seluruh Indonesia. Anda dapat memantau log untuk melihat progresnya.
```bash
docker-compose logs -f
```

### ⚠️ Layanan Siap Digunakan
Layanan dianggap siap sepenuhnya jika Anda melihat pesan valhalla_service_run(): Running service... di akhir log. Selama proses ini berjalan, permintaan ke API akan gagal.

Langkah 2: Menjalankan Analisis Jarak 🐍
Setelah server Valhalla siap, Anda bisa menggunakan skrip Python untuk mengirim data koordinat dan mendapatkan hasilnya.

2.1 Instalasi Library Python
Jika belum terinstal, jalankan perintah ini di terminal Anda:
```bash
pip install pandas requests tqdm
```
2.2 Siapkan Data Input
Letakkan file CSV data Anda (contoh: testing_data_1.csv) ke dalam direktori input. Pastikan file CSV memiliki kolom-kolom berikut:

- BRANCH_LONGITUDE
- BRANCH_LATITUDE
- SELECTED_LONGITUDE
- SELECTED_LATITUDE

```
/routing_valhalla
└── input/
    └── testing_data_1.csv  <-- File data Anda di sini
```

2.3 Jalankan Skrip
Pastikan server Valhalla sudah siap, lalu jalankan search_route.py dari terminal:

python search_route.py

Skrip akan memproses setiap baris, menampilkan progress bar, dan setelah selesai, sebuah file CSV baru akan dibuat di dalam direktori output dengan tambahan kolom JARAK_KM dan DURASI_MENIT.

