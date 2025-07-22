#!/usr/bin/env python3
"""
Düzeltilmiş detaylı test analizi - Method hatası çözüldü
"""

import os
import time
from pathlib import Path
import pandas as pd

from src.testers import StatisticalTester
from src.config import ExperimentConfig
from src.utils import FileManager, Logger

class EnhancedStatisticalTester(StatisticalTester):
    """StatisticalTester'ı genişlet - check_individual_test ekle"""
    
    def check_individual_test(self, test_name: str, result: int, key_length: int, threshold: float) -> bool:
        """Tek bir testin eşik kontrolü"""
        if key_length not in self.thresholds or threshold not in self.thresholds[key_length]:
            return True  # Tanımlanmamış durumlar için geçti say
        
        thresholds = self.thresholds[key_length][threshold]
        
        if test_name in thresholds:
            min_val, max_val = thresholds[test_name]
            return min_val <= result <= max_val
        
        return True  # Test tanımlı değilse geçti say

def continue_tests_detailed():
    """Düzeltilmiş detaylı test analizi"""
    
    print("🔄 DETAYLI TEST ANALİZİ BAŞLIYOR...")
    print("=" * 50)
    
    config = ExperimentConfig()
    file_manager = FileManager()
    logger = Logger("detailed_tests.log")
    tester = EnhancedStatisticalTester()  # Enhanced versiyonu kullan
    
    # Test isimleri
    test_names = [
        'frequency', 'run_count', 'run_L1', 'template_4_1', 
        'template_4_2', 'template_4_3', 'template_4_4', 
        'linear_complexity', 'blind_spot_complexity'
    ]
    
    # Hangi key dosyaları var?
    key_files = list(Path("output/keys").glob("*.txt"))
    print(f"Bulunan anahtar dosyası: {len(key_files)}")
    
    total_files = len(key_files)
    current_file = 0
    
    # Detaylı sonuçları topla
    detailed_results = []
    
    for key_file in key_files:
        current_file += 1
        combo_name = key_file.stem.replace("_keys", "")
        
        print(f"🧪 [{current_file:2}/{total_files}] Analiz ediliyor: {combo_name}")
        
        # Anahtarları yükle
        keys = file_manager.load_keys(str(key_file))
        key_length = int(combo_name.split("_")[-1])
        
        if not keys:
            print(f"   ⚠️  Anahtar dosyası boş: {key_file}")
            continue
            
        start_time = time.time()
        
        # Her iki eşik değeri için analiz et
        for threshold in [0.01, 0.05]:
            print(f"   🔍 Eşik {threshold} analiz ediliyor...")
            
            # Her test için başarı sayacı
            test_pass_counts = {test_name: 0 for test_name in test_names}
            overall_pass_count = 0
            total_keys = len(keys)
            
            all_test_results = []
            
            for i, key in enumerate(keys):
                try:
                    # Tüm testleri uygula
                    results = tester.run_all_tests(key, key_length)
                    
                    # Her testin bireysel başarısını kontrol et
                    individual_passes = {}
                    all_tests_passed = True
                    
                    for test_name in test_names:
                        if test_name in results:
                            individual_passed = tester.check_individual_test(
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
                        print(f"      {i + 1}/{total_keys} analiz tamamlandı...")
                        
                except Exception as e:
                    print(f"      ⚠️  Key {i+1} analiz hatası: {str(e)[:50]}...")
                    
                    # Hatalı key için varsayılan sonuç ekle
                    result_row = {
                        'key_id': i + 1,
                        'key_bits': ''.join(['1' if b else '0' for b in key]),
                        'overall_passed': False
                    }
                    
                    # Her test için False ekle
                    for test_name in test_names:
                        result_row[f'{test_name}_passed'] = False
                        result_row[test_name] = -1  # Error değeri
                    
                    all_test_results.append(result_row)
            
            # Sonuçları kaydet
            threshold_str = str(threshold).replace(".", "")
            
            # CSV dosyası
            csv_file = f"output/detailed_results/{combo_name}_threshold_{threshold_str}_detailed.csv"
            Path("output/detailed_results").mkdir(exist_ok=True)
            
            df = pd.DataFrame(all_test_results)
            df.to_csv(csv_file, index=False)
            
            # Özet istatistikleri
            test_time = time.time() - start_time
            overall_pass_rate = (overall_pass_count / total_keys) * 100
            
            print(f"   📊 Eşik {threshold} Sonuçları:")
            print(f"      🎯 TÜM testleri geçen: {overall_pass_count}/{total_keys} (%{overall_pass_rate:.1f})")
            
            # Her testin bireysel başarı oranı
            for test_name in test_names:
                individual_rate = (test_pass_counts[test_name] / total_keys) * 100
                status = "✅" if individual_rate >= 50 else "❌"
                print(f"      {status} {test_name:20}: {test_pass_counts[test_name]:4}/{total_keys} (%{individual_rate:5.1f})")
            
            print(f"      💾 Detaylı sonuçlar: {csv_file}")
            
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
            for test_name in test_names:
                result_summary[f'{test_name}_passed'] = test_pass_counts[test_name]
                result_summary[f'{test_name}_pass_rate'] = (test_pass_counts[test_name] / total_keys) * 100
            
            detailed_results.append(result_summary)
            
            logger.info(f"{combo_name} threshold {threshold}: Overall {overall_pass_count}/{total_keys} ({overall_pass_rate:.1f}%)")
            print()  # Boş satır

    print("\n🎉 DETAYLI ANALİZ TAMAMLANDI!")
    
    # Final detaylı raporu oluştur
    generate_detailed_final_report(detailed_results)

def generate_detailed_final_report(detailed_results):
    """Detaylı final raporu oluştur"""
    print("\n📊 Detaylı final raporu oluşturuluyor...")
    
    if not detailed_results:
        print("❌ Hiç sonuç bulunamadı!")
        return
    
    # DataFrame'e dönüştür
    df = pd.DataFrame(detailed_results)
    df = df.sort_values(['source_type', 'method_type', 'key_length', 'threshold'])
    
    # Final detaylı CSV
    detailed_file = "output/reports/detailed_experiment_results.csv"
    Path("output/reports").mkdir(exist_ok=True)
    df.to_csv(detailed_file, index=False)
    
    print(f"✅ Detaylı final rapor kaydedildi: {detailed_file}")
    
    # Test bazlı özet rapor
    test_names = [
        'frequency', 'run_count', 'run_L1', 'template_4_1', 
        'template_4_2', 'template_4_3', 'template_4_4', 
        'linear_complexity', 'blind_spot_complexity'
    ]
    
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
        for test_name in test_names:
            rate_col = f'{test_name}_pass_rate'
            if rate_col in threshold_data.columns:
                avg_rate = threshold_data[rate_col].mean()
                min_rate = threshold_data[rate_col].min()
                max_rate = threshold_data[rate_col].max()
                
                status = "✅" if avg_rate >= 50 else "❌"
                print(f"{status} {test_name:22}: %{avg_rate:5.1f} (ort.) [%{min_rate:.1f}-%{max_rate:.1f}]")
    
    # En başarılı ve başarısız kombinasyonlar
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
    print(f"   - Bireysel CSVler: output/detailed_results/")
    print(f"   - Log dosyası: logs/detailed_tests.log")

if __name__ == "__main__":
    continue_tests_detailed()