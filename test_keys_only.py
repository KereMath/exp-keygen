#!/usr/bin/env python3
"""
Sadece Test Aşaması Scripti - TAMAMEN HATASIZ VERSIYON
Detaylı test analizi - Her testin ayrı başarı oranı
"""

import os
import time
from pathlib import Path
import pandas as pd

from src.testers_fixed import StatisticalTester  # Düzeltilmiş threshold kontrolü
from src.config import ExperimentConfig
from src.utils_fixed import FileManager, Logger

class TestingPipeline:
    """Sadece test pipeline"""
    
    def __init__(self):
        self.config = ExperimentConfig()
        self.file_manager = FileManager()
        self.logger = Logger("testing.log")  # logs/testing.log
        self.tester = StatisticalTester()
        
        # Test isimleri
        self.test_names = [
            'frequency', 'run_count', 'run_L1', 'template_4_1', 
            'template_4_2', 'template_4_3', 'template_4_4', 
            'linear_complexity', 'blind_spot_complexity'
        ]
        
        # Çıktı klasörlerini oluştur
        self.setup_directories()
        
    def setup_directories(self):
        """Gerekli klasörleri oluştur"""
        dirs = [
            'output/test_results',    # Test sonuçları
            'output/detailed_results', # Detaylı sonuçlar
            'output/reports',         # Final raporlar
            'logs'                    # Log dosyaları
        ]
        
        for dir_path in dirs:
            Path(dir_path).mkdir(parents=True, exist_ok=True)
            
        self.logger.info("Test aşaması klasör yapısı hazırlandı")
    
    def test_all_keys(self):
        """Tüm anahtarları detaylı test et"""
        self.logger.info("=== İSTATİSTİKSEL TESTLER BAŞLADI ===")
        
        # Hangi key dosyaları var?
        key_files = list(Path("output/keys").glob("*.txt"))
        
        if not key_files:
            print("❌ HATA: output/keys/ klasöründe anahtar dosyası bulunamadı!")
            print("Önce generate_keys.bat çalıştırın.")
            return
        
        total_files = len(key_files)
        current_file = 0
        
        # Detaylı sonuçları topla
        detailed_results = []
        start_time = time.time()
        
        print("🧪 İSTATİSTİKSEL TESTLER BAŞLIYOR")
        print("=" * 50)
        print(f"Bulunan anahtar dosyası: {total_files}")
        print(f"Test edilecek eşikler: 0.01, 0.05")
        print(f"Test türü sayısı: {len(self.test_names)}")
        print("=" * 50)
        print()
        
        for key_file in key_files:
            current_file += 1
            combo_name = key_file.stem.replace("_keys", "")
            
            print(f"🔍 [{current_file:2}/{total_files}] Analiz ediliyor: {combo_name}")
            
            # Anahtarları yükle
            keys = self.file_manager.load_keys(str(key_file))
            
            if not keys:
                print(f"   ⚠️  Anahtar dosyası boş: {key_file}")
                continue
            
            key_length = int(combo_name.split("_")[-1])
            combo_start_time = time.time()
            
            # Her iki eşik değeri için test et
            for threshold in [0.01, 0.05]:
                print(f"   🔍 Eşik {threshold} test ediliyor...")
                
                # Her test için başarı sayacı
                test_pass_counts = {test_name: 0 for test_name in self.test_names}
                overall_pass_count = 0
                total_keys = len(keys)
                
                all_test_results = []
                
                for i, key in enumerate(keys):
                    try:
                        # Tüm testleri uygula
                        results = self.tester.run_all_tests(key, key_length)
                        
                        # Her testin bireysel başarısını kontrol et
                        individual_passes = {}
                        all_tests_passed = True
                        
                        for test_name in self.test_names:
                            if test_name in results:
                                individual_passed = self.tester.check_individual_test(
                                    test_name, results[test_name], key_length, threshold
                                )
                                individual_passes[f'{test_name}_passed'] = individual_passed
                                
                                if individual_passed:
                                    test_pass_counts[test_name] += 1
                                else:
                                    all_tests_passed = False
                            else:
                                # Test sonucu yoksa False say
                                individual_passes[f'{test_name}_passed'] = False
                                all_tests_passed = False
                        
                        # Tüm testleri geçti mi?
                        if all_tests_passed:
                            overall_pass_count += 1
                        
                        # Detaylı sonucu kaydet
                        result_row = {
                            'key_id': i + 1,
                            'key_bits': ''.join(['1' if b else '0' for b in key]),
                            'overall_passed': all_tests_passed,
                            **individual_passes,  # Her testin pass/fail durumu
                            **results            # Her testin sayısal sonucu
                        }
                        all_test_results.append(result_row)
                        
                        # Progress göster
                        if (i + 1) % 100 == 0:
                            elapsed = time.time() - combo_start_time
                            rate = (i + 1) / elapsed if elapsed > 0 else 0
                            print(f"      {i + 1}/{total_keys} test tamamlandı ({rate:.1f} test/sec)")
                            
                    except Exception as e:
                        print(f"      ⚠️  Key {i+1} test hatası: {str(e)[:50]}...")
                        
                        # Hatalı key için varsayılan sonuç ekle
                        result_row = {
                            'key_id': i + 1,
                            'key_bits': ''.join(['1' if b else '0' for b in key]),
                            'overall_passed': False
                        }
                        
                        # Her test için False ekle
                        for test_name in self.test_names:
                            result_row[f'{test_name}_passed'] = False
                            result_row[test_name] = -1  # Error değeri
                        
                        all_test_results.append(result_row)
                
                # Sonuçları kaydet
                threshold_str = str(threshold).replace(".", "")
                
                # Detaylı CSV dosyası
                csv_file = f"output/detailed_results/{combo_name}_threshold_{threshold_str}_detailed.csv"
                df = pd.DataFrame(all_test_results)
                df.to_csv(csv_file, index=False)
                
                # Basit test sonuçları CSV'si (eski format uyumluluğu için)
                simple_results = []
                for row in all_test_results:
                    simple_row = {
                        'key_id': row['key_id'],
                        'key_bits': row['key_bits'],
                        'passed': row['overall_passed']
                    }
                    # Sayısal test sonuçlarını ekle
                    for test_name in self.test_names:
                        if test_name in row:
                            simple_row[test_name] = row[test_name]
                    
                    simple_results.append(simple_row)
                
                simple_csv_file = f"output/test_results/{combo_name}_threshold_{threshold_str}.csv"
                simple_df = pd.DataFrame(simple_results)
                simple_df.to_csv(simple_csv_file, index=False)
                
                # Özet istatistikleri
                combo_elapsed = time.time() - combo_start_time
                overall_pass_rate = (overall_pass_count / total_keys) * 100
                
                print(f"   📊 Eşik {threshold} Sonuçları:")
                print(f"      🎯 TÜM testleri geçen: {overall_pass_count}/{total_keys} (%{overall_pass_rate:.1f})")
                
                # Her testin bireysel başarı oranı
                for test_name in self.test_names:
                    individual_rate = (test_pass_counts[test_name] / total_keys) * 100
                    status = "✅" if individual_rate >= 50 else "❌"
                    print(f"      {status} {test_name:20}: {test_pass_counts[test_name]:4}/{total_keys} (%{individual_rate:5.1f})")
                
                print(f"      💾 Sonuçlar: {csv_file}")
                
                # Sonuçları toplam tabloya ekle
                combo_parts = combo_name.split("_")
                if len(combo_parts) == 3:
                    combo_source, combo_method, combo_length = combo_parts
                else:
                    print(f"   ⚠️  Geçersiz combo name: {combo_name}")
                    continue
                
                result_summary = {
                    'source_type': combo_source,
                    'method_type': combo_method,
                    'key_length': int(combo_length),
                    'threshold': threshold,
                    'total_keys': total_keys,
                    'overall_passed': overall_pass_count,
                    'overall_pass_rate': overall_pass_rate
                }
                
                # Her testin bireysel sonuçlarını ekle
                for test_name in self.test_names:
                    result_summary[f'{test_name}_passed'] = test_pass_counts[test_name]
                    result_summary[f'{test_name}_pass_rate'] = (test_pass_counts[test_name] / total_keys) * 100
                
                detailed_results.append(result_summary)
                
                self.logger.info(f"{combo_name} threshold {threshold}: Overall {overall_pass_count}/{total_keys} ({overall_pass_rate:.1f}%)")
            
            # Combo tamamlandı
            combo_total_time = time.time() - combo_start_time
            print(f"   ⏱️  Toplam süre: {combo_total_time:.1f}s")
            print()

        print("\n🎉 TÜM TESTLER TAMAMLANDI!")
        
        # Final detaylı raporu oluştur
        self.generate_detailed_final_report(detailed_results, start_time)

    def generate_detailed_final_report(self, detailed_results, start_time):
        """Detaylı final raporu oluştur"""
        print("\n📊 Final raporları oluşturuluyor...")
        
        if not detailed_results:
            print("❌ Hiç sonuç bulunamadı!")
            return
        
        # DataFrame'e dönüştür
        df = pd.DataFrame(detailed_results)
        df = df.sort_values(['source_type', 'method_type', 'key_length', 'threshold'])
        
        # Final detaylı CSV
        detailed_file = "output/reports/detailed_experiment_results.csv"
        df.to_csv(detailed_file, index=False)
        
        # Basit final CSV (eski format uyumluluğu)
        simple_final = []
        for _, row in df.iterrows():
            simple_row = {
                'source_type': row['source_type'],
                'method_type': row['method_type'],
                'key_length': row['key_length'],
                'threshold': row['threshold'],
                'total_keys': row['total_keys'],
                'passed_keys': row['overall_passed'],
                'failed_keys': row['total_keys'] - row['overall_passed'],
                'pass_rate_percent': row['overall_pass_rate']
            }
            simple_final.append(simple_row)
        
        simple_final_df = pd.DataFrame(simple_final)
        simple_file = "output/reports/final_experiment_results.csv"
        simple_final_df.to_csv(simple_file, index=False)
        
        # Toplam süre
        total_time = time.time() - start_time
        
        print(f"✅ Raporlar kaydedildi:")
        print(f"   - Detaylı rapor: {detailed_file}")
        print(f"   - Basit rapor: {simple_file}")
        
        # Test bazlı özet istatistikler
        self.print_test_summary(df)
        
        print(f"\n⏱️  TOPLAM TEST SÜRESİ: {total_time/60:.1f} dakika")
        
        self.logger.info(f"Test aşaması tamamlandı! Toplam süre: {total_time/60:.1f} dakika")

    def print_test_summary(self, df):
        """Test bazlı özet istatistikleri yazdır"""
        print("\n📈 TEST BAZLI ÖZET İSTATİSTİKLER:")
        print("=" * 80)
        
        for threshold in [0.01, 0.05]:
            threshold_data = df[df['threshold'] == threshold]
            
            if threshold_data.empty:
                continue
                
            print(f"\n🎯 Eşik {threshold} Sonuçları:")
            print("-" * 60)
            
            # Genel başarı oranı
            avg_overall = threshold_data['overall_pass_rate'].mean()
            min_overall = threshold_data['overall_pass_rate'].min()
            max_overall = threshold_data['overall_pass_rate'].max()
            
            print(f"🏆 {'TÜM Testler (Genel)':25}: %{avg_overall:5.1f} (ort.) [%{min_overall:.1f}-%{max_overall:.1f}]")
            print("-" * 60)
            
            # Her test için ortalama başarı oranı
            for test_name in self.test_names:
                rate_col = f'{test_name}_pass_rate'
                if rate_col in threshold_data.columns:
                    avg_rate = threshold_data[rate_col].mean()
                    min_rate = threshold_data[rate_col].min()
                    max_rate = threshold_data[rate_col].max()
                    
                    status = "✅" if avg_rate >= 50 else "❌"
                    print(f"{status} {test_name:22}: %{avg_rate:5.1f} (ort.) [%{min_rate:.1f}-%{max_rate:.1f}]")
        
        # En başarılı ve başarısız kombinasyonlar
        self.print_best_worst_combinations(df)
    
    def print_best_worst_combinations(self, df):
        """En iyi ve en kötü kombinasyonları yazdır"""
        print(f"\n🏆 EN BAŞARILI KOMBİNASYONLAR:")
        print("-" * 60)
        
        for threshold in [0.01, 0.05]:
            threshold_data = df[df['threshold'] == threshold]
            if not threshold_data.empty:
                best = threshold_data.nlargest(3, 'overall_pass_rate')
                print(f"\nEşik {threshold}:")
                for _, row in best.iterrows():
                    print(f"  {row['source_type']:6}_{row['method_type']:10}_{row['key_length']:4}: %{row['overall_pass_rate']:5.1f}")
        
        print(f"\n💀 EN BAŞARISIZ KOMBİNASYONLAR:")
        print("-" * 60)
        
        for threshold in [0.01, 0.05]:
            threshold_data = df[df['threshold'] == threshold]
            if not threshold_data.empty:
                worst = threshold_data.nsmallest(3, 'overall_pass_rate')
                print(f"\nEşik {threshold}:")
                for _, row in worst.iterrows():
                    print(f"  {row['source_type']:6}_{row['method_type']:10}_{row['key_length']:4}: %{row['overall_pass_rate']:5.1f}")
                    
        print("\n🎯 ANALİZ TAMAMLANDI!")
        print("=" * 60)
        print("📁 Çıktı Dosyaları:")
        print(f"   - Detaylı rapor: output/reports/detailed_experiment_results.csv")
        print(f"   - Basit rapor: output/reports/final_experiment_results.csv")
        print(f"   - Bireysel detaylı CSVler: output/detailed_results/")
        print(f"   - Bireysel basit CSVler: output/test_results/")
        print(f"   - Log dosyası: logs/testing.log")

def main():
    """Ana fonksiyon"""
    try:
        pipeline = TestingPipeline()
        pipeline.test_all_keys()
        
    except Exception as e:
        print(f"❌ HATA: {e}")
        import traceback
        traceback.print_exc()
        
        # Log'a da yaz
        logger = Logger("testing.log")
        logger.error(f"Test aşaması hatası: {e}")
        
        input("Devam etmek için Enter tuşuna basın...")

if __name__ == "__main__":
    main()