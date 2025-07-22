@echo off
REM Anahtar Üretici Deney - Tam Kurulum Scripti

echo ============================================
echo    ANAHTAR URETICI DENEY KURULUM
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

REM Virtual environment oluştur
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

REM Virtual environment'ı aktifleştir
echo.
echo [INFO] Virtual environment aktiflestirilyor...
call venv\Scripts\activate.bat

REM Gereksinimleri yükle
echo [INFO] Python gereksinimleri yukleniyor...
pip install -r requirements.txt --quiet

if errorlevel 1 (
    echo [ERROR] Python gereksinimleri yuklenemedi!
    pause
    exit /b 1
)

echo [SUCCESS] Python gereksinimleri hazir.

REM Klasör yapısını oluştur
echo.
echo [INFO] Klasor yapisi olusturuluyor...

mkdir output\keys 2>nul
mkdir output\test_results 2>nul
mkdir output\detailed_results 2>nul
mkdir output\reports 2>nul
mkdir logs 2>nul

echo [SUCCESS] Klasor yapisi hazir.

REM G++ kontrolü
echo.
echo [INFO] C++ compiler kontrol ediliyor...
g++ --version >nul 2>&1
if errorlevel 1 (
    echo [WARNING] g++ bulunamadi!
    echo MT19937 C++ kutuphanesi icin gerekli.
    echo.
    echo Kurulum onerileri:
    echo 1. MinGW-w64: https://www.mingw-w64.org/downloads/
    echo 2. MSYS2: https://www.msys2.org/
    echo 3. Visual Studio Build Tools
    echo.
    choice /C YN /M "g++ olmadan devam etmek istiyor musunuz"
    if !errorlevel!==2 (
        echo Kurulumu iptal ediliyor...
        pause
        exit /b 1
    )
    echo [WARNING] MT19937 manual compile gerekecek.
) else (
    echo [SUCCESS] g++ bulundu, MT19937 otomatik compile edilecek.
)

REM Dosya varlığını kontrol et
echo.
echo [INFO] Proje dosyalari kontrol ediliyor...

set missing_files=0

if not exist "src\config.py" (
    echo [ERROR] src\config.py eksik
    set missing_files=1
)

if not exist "src\generators_mt19937.py" (
    echo [ERROR] src\generators_mt19937.py eksik
    set missing_files=1
)

if not exist "src\testers_fixed.py" (
    echo [ERROR] src\testers_fixed.py eksik
    set missing_files=1
)

if not exist "src\utils_fixed.py" (
    echo [ERROR] src\utils_fixed.py eksik
    set missing_files=1
)

if not exist "mt19937_wrapper.cpp" (
    echo [ERROR] mt19937_wrapper.cpp eksik
    set missing_files=1
)

if not exist "mt19937_random.py" (
    echo [ERROR] mt19937_random.py eksik
    set missing_files=1
)

if not exist "generate_keys_only.py" (
    echo [ERROR] generate_keys_only.py eksik
    set missing_files=1
)

if not exist "test_keys_only.py" (
    echo [ERROR] test_keys_only.py eksik
    set missing_files=1
)

if %missing_files%==1 (
    echo.
    echo [ERROR] Eksik dosyalar var! Tum dosyalari kopyalayin.
    pause
    exit /b 1
)

echo [SUCCESS] Tum proje dosyalari mevcut.

REM MT19937 compile et (eğer g++ varsa)
g++ --version >nul 2>&1
if not errorlevel 1 (
    echo.
    echo [INFO] MT19937 C++ kutuphanesi compile ediliyor...
    
    g++ -shared -fPIC -O2 -std=c++11 mt19937_wrapper.cpp -o mt19937_wrapper.dll
    
    if errorlevel 1 (
        echo [ERROR] MT19937 compile basarisiz!
        echo Manuel compile gerekebilir: compile_mt19937.bat
    ) else (
        echo [SUCCESS] MT19937 C++ kutuphanesi hazir.
        
        REM Quick test
        python -c "import mt19937_random; print('MT19937 test OK')" 2>nul
        if errorlevel 1 (
            echo [WARNING] MT19937 import test basarisiz.
        ) else (
            echo [SUCCESS] MT19937 Python wrapper calisir durumda.
        )
    )
)

echo.
echo ============================================
echo    KURULUM TAMAMLANDI!
echo ============================================
echo.

echo 📊 Sistem Durumu:
echo   ✅ Python: Hazir
echo   ✅ Virtual Env: Hazir
echo   ✅ Gereksinimler: Yuklu
echo   ✅ Klasorler: Olusturuldu
echo   ✅ Proje Dosyalari: Mevcut

if exist "mt19937_wrapper.dll" (
    echo   ✅ MT19937 C++: Compile edildi
) else (
    echo   ⚠️  MT19937 C++: Manuel compile gerekli
)

echo.
echo 🚀 Kullanima Hazir!
echo.
echo Adimlar:
echo   1. generate_keys.bat   (36,000 anahtar uret)
echo   2. test_keys.bat       (Testleri calistir)
echo.
echo Alternatif:
echo   - compile_mt19937.bat  (MT19937 manuel compile)
echo.

pause