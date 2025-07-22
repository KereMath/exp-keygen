@echo off
REM Anahtar Üretici Deney Çalıştırma Scripti (Windows)

echo ============================================
echo    ANAHTAR URETICI DENEYSEL PIPELINE
echo ============================================
echo.

REM Python versionunu kontrol et
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python bulunamadi! Python 3.8+ yukleyin.
    pause
    exit /b 1
)

echo [INFO] Python bulundu: 
python --version

REM Virtual environment var mi kontrol et
if not exist "venv\" (
    echo.
    echo [INFO] Virtual environment olusturuluyor...
    python -m venv venv
    if errorlevel 1 (
        echo [ERROR] Virtual environment olusturulamadi!
        pause
        exit /b 1
    )
    echo [SUCCESS] Virtual environment olusturuldu.
)

REM Virtual environment'i aktiflestir
echo.
echo [INFO] Virtual environment aktiflestirilyor...
call venv\Scripts\activate.bat

REM Gereksinimleri yukle
echo [INFO] Gereksinimler kontrol ediliyor...
pip install -r requirements.txt --quiet

if errorlevel 1 (
    echo [ERROR] Gereksinimler yuklenemedi!
    pause
    exit /b 1
)

echo [SUCCESS] Gereksinimler hazir.
echo.

REM Cikti klasorlerini olustur
if not exist "output\keys\" mkdir output\keys
if not exist "output\test_results\" mkdir output\test_results
if not exist "output\reports\" mkdir output\reports
if not exist "logs\" mkdir logs

echo [INFO] Klasor yapisi hazir.
echo.

REM Ana deney scriptini calistir
echo ============================================
echo    DENEY BASLIYOR...
echo ============================================
echo.

python main.py

if errorlevel 1 (
    echo.
    echo [ERROR] Deney sirasinda hata olustu!
    echo Detaylar icin logs\experiment.log dosyasini kontrol edin.
    pause
    exit /b 1
)

echo.
echo ============================================
echo    DENEY TAMAMLANDI!
echo ============================================
echo.
echo Sonuclar:
echo   - output\keys\                (Ham anahtarlar)
echo   - output\test_results\        (Test sonuclari)  
echo   - output\reports\             (Final rapor)
echo   - logs\experiment.log         (Log dosyasi)
echo.

REM Final raporunu goster
if exist "output\reports\final_experiment_results.csv" (
    echo Final rapor olusturuldu: output\reports\final_experiment_results.csv
    echo.
    choice /C YN /M "Final raporunu Excel'de acmak istiyor musunuz"
    if !errorlevel!==1 (
        start excel "output\reports\final_experiment_results.csv"
    )
)

echo.
echo Deney tamamlandi. Herhangi bir tusa basin...
pause >nul