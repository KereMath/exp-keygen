#!/usr/bin/env python3
"""
Anahtar Üretici Deney Pipeline
=====================================

Bu script 36 farklı kombinasyonla anahtar üretir ve test eder:
- 2 Kaynak (SHA256, Random) 
- 3 Yöntem (Shrinking, Alternating, AES)
- 6 Uzunluk (128, 256, 512, 1024, 2048, 4096 bit)

Her kombinasyondan 1000 anahtar üretir ve test eder.
"""

import os
import time
from pathlib import Path
import pandas as pd

from src.generators import KeyGeneratorFactory
from src.testers import StatisticalTester
from src.config import ExperimentConfig
from src.utils import FileManager, Logger

class ExperimentPipeline:
    """Ana deney pipeline sınıfı"""
    
    def __init__(self):
        self.config = ExperimentConfig()
        self.file_manager = FileManager()
        self.logger = Logger("experiment.log")
        self.generator_factory = KeyGeneratorFactory()
        self.tester = StatisticalTester()
        
        # Çıktı klasörlerini oluştur
        self.setup_directories()
        
    def setup_directories(self):
        """Gerekli klasörleri oluştur"""
        dirs = [
            'output/keys',           # Ham anahtar dosyaları
            'output/test_results',   # Test sonuçları CSV'leri
            'output/reports',        # Final raporlar
            'logs'                   # Log dosyaları
        ]
        
        for dir_path in dirs:
            Path(dir_path).mkdir(parents=True, exist_ok=True)
            
        self.logger.info("Klasör yapısı hazırlandı")
        
    def generate_all_combinations(self):
        """36 kombinasyonun hepsini üret"""
        self.logger.info("=== AŞAMA 1: ANAHTAR ÜRETİMİ BAŞLADI ===")
        
        total_combinations = len(self.config.get_all_combinations())
        current_combo = 0
        
        for combo in self.config.get_all_combinations():
            current_combo += 1
            source_type, method_type, key_length = combo
            
            combo_name = f"{source_type}_{method_type}_{key_length}"
            self.logger.info(f"[{current_combo}/{total_combinations}] Üretiliyor: {combo_name}")
            
            print(f"🔑 [{current_combo:2}/{total_combinations}] {combo_name} - 1000 anahtar üretiliyor...")
            
            start_time = time.time()
            
            # Generator'ı al
            generator = self.generator_factory.get_generator(source_type, method_type)
            
            # 1000 anahtar üret
            keys = []
            for i in range(1000):
                seed = generator.generate_seed()
                key = generator.generate_key(seed, key_length)
                keys.append(key)
                
                # Progress göster
                if (i + 1) % 100 == 0:
                    print(f"   {i + 1}/1000 tamamlandı...")
                    
            generation_time = time.time() - start_time
            
            # Anahtarları kaydet
            key_file = f"output/keys/{combo_name}_keys.txt"
            self.file_manager.save_keys(keys, key_file)
            
            self.logger.info(f"{combo_name}: 1000 anahtar üretildi ({generation_time:.2f}s)")
            print(f"   ✅ Kaydedildi: {key_file}")
            
        print("\n🎉 AŞAMA 1 TAMAMLANDI: Tüm anahtarlar üretildi!\n")
        
    def test_all_keys(self):
        """Tüm anahtarları test et"""
        self.logger.info("=== AŞAMA 2: İSTATİSTİKSEL TESTLER BAŞLADI ===")
        
        key_files = list(Path("output/keys").glob("*.txt"))
        total_files = len(key_files)
        current_file = 0
        
        for key_file in key_files:
            current_file += 1
            combo_name = key_file.stem.replace("_keys", "")
            
            print(f"🧪 [{current_file:2}/{total_files}] Test ediliyor: {combo_name}")
            
            # Anahtarları yükle
            keys = self.file_manager.load_keys(str(key_file))
            key_length = int(combo_name.split("_")[-1])
            
            start_time = time.time()
            
            # Her iki eşik değeri için test et
            for threshold in [0.01, 0.05]:
                threshold_str = str(threshold).replace(".", "")
                
                print(f"   Eşik {threshold} test ediliyor...")
                
                test_results = []
                passed_count = 0
                
                for i, key in enumerate(keys):
                    # Tüm testleri uygula
                    results = self.tester.run_all_tests(key, key_length)
                    
                    # Eşik kontrolü yap
                    passed = self.tester.check_thresholds(results, key_length, threshold)
                    if passed:
                        passed_count += 1
                    
                    # Test sonucunu kaydet
                    result_row = {
                        'key_id': i + 1,
                        'key_bits': ''.join(['1' if b else '0' for b in key]),
                        'passed': passed,
                        **results  # Tüm test sonuçlarını ekle
                    }
                    test_results.append(result_row)
                    
                    # Progress göster
                    if (i + 1) % 100 == 0:
                        print(f"      {i + 1}/1000 test tamamlandı...")
                
                # CSV'ye kaydet
                csv_file = f"output/test_results/{combo_name}_threshold_{threshold_str}.csv"
                df = pd.DataFrame(test_results)
                df.to_csv(csv_file, index=False)
                
                test_time = time.time() - start_time
                pass_rate = (passed_count / 1000) * 100
                
                print(f"   ✅ Eşik {threshold}: {passed_count}/1000 geçti (%{pass_rate:.1f}) - {csv_file}")
                self.logger.info(f"{combo_name} threshold {threshold}: {passed_count}/1000 passed ({pass_rate:.1f}%)")
        
        print("\n🎉 AŞAMA 2 TAMAMLANDI: Tüm testler bitti!\n")
        
    def generate_final_report(self):
        """Final raporu oluştur"""
        self.logger.info("=== AŞAMA 3: FİNAL RAPORU OLUŞTURULUYOR ===")
        
        print("📊 Final raporu oluşturuluyor...")
        
        # Test sonuçlarını topla
        final_results = []
        
        for combo in self.config.get_all_combinations():
            source_type, method_type, key_length = combo
            combo_name = f"{source_type}_{method_type}_{key_length}"
            
            for threshold in [0.01, 0.05]:
                threshold_str = str(threshold).replace(".", "")
                csv_file = f"output/test_results/{combo_name}_threshold_{threshold_str}.csv"
                
                if os.path.exists(csv_file):
                    df = pd.read_csv(csv_file)
                    passed_count = df['passed'].sum()
                    pass_rate = (passed_count / 1000) * 100
                    
                    final_results.append({
                        'source_type': source_type,
                        'method_type': method_type,
                        'key_length': key_length,
                        'threshold': threshold,
                        'total_keys': 1000,
                        'passed_keys': passed_count,
                        'failed_keys': 1000 - passed_count,
                        'pass_rate_percent': pass_rate
                    })
        
        # Final CSV'yi kaydet
        final_df = pd.DataFrame(final_results)
        final_df = final_df.sort_values(['source_type', 'method_type', 'key_length', 'threshold'])
        
        final_file = "output/reports/final_experiment_results.csv"
        final_df.to_csv(final_file, index=False)
        
        print(f"✅ Final rapor kaydedildi: {final_file}")
        
        # Özet istatistikleri göster
        print("\n📈 ÖZET İSTATİSTİKLER:")
        print("=" * 60)
        
        for threshold in [0.01, 0.05]:
            threshold_data = final_df[final_df['threshold'] == threshold]
            avg_pass_rate = threshold_data['pass_rate_percent'].mean()
            min_pass_rate = threshold_data['pass_rate_percent'].min()
            max_pass_rate = threshold_data['pass_rate_percent'].max()
            
            print(f"Eşik {threshold}:")
            print(f"  Ortalama geçme oranı: %{avg_pass_rate:.1f}")
            print(f"  En düşük geçme oranı: %{min_pass_rate:.1f}")
            print(f"  En yüksek geçme oranı: %{max_pass_rate:.1f}")
            print()
            
        self.logger.info("Final raporu oluşturuldu")
        
    def run_full_experiment(self):
        """Tam deneyi çalıştır"""
        start_time = time.time()
        
        print("🚀 ANAHTAR ÜRETİCİ DENEYİ BAŞLIYOR")
        print("=" * 50)
        print(f"Toplam kombinasyon: {len(self.config.get_all_combinations())}")
        print(f"Her kombinasyondan: 1000 anahtar")
        print(f"Toplam anahtar: {len(self.config.get_all_combinations()) * 1000}")
        print(f"Test eşikleri: 0.01, 0.05")
        print("=" * 50)
        print()
        
        try:
            # Aşama 1: Anahtar üretimi
            self.generate_all_combinations()
            
            # Aşama 2: Testler
            self.test_all_keys()
            
            # Aşama 3: Final rapor
            self.generate_final_report()
            
            total_time = time.time() - start_time
            
            print("🎉 DENEY TAMAMLANDI!")
            print("=" * 50)
            print(f"Toplam süre: {total_time/60:.1f} dakika")
            print()
            print("📁 Çıktı dosyaları:")
            print(f"  - Ham anahtarlar: output/keys/")
            print(f"  - Test sonuçları: output/test_results/")
            print(f"  - Final rapor: output/reports/final_experiment_results.csv")
            print(f"  - Log dosyası: logs/experiment.log")
            
            self.logger.info(f"Deney tamamlandı! Toplam süre: {total_time/60:.1f} dakika")
            
        except Exception as e:
            print(f"❌ HATA: {e}")
            self.logger.error(f"Deney hatası: {e}")
            raise

def main():
    """Ana fonksiyon"""
    experiment = ExperimentPipeline()
    experiment.run_full_experiment()

if __name__ == "__main__":
    main()