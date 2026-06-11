# QA System Rumah Sakit Sehat Selalu

Sistem tanya jawab berbasis AI untuk data Rumah Sakit Sehat Selalu. Pengguna bisa mengajukan pertanyaan dalam bahasa natural dan sistem akan menjawab langsung dari database rumah sakit menggunakan AI agent.

![Status](https://img.shields.io/badge/status-active-brightgreen)
![Python](https://img.shields.io/badge/python-3.10+-blue)
![React](https://img.shields.io/badge/react-18+-61DAFB)

---

## Tampilan Aplikasi

> Screenshot antarmuka QA System

---

## Arsitektur Sistem

```
User (Browser)
    │
    ▼
React + Vite (port 5173)
    │  Axios POST /chat
    ▼
FastAPI + Uvicorn (port 8000)
    │
    ▼
LangChain ReAct Agent
    │  Llama-3.3-70B via Groq API
    ▼
┌─────────────────────────────────────────┐
│              5 Tools Agent              │
│                                         │
│  cari_makna_medis    → KNN Vector       │
│  cari_keyword_eksak  → BM25 Keyword     │
│  statistik_tagihan   → Aggregation      │
│  statistik_diagnosa  → Aggregation      │
│  statistik_dokter    → Aggregation      │
└─────────────────────────────────────────┘
    │
    ▼
OpenSearch (port 9200)
```

---

## Stack Teknologi

| Komponen | Teknologi | Keterangan |
|---|---|---|
| LLM | Llama-3.3-70B via Groq | Gratis, cepat, mendukung tool calling |
| AI Agent | LangChain ReAct | Reasoning loop otomatis |
| Vector DB | OpenSearch 2.x | KNN search + BM25 dalam satu engine |
| Embedding | paraphrase-multilingual-MiniLM-L12-v2 | Mendukung Bahasa Indonesia, 384 dimensi |
| Backend | FastAPI + Uvicorn | REST API |
| Frontend | React + Vite | UI chatbot |

---

## Struktur Project

```
Project_QASystem_OpenSearch/
├── backend/
│   ├── main.py               # API Gateway (FastAPI)
│   ├── agent_brain.py        # LangChain ReAct Agent
│   ├── tools_vector.py       # KNN + BM25 search tools
│   ├── tools_analytics.py    # Aggregation analytics tools
│   ├── ingest_pipeline.py    # Pipeline ingestion data ke OpenSearch
│   ├── config.py             # Konfigurasi terpusat
│   ├── requirements.txt      # Dependencies Python
│   └── .env                  # API key (buat sendiri, tidak ada di repo)
├── frontend/
│   ├── src/
│   │   ├── App.jsx           # Komponen utama chatbot
│   │   └── App.css           # Styling
│   ├── package.json
│   └── vite.config.js
├── docker-compose.yml        # Setup OpenSearch
└── README.md
```

---

## Prerequisites

Pastikan semua tools berikut sudah terinstall di laptopmu sebelum mulai.

### 1. Docker Desktop
Download di https://www.docker.com/products/docker-desktop

Setelah install, buka Docker Desktop dan pastikan statusnya **Engine running** (ikon hijau di pojok kiri bawah).

### 2. Python 3.10+
Download di https://www.python.org/downloads

> **PENTING:** Saat instalasi, centang kotak **"Add Python to PATH"** sebelum klik Install Now.

Verifikasi:
```bash
python --version
```

### 3. Node.js (LTS)
Download di https://nodejs.org

Verifikasi:
```bash
node --version
```

### 4. Git
Download di https://git-scm.com/download/win

Verifikasi:
```bash
git --version
```

---

## Setup dan Instalasi

### Langkah 1: Clone Repository

```bash
git clone https://github.com/USERNAME/Project_QASystem_OpenSearch.git
cd Project_QASystem_OpenSearch
```

> Ganti `USERNAME` dengan username GitHub pemilik repo.

---

### Langkah 2: Siapkan File Data JSON

File data JSON tidak ikut di dalam repository. Minta folder data dari anggota kelompok yang memilikinya. Folder berisi 6 file:

- `rs_sehat_selalu.Dokter.json`
- `rs_sehat_selalu.Pasien.json`
- `rs_sehat_selalu.Rekam_Medis.json`
- `rs_sehat_selalu.Tagihan.json`
- `rs_sehat_selalu.Departemen.json`
- `rs_sehat_selalu.Tim_Medis.json`

Simpan folder tersebut di lokasi yang mudah diingat, contoh: `C:\Data_RS_OpenSearch`

---

### Langkah 3: Buat File .env

Buat file bernama `.env` di dalam folder `backend/`:

```
GROQ_API_KEY=isi_dengan_api_key_groq_kamu
```

Untuk mendapatkan API key Groq:
1. Buka https://console.groq.com dan daftar akun gratis
2. Klik menu **API Keys** di sidebar
3. Klik **Create API Key**, beri nama, lalu copy key yang muncul

> **PENTING:** Simpan API key di tempat aman. Key hanya ditampilkan sekali.

---

### Langkah 4: Sesuaikan Path Data

Buka file `backend/config.py` dan `backend/ingest_pipeline.py`, cari baris `DATA_FOLDER` dan ganti dengan path folder data JSON di laptopmu:

```python
# Ganti ini:
DATA_FOLDER = r"C:\Tugas Folder\Semester 6\ROBD\Data_RS_OpenSearch"

# Menjadi path folder data di laptopmu, contoh:
DATA_FOLDER = r"C:\Data_RS_OpenSearch"
```

---

### Langkah 5: Jalankan OpenSearch

Pastikan Docker Desktop sudah menyala, lalu jalankan di terminal dari folder utama project:

```bash
docker-compose up -d
```

Tunggu sampai proses selesai. Verifikasi OpenSearch sudah berjalan dengan membuka browser ke:

```
http://localhost:9200
```

Jika berhasil, browser menampilkan response JSON berisi informasi cluster OpenSearch.

> OpenSearch perlu dijalankan ulang setiap kali laptop restart dengan perintah yang sama.

---

### Langkah 6: Install Dependencies Python

```bash
cd backend
pip install -r requirements.txt
pip install python-dotenv
```

Proses ini bisa memakan waktu 5-10 menit tergantung koneksi internet.

---

### Langkah 7: Isi Data ke OpenSearch

Langkah ini hanya perlu dilakukan **sekali**.

```bash
cd backend
python ingest_pipeline.py
```

Tunggu sampai muncul output:
```
[INFO] Operasi pipa data selesai secara mutlak. Pangkalan Data terstruktur dengan sempurna.
```

---

### Langkah 8: Install Dependencies Frontend

```bash
cd frontend
npm install
```

---

## Menjalankan Aplikasi

Kamu butuh **dua terminal** yang berjalan bersamaan.

### Terminal 1 — Backend

```bash
cd backend
python main.py
```

Tunggu sampai muncul:
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

### Terminal 2 — Frontend

```bash
cd frontend
npm run dev
```

Tunggu sampai muncul:
```
VITE v8.x.x  ready in xxx ms
  -> Local:   http://localhost:5173/
```

Buka browser ke **http://localhost:5173**

> Jangan tutup kedua terminal ini selama menggunakan aplikasi.

---

## Verifikasi Sistem Berjalan

1. Buka browser ke `http://localhost:5173`
2. Pastikan status badge di pojok kanan atas menampilkan **Online** (hijau)
3. Coba ketik pertanyaan berikut di chatbox:

```
Berapa total tagihan rumah sakit?
```

```
Dokter spesialis Pediatri siapa saja?
```

```
Diagnosa apa yang paling sering?
```

Jika ketiganya terjawab, sistem berjalan dengan benar.

---

## Contoh Pertanyaan

| Jenis Pertanyaan | Contoh |
|---|---|
| Statistik keuangan | Berapa total tagihan rumah sakit? |
| Statistik keuangan | Berapa tagihan yang belum lunas? |
| Diagnosa | Diagnosa apa yang paling sering? |
| Diagnosa | Berapa pasien yang didiagnosa Diabetes? |
| Dokter | Berapa jumlah dokter per spesialisasi? |
| Dokter | Dokter spesialis Pediatri siapa saja? |
| Pasien | Siapa pasien yang alergi kacang? |
| Pencarian spesifik | Dokter Maryanto Sudiati spesialisasi apa? |

---

## Troubleshooting

**Status badge merah Offline**
Pastikan terminal backend menyala. Coba jalankan ulang `python main.py`.

**Error koneksi OpenSearch saat ingest**
Pastikan Docker Desktop menyala dan jalankan ulang `docker-compose up -d`. Tunggu 2 menit lalu coba lagi.

**`npm run dev` error Missing script**
Jalankan `npm install` di folder frontend terlebih dahulu.

**`python main.py` error ModuleNotFoundError**
Jalankan `pip install -r requirements.txt` dan `pip install python-dotenv` di folder backend.

**Jawaban sistem selalu error**
Pastikan file `.env` sudah dibuat di folder backend dan berisi API key Groq yang valid.

**Data kosong atau tidak ditemukan**
Pastikan path `DATA_FOLDER` di `config.py` dan `ingest_pipeline.py` sudah disesuaikan, lalu jalankan ulang `python ingest_pipeline.py`.

**Port 5173 sudah dipakai**
Vite akan otomatis pindah ke port berikutnya (5174, 5175, dst). Lihat port yang muncul di terminal dan buka port tersebut di browser.

---

## Mata Kuliah

Rekayasa dan Organisasi Sistem Big Data
Dosen Pengampu: Bapak Kemas Rahmat Saleh Wiharja
Program Studi S1 Sains Data — Fakultas Informatika — Telkom University 2026
