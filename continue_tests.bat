@echo off
REM Testleri kaldığımız yerden devam ettir

echo ============================================
echo    TESTLERE KALDIĞIMIZ YERDEN DEVAM
echo ============================================
echo.

REM Virtual environment'ı aktifleştir
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
) else (
    echo [ERROR] Virtual environment bulunamadi!
    echo once run_experiment.bat calistirin.
    pause
    exit /b 1
)

echo [INFO] Virtual environment aktif.
echo.

REM Dosyaları kontrol et
if not exist "src\testers.py" (
    echo [ERROR] src\testers.py bulunamadi!
    echo Önce düzeltilmiş testers.py dosyasını kopyalayın.
    pause
    exit /b 1
)

if not exist "continue_tests.py" (
    echo [ERROR] continue_tests.py bulunamadi!
    echo Bu dosyayı ana klasörde oluşturun.
    pause
    exit /b 1
)

REM Key dosyalarını kontrol et
set key_count=0
for /f %%i in ('dir /b "output\keys\*.txt" 2^>nul ^| find /c /v ""') do set key_count=%%i

if "%key_count%"=="0" (
    echo [ERROR] output\keys klasorunde anahtar dosyasi bulunamadi!
    echo Once main.py ile anahtar uretimini tamamlayin.
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

REM Continue script'i çalıştır
python continue_tests.py

if errorlevel 1 (
    echo.
    echo [ERROR] Test aşamasında hata oluştu!
    echo Detaylar için logs\continue_tests.log dosyasını kontrol edin.
    pause
    exit /b 1
)

echo.
echo ============================================
echo    TESTLER TAMAMLANDI!
echo ============================================
echo.

REM Sonuçları göster
if exist "output\reports\final_experiment_results.csv" (
    echo ✅ Final rapor oluşturuldu: output\reports\final_experiment_results.csv
    echo.
    
    echo Dosya boyutları:
    for /f "tokens=3" %%a in ('dir "output\reports\final_experiment_results.csv" ^| find "final_experiment_results.csv"') do echo   Final rapor: %%a bytes
    
    echo.
    choice /C YN /M "Final raporunu Excel'de açmak istiyor musunuz"
    if !errorlevel!==1 (
        start excel "output\reports\final_experiment_results.csv"
    )
) else (
    echo ❌ Final rapor oluşturulamadı!
)

echo.
echo 🎉 İşlem tamamlandı. Herhangi bir tuşa basın...
pause >nul