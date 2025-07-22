@echo off
REM MT19937 C++ Kütüphanesi Compile Scripti

echo ============================================
echo    MT19937 C++ KÜTÜPHANE COMPILE
echo ============================================
echo.

REM G++ varlığını kontrol et
g++ --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] g++ bulunamadi!
    echo MinGW-w64 veya Visual Studio Build Tools yukleyin.
    echo.
    echo Alternatif indirme linkleri:
    echo - MinGW-w64: https://www.mingw-w64.org/downloads/
    echo - MSYS2: https://www.msys2.org/
    echo.
    pause
    exit /b 1
)

echo [INFO] g++ bulundu:
REM 'head' komutu yerine 'for /f' kullanarak ilk satırı alıyoruz
for /f "delims=" %%i in ('g++ --version') do (
    echo %%i
    goto :skip_gpp_version
)
:skip_gpp_version

echo.
echo [INFO] MT19937 C++ kodu compile ediliyor...

REM C++ dosyasini kontrol et
if not exist "mt19937_wrapper.cpp" (
    echo [ERROR] mt19937_wrapper.cpp dosyasi bulunamadi!
    echo Bu dosyayi ana klasore kopyalayin.
    pause
    exit /b 1
)

REM Windows icin DLL compile et
g++ -shared -fPIC -O2 -std=c++11 mt19937_wrapper.cpp -o mt19937_wrapper.dll

if errorlevel 1 (
    echo.
    echo [ERROR] Compile basarisiz!
    echo Hata detaylarini kontrol edin.
    pause
    exit /b 1
)

echo [SUCCESS] MT19937 kutuphanesi basariyla compile edildi!
echo.

REM Gerekli runtime DLL'lerini kopyala
echo [INFO] Gerekli runtime DLL'leri kopyalanıyor...
set MINGW_BIN_PATH=C:\msys64\mingw64\bin
copy "%MINGW_BIN_PATH%\libstdc++-6.dll" . >nul 2>&1
copy "%MINGW_BIN_PATH%\libgcc_s_seh-1.dll" . >nul 2>&1
copy "%MINGW_BIN_PATH%\libwinpthread-1.dll" . >nul 2>&1
echo [INFO] Runtime DLL'leri kopyalandı.

REM Dosya boyutunu goster
if exist "mt19937_wrapper.dll" (
    for %%A in (mt19937_wrapper.dll) do (
        echo 📄 Dosya: mt19937_wrapper.dll (%%~zA bytes)
    )
)

echo.
echo [INFO] Test ediliyor...

REM Python testi calistir
python -c "from mt19937_random import test_mt19937; test_mt19937()"

if errorlevel 1 (
    echo.
    echo [WARNING] Python testi basarisiz. Manuel test yapın:
    echo python -c "import mt19937_random; print('OK')"
) else (
    echo.
    echo ✅ MT19937 C++ kutuphanesi hazir ve calisir durumda!
)

echo.
echo 🔄 Simdi anahtar uretimi yapabilirsiniz:
echo    generate_keys.bat
echo.

pause
