@echo off
REM Sadece Test Aşaması Scripti

echo ============================================
echo         TEST AŞAMASI
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

REM Key dosyalarını kontrol et
set key_count=0
for /f %%i in ('dir /b "output\keys\*.txt" 2^>nul ^| find /c /v ""') do set key_count=%%i

if "%key_count%"=="0" (
    echo [ERROR] Anahtar dosyasi bulunamadi!
    echo Önce generate_keys.bat ile anahtar üretin.
    pause
    exit /b 1
)

echo [INFO] %key_count% anahtar dosyasi bulundu.
echo.

REM Test sonuçlarını kontrol et
set test_count=0
for /f %%i in ('dir /b "output\test_results\*.csv" 2^>nul ^| find /c /v ""') do set test_count=%%i
echo [INFO] %test_count% test dosyasi zaten mevcut (atlanacak).
echo.

echo ============================================
echo    TESTLER BAŞLIYOR...
echo ============================================
echo.

REM Test scripti çalıştır
python test_keys_only.py

if errorlevel 1 (
    echo.
    echo [ERROR] Test aşamasında hata oluştu!
    echo Detaylar için logs\testing.log dosyasını kontrol edin.
    pause
    exit /b 1
)

echo.
echo ============================================
echo    TESTLER TAMAMLANDI!
echo ============================================
echo.

REM Sonuçları kontrol et
set final_test_count=0
for /f %%i in ('dir /b "output\test_results\*.csv" 2^>nul ^| find /c /v ""') do set final_test_count=%%i

echo 📊 Sonuçlar:
echo   - Test sonucu dosyası: %final_test_count%/72
echo   - Klasör: output\test_results\
echo   - Log: logs\testing.log

REM Final raporu kontrol et
if exist "output\reports\detailed_experiment_results.csv" (
    echo   - Final rapor: output\reports\detailed_experiment_results.csv
    echo.
    echo ✅ Analiz tamamlandı!
    echo.
    choice /C YN /M "Final raporunu Excel'de açmak istiyor musunuz"
    if !errorlevel!==1 (
        start excel "output\reports\detailed_experiment_results.csv"
    )
) else (
    echo   - Final rapor: OLUŞTURULAMADI
    echo.
    echo ⚠️  Final rapor eksik. Log dosyalarını kontrol edin.
)

echo.
echo Devam etmek için herhangi bir tuşa basın...
pause >nul