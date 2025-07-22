# 🚀 Anahtar Üretici Deney - Kurulum Rehberi

Bu rehber, projeyi sıfırdan kurmak için gereken tüm adımları içerir.

## 📁 1. Klasör Yapısını Oluşturun

Desktop'ta bir terminal açın ve şu komutları çalıştırın:

### Windows (Command Prompt):
```cmd
cd Desktop
mkdir keygen-experiment
cd keygen-experiment

REM Ana klasörleri oluştur
mkdir src
mkdir output\keys
mkdir output\test_results
mkdir output\reports
mkdir logs

REM Boş __init__.py dosyası oluştur
echo. > src\__init__.py
```

### Linux/Mac (Terminal):
```bash
cd Desktop
mkdir keygen-experiment
cd keygen-experiment

# Ana klasörleri oluştur
mkdir -p src
mkdir -p output/{keys,test_results,reports}
mkdir -p logs

# Boş __init__.py dosyası oluştur
touch src/__init__.py
```

## 📝 2. Dosyaları Oluşturun

Aşağıdaki dosyaları belirtilen konumlarda oluşturun:

### 📄 Ana Dosyalar (keygen-experiment/ klasöründe):
- `main.py` - Ana deney scripti
- `requirements.txt` - Python gereksinimleri
- `setup.py` - Kurulum scripti
- `README.md` - Dokümantasyon
- `run_experiment.bat` - Windows çalıştırma scripti
- `run_experiment.sh` - Linux/Mac çalıştırma scripti

### 📁 src/ klasöründe:
- `__init__.py` - Paket tanımı
- `config.py` - Deney konfigürasyonu
- `generators.py` - Anahtar üretici algoritmaları
- `testers.py` - İstatistiksel test modülü
- `utils.py` - Yardımcı fonksiyonlar

## ⚙️ 3. Python Ortamını Hazırlayın

### Python Versiyonu Kontrolü:
```bash
python --version
# veya
python3 --version

# 3.8 veya üzeri olmalı
```

### Virtual Environment Oluşturun:
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac  
python3 -m venv venv
source venv/bin/activate
```

### Gereksinimleri Yükleyin:
```bash
pip install -r requirements.txt
```

## 🗂️ 4. Final Klasör Yapısı

İşlem sonunda klasör yapınız şu şekilde olmalı:

```
Desktop/keygen-experiment/
├── main.py ⭐
├── requirements.txt ⭐
├── setup.py ⭐
├── README.md ⭐
├── run_experiment.bat ⭐ (Windows)
├── run_experiment.sh ⭐ (Linux/Mac)
├── KURULUM_REHBERI.md ⭐ (Bu dosya)
│
├── src/ ⭐
│   ├── __init__.py ⭐
│   ├── config.py ⭐
│   ├── generators.py ⭐
│   ├── testers.py ⭐
│   └── utils.py ⭐
│
├── venv/ (Virtual environment)
│
├── output/ (Boş klasörler)
│   ├── keys/
│   ├── test_results/
│   └── reports/
│
└── logs/ (Boş klasör)
```

**⭐ işareti**: Siz tarafından oluşturulması gereken dosyalar

## 🚀 5. Çalıştırın

### Otomatik Çalıştırma (Önerilen):
```bash
# Windows
run_experiment.bat

# Linux/Mac
chmod +x run_experiment.sh
./run_experiment.sh
```

### Manuel Çalıştırma:
```bash
# Virtual environment aktifleştirin
source venv/bin/activate  # Linux/Mac
# veya
venv\Scripts\activate     # Windows

# Deneyi başlatın
python main.py
```

## ✅ 6. Başarı Kontrolü

Deney başarılı olursa şu dosyalar oluşmalı:

### Ham Anahtarlar (`output/keys/`):
```
sha256_shrinking_128_keys.txt
sha256_shrinking_256_keys.txt
...
random_aes_4096_keys.txt
(Toplam 36 dosya)
```

### Test Sonuçları (`output/test_results/`):
```
sha256_shrinking_128_threshold_001.csv
sha256_shrinking_128_threshold_005.csv
...
random_aes_4096_threshold_005.csv
(Toplam 72 dosya)
```

### Final Rapor (`output/reports/`):
```
final_experiment_results.csv ⭐ (En önemli dosya)
```

## 🔍 7. Sonuçları İnceleme

### Excel/LibreOffice ile:
```
output/reports/final_experiment_results.csv dosyasını açın
```

### Python ile:
```python
import pandas as pd
df = pd.read_csv('output/reports/final_experiment_results.csv')
print(df.head())
print(df.groupby('source_type')['pass_rate_percent'].mean())
```

## ❗ 8. Sorun Giderme

### Problem: "ModuleNotFoundError"
**Çözüm**: Virtual environment aktif mi kontrol edin
```bash
# Tekrar aktifleştirin
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

### Problem: "Permission Denied"
**Çözüm**: Script'i çalıştırılabilir yapın
```bash
# Linux/Mac
chmod +x run_experiment.sh
```

### Problem: Çok yavaş çalışıyor
**Çözüm**: `src/config.py`'da `KEYS_PER_COMBINATION = 100` yapın

### Problem: Memory Error
**Çözüm**: Sadece küçük uzunlukları test edin:
```python
# src/config.py dosyasında
KEY_LENGTHS = [128, 256, 512]  # 1024, 2048, 4096'yı kaldırın
```

## 📞 9. Yardım

- **Log dosyası**: `logs/experiment.log`
- **Hata mesajları**: Terminal çıktısını kaydedin
- **Test verileri**: `output/test_results/` klasörünü kontrol edin

## 🎯 10. Beklenen Sonuç

Deney başarıyla tamamlandıktan sonra:

1. **36,000 anahtar** üretilmiş olacak
2. **324,000 test** yapılmış olacak  
3. **Final CSV** algoritma performanslarını gösterecek
4. **Yaklaşık 45-60 dakika** sürmüş olacak

**🎉 Başarılar! Artık kriptografik anahtar üretici algoritmalarının kapsamlı analizine sahipsiniz.**

---

## 📋 Hızlı Kontrol Listesi

- [ ] Python 3.8+ yüklü
- [ ] Tüm dosyalar oluşturuldu
- [ ] Virtual environment hazır  
- [ ] requirements.txt yüklendi
- [ ] Klasör yapısı doğru
- [ ] `python main.py` çalışıyor
- [ ] Çıktı dosyaları oluşuyor

**Hepsi ✅ ise deney hazır! 🚀**