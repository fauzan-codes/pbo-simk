@echo off
title Setup SIMK - Sistem Informasi Manajemen Klinik
echo ========================================================
echo        Memulai Setup Lingkungan Pengembangan SIMK
echo ========================================================
echo.

IF NOT EXIST "venv\Scripts\activate.bat" (
    echo [1/4] Membuat Virtual Environment "venv"...
    python -m venv venv
    if errorlevel 1 (
        echo [ERROR] Gagal membuat virtual environment! Pastikan Python sudah terinstal.
        pause
        exit /b
    )
) ELSE (
    echo [1/4] Virtual Environment sudah ada.
)

echo [2/4] Mengaktifkan Virtual Environment...
call venv\Scripts\activate

echo [3/4] Menginstal dependensi dari requirements.txt...
pip install -r requirements.txt
if errorlevel 1 (
    echo [ERROR] Gagal menginstal dependensi! Pastikan file requirements.txt ada.
    pause
    exit /b
)

echo [4/4] Memeriksa konfigurasi Tailwind...

IF NOT EXIST "theme\" (
    echo [!] Folder theme belum ditemukan. Menjalankan tailwind init...
    echo | python manage.py tailwind init
)

echo Menginstal dependensi Tailwind CSS...
python manage.py tailwind install

if errorlevel 1 (
    echo [ERROR] Gagal menginstal Tailwind! Pastikan Node.js sudah terinstal.
    pause
    exit /b
)

echo.
echo ========================================================
echo Memeriksa Kesehatan Sistem Django...
echo ========================================================
python manage.py check

if errorlevel 1 (
    echo.
    echo [WARNING] Ada masalah pada sistem Django - lihat pesan di atas.
) else (
    echo.
    echo [SUKSES] Sistem Django berjalan tanpa masalah kritikal.
)

echo.
echo ========================================================
echo SETUP SELESAI!
echo ========================================================
