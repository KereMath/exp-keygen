"""
Deney konfigürasyon dosyası
"""

class ExperimentConfig:
    """Deney parametrelerini yönetir"""
    
    # Kaynak türleri
    SOURCE_TYPES = ['sha256', 'random']
    
    # Üretim yöntemleri
    METHOD_TYPES = ['shrinking', 'alternating', 'aes']
    
    # Anahtar uzunlukları
    KEY_LENGTHS = [128, 256, 512, 1024, 2048, 4096]
    
    # Test eşikleri
    THRESHOLDS = [0.01, 0.05]
    
    # Her kombinasyondan kaç anahtar
    KEYS_PER_COMBINATION = 1000
    
    # Varsayılan tohum (SHA256 için)
    DEFAULT_SEED = "experiment_seed_2024"
    
    def get_all_combinations(self):
        """36 kombinasyonun hepsini döndür"""
        combinations = []
        
        for source in self.SOURCE_TYPES:
            for method in self.METHOD_TYPES:
                for length in self.KEY_LENGTHS:
                    combinations.append((source, method, length))
                    
        return combinations
    
    def get_combination_name(self, source, method, length):
        """Kombinasyon adını oluştur"""
        return f"{source}_{method}_{length}"
    
    def get_total_combinations(self):
        """Toplam kombinasyon sayısı"""
        return len(self.SOURCE_TYPES) * len(self.METHOD_TYPES) * len(self.KEY_LENGTHS)
    
    def get_total_keys(self):
        """Toplam üretilecek anahtar sayısı"""
        return self.get_total_combinations() * self.KEYS_PER_COMBINATION
    
    def validate_combination(self, source, method, length):
        """Kombinasyonun geçerli olup olmadığını kontrol et"""
        return (source in self.SOURCE_TYPES and 
                method in self.METHOD_TYPES and 
                length in self.KEY_LENGTHS)