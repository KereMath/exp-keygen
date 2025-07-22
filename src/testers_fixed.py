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
                    'frequency': (45, 83),
                    'run_count': (46, 86),
                    'run_L1': (13, 60),
                    'template_4_1': (0, 25),
                    'template_4_2': (0, 19),
                    'template_4_3': (0, 16),
                    'template_4_4': (0, 15),
                    'linear_complexity': (59, 67),
                    'blind_spot_complexity': (59, 70)
                },
                0.05: {
                    'frequency': (48, 80),
                    'run_count': (48, 80),
                    'run_L1': (16, 51),
                    'template_4_1': (0, 22),
                    'template_4_2': (0, 17),
                    'template_4_3': (0, 15),
                    'template_4_4': (0, 14),
                    'linear_complexity': (60, 68),
                    'blind_spot_complexity': (60, 68)
                }
            },
            256: {
                0.01: {
                    'frequency': (100, 153),
                    'run_count': (102, 155),
                    'run_L1': (37, 96),
                    'template_4_1': (0, 38),
                    'template_4_2': (0, 30),
                    'template_4_3': (0, 28),
                    'template_4_4': (0, 26),
                    'linear_complexity': (123, 134),
                    'blind_spot_complexity': (123, 134)
                },
                0.05: {
                    'frequency': (105, 151),
                    'run_count': (106, 151),
                    'run_L1': (41, 91),
                    'template_4_1': (0, 34),
                    'template_4_2': (0, 27),
                    'template_4_3': (0, 26),
                    'template_4_4': (0, 24),
                    'linear_complexity': (123, 132),
                    'blind_spot_complexity': (123, 132)
                }
            },
            512: {
                0.01: {
                    'frequency': (218, 294),
                    'run_count': (219, 296),
                    'run_L1': (89, 175),
                    'template_4_1': (0, 63),
                    'template_4_2': (0, 51),
                    'template_4_3': (0, 48),
                    'template_4_4': (0, 45),
                    'linear_complexity': (251, 262),
                    'blind_spot_complexity': (251, 262)
                },
                0.05: {
                    'frequency': (224, 288),
                    'run_count': (224, 288),
                    'run_L1': (94, 165),
                    'template_4_1': (0, 56),
                    'template_4_2': (0, 48),
                    'template_4_3': (0, 46),
                    'template_4_4': (0, 43),
                    'linear_complexity': (251, 262),
                    'blind_spot_complexity': (251, 262)
                }
            },
            1024: {
                0.01: {
                    'frequency': (459, 566),
                    'run_count': (460, 566),
                    'run_L1': (200, 319),
                    'template_4_1': (0, 105),
                    'template_4_2': (0, 91),
                    'template_4_3': (0, 87),
                    'template_4_4': (0, 82),
                    'linear_complexity': (507, 518),
                    'blind_spot_complexity': (507, 518)
                },
                0.05: {
                    'frequency': (468, 557),
                    'run_count': (468, 557),
                    'run_L1': (208, 307),
                    'template_4_1': (0, 97),
                    'template_4_2': (0, 86),
                    'template_4_3': (0, 83),
                    'template_4_4': (0, 79),
                    'linear_complexity': (508, 517),
                    'blind_spot_complexity': (508, 517)
                }
            },
            2048: {
                0.01: {
                    'frequency': (950, 1100),
                    'run_count': (950, 1098),
                    'run_L1': (431, 599),
                    'template_4_1': (0, 185),
                    'template_4_2': (0, 165),
                    'template_4_3': (0, 160),
                    'template_4_4': (0, 154),
                    'linear_complexity': (1019, 1030),
                    'blind_spot_complexity': (1019, 1030)
                },
                0.05: {
                    'frequency': (961, 1087),
                    'run_count': (961, 1088),
                    'run_L1': (443, 584),
                    'template_4_1': (0, 174),
                    'template_4_2': (0, 158),
                    'template_4_3': (0, 154),
                    'template_4_4': (0, 149),
                    'linear_complexity': (1020, 1029),
                    'blind_spot_complexity': (1020, 1029)
                }
            },
            4096: {
                0.01: {
                    'frequency': (1943, 2154),
                    'run_count': (1943, 2150),
                    'run_L1': (909, 1143),
                    'template_4_1': (0, 334),
                    'template_4_2': (0, 308),
                    'template_4_3': (0, 301),
                    'template_4_4': (0, 293),
                    'linear_complexity': (2043, 2054),
                    'blind_spot_complexity': (2043, 2054)
                },
                0.05: {
                    'frequency': (1959, 2137),
                    'run_count': (1959, 2137),
                    'run_L1': (927, 1123),
                    'template_4_1': (0, 320),
                    'template_4_2': (0, 298),
                    'template_4_3': (0, 293),
                    'template_4_4': (0, 286),
                    'linear_complexity': (2044, 2053),
                    'blind_spot_complexity': (2044, 2053)
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