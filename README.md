# Cara Menjalankan Dashboard

Ikuti langkah berikut secara berurutan agar dashboard dapat berjalan dengan baik.

## 1. Buka folder project
Pastikan terminal berada di folder `submission`.

```bash
cd /path/ke/submission
```

## 2. Buat virtual environment
Jika virtual environment belum ada, jalankan perintah berikut.

```bash
python3 -m venv .venv
```

## 3. Aktifkan virtual environment

```bash
source .venv/bin/activate
```

## 4. Install library yang dibutuhkan

```bash
pip install -r requirements.txt
```

## 5. Jalankan notebook
Jalankan file `notebook.ipynb` dari atas sampai bawah agar file `dashboard/main_data.csv` dibuat atau diperbarui.

## 6. Jalankan dashboard Streamlit
Setelah `main_data.csv` tersedia, jalankan perintah berikut dari root project.

```bash
streamlit run dashboard/dashboard.py
```

## 7. Buka dashboard di browser
Jika dashboard tidak terbuka otomatis, salin URL lokal yang muncul di terminal, biasanya:

```text
http://localhost:8501
```
