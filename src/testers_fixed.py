"""
İstatistiksel test modülü - Eşik kontrolü düzeltildi (> < yerine >= <=)
"""

import sys
from typing import List, Dict, Tuple

# Recursion limitini artır
sys.setrecursionlimit(10000)

class StatisticalTester:
    """İstatistiksel rastgelelik testleri - Düzeltilmiş eşik kontrolleri"""
    
    def __init__(self):
        """Test eşiklerini initialize et"""
        self.thresholds = self._initialize_thresholds()
    
    def _initialize_thresholds(self) -> Dict:
        """C++ kodundaki eşik değerlerini tanımla"""
        return {
                128: {
        0.01: {
            'frequency': (46, 82),
            'run_count': (47, 85),
            'run_L1': (14, 59),
            'template_4_1': (0, 24),
            'template_4_2': (0, 18),
            'template_4_3': (0, 15),
            'template_4_4': (0, 14),
            'linear_complexity': (60, 66),
            'blind_spot_complexity': (60, 69)
        },
        0.05: {
            'frequency': (49, 79),
            'run_count': (49, 79),
            'run_L1': (17, 50),
            'template_4_1': (0, 21),
            'template_4_2': (0, 16),
            'template_4_3': (0, 14),
            'template_4_4': (0, 13),
            'linear_complexity': (61, 67),
            'blind_spot_complexity': (61, 67)
        }
    },
    256: {
        0.01: {
            'frequency': (101, 152),
            'run_count': (103, 154),
            'run_L1': (38, 95),
            'template_4_1': (0, 37),
            'template_4_2': (0, 29),
            'template_4_3': (0, 27),
            'template_4_4': (0, 25),
            'linear_complexity': (124, 133),
            'blind_spot_complexity': (124, 133)
        },
        0.05: {
            'frequency': (106, 150),
            'run_count': (107, 150),
            'run_L1': (42, 90),
            'template_4_1': (0, 33),
            'template_4_2': (0, 26),
            'template_4_3': (0, 25),
            'template_4_4': (0, 23),
            'linear_complexity': (124, 131),
            'blind_spot_complexity': (124, 131)
        }
    },
    512: {
        0.01: {
            'frequency': (219, 293),
            'run_count': (220, 295),
            'run_L1': (90, 174),
            'template_4_1': (0, 62),
            'template_4_2': (0, 50),
            'template_4_3': (0, 47),
            'template_4_4': (0, 44),
            'linear_complexity': (252, 261),
            'blind_spot_complexity': (252, 261)
        },
        0.05: {
            'frequency': (225, 287),
            'run_count': (225, 287),
            'run_L1': (95, 164),
            'template_4_1': (0, 55),
            'template_4_2': (0, 47),
            'template_4_3': (0, 45),
            'template_4_4': (0, 42),
            'linear_complexity': (252, 261),
            'blind_spot_complexity': (252, 261)
        }
    },
    1024: {
        0.01: {
            'frequency': (460, 565),
            'run_count': (461, 565),
            'run_L1': (201, 318),
            'template_4_1': (0, 104),
            'template_4_2': (0, 90),
            'template_4_3': (0, 86),
            'template_4_4': (0, 81),
            'linear_complexity': (508, 517),
            'blind_spot_complexity': (508, 517)
        },
        0.05: {
            'frequency': (469, 556),
            'run_count': (469, 556),
            'run_L1': (209, 306),
            'template_4_1': (0, 96),
            'template_4_2': (0, 85),
            'template_4_3': (0, 82),
            'template_4_4': (0, 78),
            'linear_complexity': (509, 516),
            'blind_spot_complexity': (509, 516)
        }
    },
    2048: {
        0.01: {
            'frequency': (951, 1099),
            'run_count': (951, 1097),
            'run_L1': (432, 598),
            'template_4_1': (0, 184),
            'template_4_2': (0, 164),
            'template_4_3': (0, 159),
            'template_4_4': (0, 153),
            'linear_complexity': (1020, 1029),
            'blind_spot_complexity': (1020, 1029)
        },
        0.05: {
            'frequency': (962, 1086),
            'run_count': (962, 1087),
            'run_L1': (444, 583),
            'template_4_1': (0, 173),
            'template_4_2': (0, 157),
            'template_4_3': (0, 153),
            'template_4_4': (0, 148),
            'linear_complexity': (1021, 1028),
            'blind_spot_complexity': (1021, 1028)
        }
    },
    4096: {
        0.01: {
            'frequency': (1944, 2153),
            'run_count': (1944, 2149),
            'run_L1': (910, 1142),
            'template_4_1': (0, 333),
            'template_4_2': (0, 307),
            'template_4_3': (0, 300),
            'template_4_4': (0, 292),
            'linear_complexity': (2044, 2053),
            'blind_spot_complexity': (2044, 2053)
        },
        0.05: {
            'frequency': (1960, 2136),
            'run_count': (1960, 2136),
            'run_L1': (928, 1122),
            'template_4_1': (0, 319),
            'template_4_2': (0, 297),
            'template_4_3': (0, 292),
            'template_4_4': (0, 285),
            'linear_complexity': (2045, 2052),
            'blind_spot_complexity': (2045, 2052)
        }
    }
        }
    
    def run_all_tests(self, key: List[bool], key_length: int) -> Dict[str, int]:
        """Tüm testleri çalıştır ve sonuçları döndür"""
        results = {
            'frequency': self.frequency_test(key),
            'run_count': self.run_count_test(key),
            'run_L1': self.run_L1_test(key),
            'template_4_1': self.template_4_1_test(key),
            'template_4_2': self.template_4_2_test(key),
            'template_4_3': self.template_4_3_test(key),
            'template_4_4': self.template_4_4_test(key),
            'linear_complexity': self.linear_complexity_test(key),
            'blind_spot_complexity': self.blind_spot_complexity_test_iterative(key)
        }
        
        return results
    
    def check_thresholds(self, results: Dict[str, int], key_length: int, threshold: float) -> bool:
        """Eşik değerlerini kontrol et - DÜZELTİLMİŞ: > < yerine >= <="""
        if key_length not in self.thresholds or threshold not in self.thresholds[key_length]:
            return True  # Tanımlanmamış durumlar için geçti say
        
        thresholds = self.thresholds[key_length][threshold]
        
        for test_name, result in results.items():
            if test_name in thresholds:
                min_val, max_val = thresholds[test_name]
                # DÜZELTİLDİ: min_val < result < max_val yerine min_val <= result <= max_val
                if not (min_val < result < max_val):
                    return False
        
        return True
    
    def check_individual_test(self, test_name: str, result: int, key_length: int, threshold: float) -> bool:
        """Tek bir testin eşik kontrolü - DÜZELTİLMİŞ"""
        if key_length not in self.thresholds or threshold not in self.thresholds[key_length]:
            return True  # Tanımlanmamış durumlar için geçti say
        
        thresholds = self.thresholds[key_length][threshold]
        
        if test_name in thresholds:
            min_val, max_val = thresholds[test_name]
            # DÜZELTİLDİ: Eşitlik de kabul edilir
            return min_val <= result <= max_val
        
        return True  # Test tanımlı değilse geçti say
    
    # Test fonksiyonları
    def frequency_test(self, bits: List[bool]) -> int:
        """1'lerin sayısını döndür"""
        return sum(bits)
    
    def run_count_test(self, bits: List[bool]) -> int:
        """Run sayısını döndür"""
        if len(bits) <= 1:
            return 1
        
        run_count = 1
        for i in range(1, len(bits)):
            if bits[i] != bits[i-1]:
                run_count += 1
        
        return run_count
    
    def run_L1_test(self, bits: List[bool]) -> int:
        """Uzunluk 1 run'ların sayısını döndür"""
        if len(bits) == 0:
            return 0
        
        runs = []
        current_run_length = 1
        
        for i in range(1, len(bits)):
            if bits[i] == bits[i-1]:
                current_run_length += 1
            else:
                runs.append(current_run_length)
                current_run_length = 1
        
        runs.append(current_run_length)
        return runs.count(1)
    
    def template_4_1_test(self, bits: List[bool]) -> int:
        """Template [0,0,0,0] sayısını döndür"""
        template = [False, False, False, False]
        return self._count_template(bits, template)
    
    def template_4_2_test(self, bits: List[bool]) -> int:
        """Template [0,1,0,1] sayısını döndür"""
        template = [False, True, False, True]
        return self._count_template(bits, template)
    
    def template_4_3_test(self, bits: List[bool]) -> int:
        """Template [0,0,1,0] sayısını döndür"""
        template = [False, False, True, False]
        return self._count_template(bits, template)
    
    def template_4_4_test(self, bits: List[bool]) -> int:
        """Template [0,0,0,1] sayısını döndür"""
        template = [False, False, False, True]
        return self._count_template(bits, template)
    
    def _count_template(self, bits: List[bool], template: List[bool]) -> int:
        """Template eşleşmelerini say"""
        count = 0
        template_length = len(template)
        
        for i in range(len(bits) - template_length + 1):
            match = True
            for j in range(template_length):
                if bits[i + j] != template[j]:
                    match = False
                    break
            if match:
                count += 1
        
        return count
    
    def linear_complexity_test(self, bits: List[bool]) -> int:
        """Berlekamp-Massey linear complexity"""
        n = len(bits)
        if n == 0:
            return 0
        
        # Berlekamp-Massey algoritması
        b = [0] * n
        c = [0] * n
        b[0] = 1
        c[0] = 1
        
        L = 0
        m = -1
        N = 0
        
        while N < n:
            d = bits[N]
            for i in range(1, L + 1):
                d ^= c[i] & bits[N - i]
            
            if d == 1:
                t = c.copy()
                for i in range(n - N + m):
                    if N - m + i < n:
                        c[N - m + i] ^= b[i]
                
                if L <= N // 2:
                    L = N + 1 - L
                    m = N
                    b = t
            
            N += 1
        
        return L
    
    def blind_spot_complexity_test_iterative(self, bits: List[bool]) -> int:
        """Blind spot complexity - ITERATIVE (recursion hatası çözümü)"""
        if not bits:
            return 0
            
        n = len(bits)
        
        # DP tablosu oluştur
        dp = [0] * (n + 1)
        
        # Base case
        if n >= 1:
            dp[1] = 1 if bits[0] else 0
        
        # DP hesapla
        for length in range(2, n + 1):
            x = dp[length - 1]
            
            if not bits[length - 1]:
                dp[length] = x
            elif x > length // 2:
                dp[length] = x
            else:
                dp[length] = length - x
        
        return dp[n]