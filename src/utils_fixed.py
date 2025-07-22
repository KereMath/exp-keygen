"""
Yardımcı fonksiyonlar - Log dizinleri düzeltildi
"""

import os
import logging
from datetime import datetime
from typing import List
from pathlib import Path

class FileManager:
    """Dosya yönetim sınıfı"""
    
    @staticmethod
    def save_keys(keys: List[List[bool]], filepath: str):
        """Anahtarları dosyaya kaydet"""
        Path(filepath).parent.mkdir(parents=True, exist_ok=True)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            for key in keys:
                key_str = ''.join('1' if bit else '0' for bit in key)
                f.write(key_str + '\n')
    
    @staticmethod
    def load_keys(filepath: str) -> List[List[bool]]:
        """Dosyadan anahtarları yükle"""
        keys = []
        
        if not os.path.exists(filepath):
            return keys
        
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    key = [bit == '1' for bit in line]
                    keys.append(key)
        
        return keys
    
    @staticmethod
    def ensure_directory(dir_path: str):
        """Klasör var olduğundan emin ol"""
        Path(dir_path).mkdir(parents=True, exist_ok=True)

class Logger:
    """Logging sınıfı - Log dizinleri düzeltildi"""
    
    def __init__(self, log_file: str = "experiment.log"):
        """Logger'ı initialize et - LOGS FOLDER İÇİNE YAZ"""
        # Log dosyası adını düzelt - logs/ klasörüne yaz
        if not log_file.startswith("logs/"):
            log_file = f"logs/{log_file}"
        
        # Log klasörünü oluştur
        Path(log_file).parent.mkdir(parents=True, exist_ok=True)
        
        # Mevcut logger'ları temizle
        for handler in logging.root.handlers[:]:
            logging.root.removeHandler(handler)
        
        # Logger'ı ayarla
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file, encoding='utf-8'),
                logging.StreamHandler()  # Console'a da yazdır
            ],
            force=True  # Mevcut konfigürasyonu zorla değiştir
        )
        
        self.logger = logging.getLogger(__name__)
        
        # İlk log mesajı
        self.info("=" * 50)
        self.info("ANAHTAR ÜRETİCİ DENEYİ BAŞLADI")
        self.info(f"Tarih: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        self.info(f"Log dosyası: {log_file}")
        self.info("=" * 50)
    
    def info(self, message: str):
        """Info log"""
        self.logger.info(message)
    
    def error(self, message: str):
        """Error log"""
        self.logger.error(message)
    
    def warning(self, message: str):
        """Warning log"""
        self.logger.warning(message)
    
    def debug(self, message: str):
        """Debug log"""
        self.logger.debug(message)

class ProgressTracker:
    """İlerleme takip sınıfı"""
    
    def __init__(self, total: int, description: str = "Progress"):
        self.total = total
        self.current = 0
        self.description = description
        self.start_time = datetime.now()
    
    def update(self, increment: int = 1):
        """İlerlemeyi güncelle"""
        self.current += increment
        percentage = (self.current / self.total) * 100
        
        # Kalan süreyi hesapla
        elapsed = datetime.now() - self.start_time
        if self.current > 0:
            total_estimated = elapsed * (self.total / self.current)
            remaining = total_estimated - elapsed
            remaining_str = str(remaining).split('.')[0]  # Saniye hassasiyetinde
        else:
            remaining_str = "Bilinmiyor"
        
        print(f"\r{self.description}: {self.current}/{self.total} (%{percentage:.1f}) - Kalan: {remaining_str}   ", end='', flush=True)
        
        if self.current >= self.total:
            print()  # Yeni satıra geç

class Statistics:
    """İstatistik hesaplama sınıfı"""
    
    @staticmethod
    def calculate_pass_rate(passed: int, total: int) -> float:
        """Geçme oranını hesapla"""
        if total == 0:
            return 0.0
        return (passed / total) * 100
    
    @staticmethod
    def format_time(seconds: float) -> str:
        """Saniyeyi okunabilir formata dönüştür"""
        if seconds < 60:
            return f"{seconds:.1f} saniye"
        elif seconds < 3600:
            minutes = seconds / 60
            return f"{minutes:.1f} dakika"
        else:
            hours = seconds / 3600
            return f"{hours:.1f} saat"
    
    @staticmethod
    def format_number(number: int) -> str:
        """Sayıyı okunabilir formata dönüştür"""
        if number < 1000:
            return str(number)
        elif number < 1000000:
            return f"{number/1000:.1f}K"
        else:
            return f"{number/1000000:.1f}M"

class Validator:
    """Doğrulama sınıfı"""
    
    @staticmethod
    def validate_key(key: List[bool]) -> bool:
        """Anahtar geçerli mi kontrol et"""
        if not isinstance(key, list):
            return False
        
        if len(key) == 0:
            return False
        
        if not all(isinstance(bit, bool) for bit in key):
            return False
        
        return True
    
    @staticmethod
    def validate_key_length(length: int) -> bool:
        """Anahtar uzunluğu geçerli mi"""
        valid_lengths = [128, 256, 512, 1024, 2048, 4096]
        return length in valid_lengths
    
    @staticmethod
    def validate_threshold(threshold: float) -> bool:
        """Eşik değeri geçerli mi"""
        valid_thresholds = [0.01, 0.05]
        return threshold in valid_thresholds
    
    @staticmethod
    def validate_source_type(source_type: str) -> bool:
        """Kaynak türü geçerli mi"""
        valid_sources = ['sha256', 'random']
        return source_type in valid_sources
    
    @staticmethod
    def validate_method_type(method_type: str) -> bool:
        """Yöntem türü geçerli mi"""
        valid_methods = ['shrinking', 'alternating', 'aes']
        return method_type in valid_methods

class ReportGenerator:
    """Rapor oluşturma sınıfı"""
    
    @staticmethod
    def create_summary_report(results_data: List[dict]) -> str:
        """Özet rapor oluştur"""
        report = []
        report.append("ANAHTAR ÜRETİCİ DENEY RAPORU")
        report.append("=" * 50)
        report.append(f"Oluşturulma Tarihi: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("")
        
        # Genel istatistikler
        total_combinations = len(set((r['source_type'], r['method_type'], r['key_length']) for r in results_data))
        total_keys = sum(r['total_keys'] for r in results_data) // 2  # Her kombo 2 kez (0.01 ve 0.05)
        
        report.append(f"Toplam Kombinasyon: {total_combinations}")
        report.append(f"Toplam Anahtar: {total_keys:,}")
        report.append("")
        
        # Eşik bazında özetler
        for threshold in [0.01, 0.05]:
            threshold_data = [r for r in results_data if r['threshold'] == threshold]
            if threshold_data:
                avg_pass_rate = sum(r['pass_rate_percent'] for r in threshold_data) / len(threshold_data)
                min_pass_rate = min(r['pass_rate_percent'] for r in threshold_data)
                max_pass_rate = max(r['pass_rate_percent'] for r in threshold_data)
                
                report.append(f"Eşik {threshold} Sonuçları:")
                report.append(f"  Ortalama Geçme Oranı: %{avg_pass_rate:.1f}")
                report.append(f"  En Düşük Geçme Oranı: %{min_pass_rate:.1f}")
                report.append(f"  En Yüksek Geçme Oranı: %{max_pass_rate:.1f}")
                report.append("")
        
        return "\n".join(report)
    
    @staticmethod
    def save_summary_report(results_data: List[dict], filepath: str):
        """Özet raporunu dosyaya kaydet"""
        report_text = ReportGenerator.create_summary_report(results_data)
        
        Path(filepath).parent.mkdir(parents=True, exist_ok=True)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(report_text)