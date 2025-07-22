@echo off
REM Sadece Anahtar Üretimi Scripti

echo ============================================
echo       ANAHTAR ÜRETIM AŞAMASI
echo ============================================
echo.

REM Virtual environment kontrol
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
) else (
    echo [ERROR] Virtual environment bulunamadi!
    echo Önce run_experiment.bat ile kurulum yapın.
    pause
    exit /b 1
)

echo [INFO] Virtual environment aktif.
echo.

REM Python scripti çalıştır
echo [INFO] Anahtar üretimi başlıyor...
python generate_keys_only.py

if errorlevel 1 (
    echo.
    echo [ERROR] Anahtar üretiminde hata oluştu!
    echo Detaylar için logs\keygen.log dosyasını kontrol edin.
    pause
    exit /b 1
)

REM Sonuçları kontrol et
set key_count=0
for /f %%i in ('dir /b "output\keys\*.txt" 2^>nul ^| find /c /v ""') do set key_count=%%i

echo.
echo ============================================
echo    ANAHTAR ÜRETIM TAMAMLANDI!
echo ============================================
echo.
echo 📊 Sonuçlar:
echo   - Üretilen dosya sayısı: %key_count%/36
echo   - Klasör: output\keys\
echo   - Log: logs\keygen.log
echo.

if "%key_count%"=="36" (
    echo ✅ Tüm kombinasyonlar başarıyla üretildi!
    echo.
    echo 🔄 Şimdi testleri çalıştırmak için:
    echo    test_keys.bat
) else (
    echo ⚠️  Eksik anahtar dosyası var. Kontrol edin.
)

echo.
echo Devam etmek için herhangi bir tuşa basın...
pause >nul