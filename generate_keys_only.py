#!/usr/bin/env python3
"""
Sadece Anahtar Üretimi Scripti
36 kombinasyon x 1000 anahtar = 36,000 anahtar
"""

import time
from pathlib import Path

# Yeni modülleri import et
from src.generators_mt19937 import KeyGeneratorFactory
from src.config import ExperimentConfig
from src.utils_fixed import FileManager, Logger

class KeyGenerationPipeline:
    """Sadece anahtar üretimi pipeline"""
    
    def __init__(self):
        self.config = ExperimentConfig()
        self.file_manager = FileManager()
        self.logger = Logger("keygen.log")  # logs/keygen.log
        self.generator_factory = KeyGeneratorFactory()
        
        # Çıktı klasörlerini oluştur
        self.setup_directories()
        
    def setup_directories(self):
        """Gerekli klasörleri oluştur"""
        dirs = [
            'output/keys',      # Ham anahtar dosyaları
            'logs'              # Log dosyaları
        ]
        
        for dir_path in dirs:
            Path(dir_path).mkdir(parents=True, exist_ok=True)
            
        self.logger.info("Anahtar üretimi klasör yapısı hazırlandı")
        
    def generate_all_combinations(self):
        """36 kombinasyonun hepsini üret"""
        self.logger.info("=== ANAHTAR ÜRETİMİ BAŞLADI ===")
        
        total_combinations = len(self.config.get_all_combinations())
        current_combo = 0
        total_keys_generated = 0
        start_time = time.time()
        
        print("🚀 ANAHTAR ÜRETİMİ BAŞLIYOR")
        print("=" * 50)
        print(f"Toplam kombinasyon: {total_combinations}")
        print(f"Her kombinasyondan: 1000 anahtar")
        print(f"Toplam hedef: {total_combinations * 1000:,} anahtar")
        print("=" * 50)
        print()
        
        for combo in self.config.get_all_combinations():
            current_combo += 1
            source_type, method_type, key_length = combo
            
            combo_name = f"{source_type}_{method_type}_{key_length}"
            self.logger.info(f"[{current_combo}/{total_combinations}] Üretiliyor: {combo_name}")
            
            print(f"🔑 [{current_combo:2}/{total_combinations}] {combo_name} - 1000 anahtar üretiliyor...")
            
            combo_start_time = time.time()
            
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
                    elapsed = time.time() - combo_start_time
                    rate = (i + 1) * key_length / elapsed if elapsed > 0 else 0
                    print(f"   {i + 1}/1000 tamamlandı ({rate:,.0f} bit/sec)")
                    
            combo_elapsed = time.time() - combo_start_time
            total_bits = 1000 * key_length
            combo_rate = total_bits / combo_elapsed if combo_elapsed > 0 else 0
            
            # Anahtarları kaydet
            key_file = f"output/keys/{combo_name}_keys.txt"
            self.file_manager.save_keys(keys, key_file)
            
            total_keys_generated += 1000
            
            print(f"   ✅ Tamamlandı: {combo_elapsed:.2f}s, {combo_rate:,.0f} bit/sec")
            print(f"   📁 Kaydedildi: {key_file}")
            
            self.logger.info(f"{combo_name}: 1000 anahtar üretildi ({combo_elapsed:.2f}s, {combo_rate:,.0f} bit/sec)")
            
            # Genel progress
            total_elapsed = time.time() - start_time
            overall_progress = (current_combo / total_combinations) * 100
            
            if total_elapsed > 0:
                estimated_total = total_elapsed / (current_combo / total_combinations)
                remaining = estimated_total - total_elapsed
                print(f"   📊 Genel ilerleme: %{overall_progress:.1f} (kalan ~{remaining/60:.1f} dakika)")
            
            print()
            
        # Final özet
        total_elapsed = time.time() - start_time
        overall_rate = (total_keys_generated * 1000) / total_elapsed if total_elapsed > 0 else 0  # Ortalama bit uzunluğu
        
        print("🎉 ANAHTAR ÜRETİMİ TAMAMLANDI!")
        print("=" * 50)
        print(f"📊 ÖZET:")
        print(f"   - Toplam kombinasyon: {total_combinations}")
        print(f"   - Toplam anahtar: {total_keys_generated:,}")
        print(f"   - Toplam süre: {total_elapsed/60:.1f} dakika")
        print(f"   - Ortalama hız: {overall_rate:,.0f} anahtar/sec")
        print()
        print(f"📁 Çıktı klasörü: output/keys/")
        print(f"📝 Log dosyası: logs/keygen.log")
        print()
        print("🔄 Devam için: test_keys.bat")
        
        self.logger.info(f"Anahtar üretimi tamamlandı! {total_keys_generated:,} anahtar, {total_elapsed/60:.1f} dakika")

def main():
    """Ana fonksiyon"""
    try:
        pipeline = KeyGenerationPipeline()
        pipeline.generate_all_combinations()
        
    except Exception as e:
        print(f"❌ HATA: {e}")
        import traceback
        traceback.print_exc()
        
        # Log'a da yaz
        logger = Logger("keygen.log")
        logger.error(f"Anahtar üretimi hatası: {e}")
        
        input("Devam etmek için Enter tuşuna basın...")

if __name__ == "__main__":
    main()