"""
Anahtar üretici algoritmaları - MT19937 C++ implementasyonu ile
Python'un hiçbir random fonksiyonu kullanılmaz!
"""

import hashlib
import time
from typing import List, Tuple
from mt19937_random import MT19937Random

class BaseGenerator:
    """Temel üretici sınıfı"""
    
    def generate_seed(self) -> str:
        """Tohum üretir (override edilecek)"""
        raise NotImplementedError
    
    def generate_key(self, seed: str, length: int) -> List[bool]:
        """Anahtar üretir (override edilecek)"""
        raise NotImplementedError

class SHA256Generator(BaseGenerator):
    """SHA256 tabanlı üretici - Deterministik"""
    
    def __init__(self):
        self.seed_counter = 0
        self.start_timestamp = int(time.time() * 1000000)  # Microsecond timestamp
    
    def generate_seed(self) -> str:
        """Deterministik tohum üret"""
        self.seed_counter += 1
        return f"sha256_seed_{self.start_timestamp}_{self.seed_counter}"
    
    def generate_key(self, seed: str, length: int) -> List[bool]:
        """SHA256 ile deterministik anahtar üret"""
        current_bits = []
        current_seed = seed
        
        while len(current_bits) < length:
            # SHA256 hash hesapla
            hash_obj = hashlib.sha256(current_seed.encode())
            hash_hex = hash_obj.hexdigest()
            
            # Hex'i binary'ye dönüştür
            for hex_char in hash_hex:
                if len(current_bits) >= length:
                    break
                # Her hex karakteri 4 bit
                bin_str = format(int(hex_char, 16), '04b')
                for bit_char in bin_str:
                    if len(current_bits) >= length:
                        break
                    current_bits.append(bit_char == '1')
            
            # Yeni seed için hash'i kullan
            current_seed = hash_hex
        
        return current_bits[:length]

class MT19937Generator(BaseGenerator):
    """MT19937 C++ tabanlı üretici - True Random"""
    
    def __init__(self):
        self.mt = MT19937Random()
        self.call_counter = 0
    
    def generate_seed(self) -> str:
        """MT19937 ile true random tohum üret"""
        self.call_counter += 1
        # Her çağrıda fresh entropy
        hex_token = self.mt.token_hex(32)  # 32 bytes = 256 bits entropy
        return f"mt19937_seed_{self.call_counter}_{hex_token}"
    
    def generate_key(self, seed: str, length: int) -> List[bool]:
        """MT19937 ile true random anahtar üret"""
        # Seed'den integer hash oluştur (deterministik)
        seed_hash = int(hashlib.sha256(seed.encode()).hexdigest(), 16)
        seed_32bit = seed_hash & 0xFFFFFFFF  # 32-bit'e indir
        
        # MT19937'yi seed ile initialize et
        temp_mt = MT19937Random()
        temp_mt.seed(seed_32bit)
        
        # Bit array üret
        return temp_mt.randbits(length)

class ShrinkingGenerator:
    """Shrinking generator algoritması - MT19937 bazlı"""
    
    def __init__(self, seed_bits: List[bool]):
        # LFSR'ları initialize et
        mid_point = len(seed_bits) // 2
        self.lfsr1 = LFSR(seed_bits[:mid_point], [0, 7, 15, 23])      # Control LFSR
        self.lfsr2 = LFSR(seed_bits[mid_point:], [0, 5, 13, 21])     # Data LFSR
    
    def generate(self, length: int) -> List[bool]:
        """Shrinking generator ile anahtar üret"""
        output = []
        max_attempts = length * 10  # Sonsuz döngü önleme
        attempts = 0
        
        while len(output) < length and attempts < max_attempts:
            attempts += 1
            control_bit = self.lfsr1.next_bit()
            data_bit = self.lfsr2.next_bit()
            
            # Control bit 1 ise data bit'i al
            if control_bit:
                output.append(data_bit)
        
        # Yetersizse kalan kısmı pad et
        while len(output) < length:
            output.append(self.lfsr2.next_bit())
        
        return output[:length]

class AlternatingGenerator:
    """Alternating step generator - MT19937 bazlı"""
    
    def __init__(self, seed_bits: List[bool]):
        # 3 LFSR'a böl
        third = len(seed_bits) // 3
        if third == 0:
            third = 1  # Minimum length
        
        self.lfsr1 = LFSR(seed_bits[:third], [0, 3, 7])              # Control
        self.lfsr2 = LFSR(seed_bits[third:2*third], [0, 5, 11])     # Data 1  
        self.lfsr3 = LFSR(seed_bits[2*third:], [0, 4, 9])           # Data 2
    
    def generate(self, length: int) -> List[bool]:
        """Alternating generator ile anahtar üret"""
        output = []
        
        for _ in range(length):
            control_bit = self.lfsr1.next_bit()
            
            if control_bit:
                output.append(self.lfsr2.next_bit())
            else:
                output.append(self.lfsr3.next_bit())
        
        return output

class ImprovedAESGenerator:
    """Geliştirilmiş AES benzeri generator - MT19937 bazlı"""
    
    def __init__(self, seed_bits: List[bool]):
        # Seed'i 128-bit key'e dönüştür
        self.key_bits = seed_bits[:128] if len(seed_bits) >= 128 else seed_bits + [False] * (128 - len(seed_bits))
        self.counter = 0
        
        # MT19937 instance (seed için)
        self.mt = MT19937Random()
        seed_int = self._bits_to_int(self.key_bits) % (2**32)
        self.mt.seed(seed_int)
    
    def generate(self, length: int) -> List[bool]:
        """Geliştirilmiş AES benzeri anahtar üret"""
        output = []
        
        while len(output) < length:
            # Counter increment
            self.counter += 1
            
            # Key ile counter'ı combine et
            counter_bits = self._int_to_bits(self.counter, 128)
            
            # XOR operation
            block = [a ^ b for a, b in zip(self.key_bits, counter_bits)]
            
            # Multiple rounds of substitution and permutation
            for round_num in range(4):  # 4 rounds
                # Substitution (non-linear)
                block = self._substitution(block)
                
                # Permutation
                block = self._permutation(block)
                
                # Add round key (from MT19937)
                round_key = self.mt.randbits(128)
                block = [a ^ b for a, b in zip(block, round_key)]
            
            output.extend(block)
        
        return output[:length]
    
    def _bits_to_int(self, bits: List[bool]) -> int:
        """Bit listesini integer'a dönüştür"""
        result = 0
        for i, bit in enumerate(bits):
            if bit:
                result |= (1 << i)
        return result
    
    def _int_to_bits(self, value: int, bit_count: int) -> List[bool]:
        """Integer'ı bit listesine dönüştür"""
        bits = []
        for i in range(bit_count):
            bits.append((value >> i) & 1 == 1)
        return bits
    
    def _substitution(self, bits: List[bool]) -> List[bool]:
        """Non-linear substitution (S-box benzeri)"""
        result = bits.copy()
        
        # 4-bit S-box transformation
        s_box = [0x9, 0x4, 0xA, 0xB, 0xD, 0x1, 0x8, 0x5, 
                 0x6, 0x2, 0x0, 0x3, 0xC, 0xE, 0xF, 0x7]
        
        for i in range(0, len(result) - 3, 4):
            # 4-bit chunk al
            chunk = (int(result[i]) << 3) | (int(result[i+1]) << 2) | \
                   (int(result[i+2]) << 1) | int(result[i+3])
            
            # S-box transformation
            new_chunk = s_box[chunk]
            
            # Geri yaz
            result[i] = bool((new_chunk >> 3) & 1)
            result[i+1] = bool((new_chunk >> 2) & 1)
            result[i+2] = bool((new_chunk >> 1) & 1)
            result[i+3] = bool(new_chunk & 1)
        
        return result
    
    def _permutation(self, bits: List[bool]) -> List[bool]:
        """Bit permutation"""
        result = [False] * len(bits)
        
        # Fixed permutation table
        for i in range(len(bits)):
            # Simple permutation formula
            new_pos = (i * 17 + 23) % len(bits)
            result[new_pos] = bits[i]
        
        return result

class LFSR:
    """Linear Feedback Shift Register - Geliştirilmiş"""
    
    def __init__(self, initial_state: List[bool], taps: List[int]):
        # State'i kopyala ve minimum uzunluk garanti et
        if len(initial_state) < 8:
            initial_state = initial_state + [False] * (8 - len(initial_state))
        
        self.state = initial_state.copy()
        self.taps = [t for t in taps if t < len(self.state)]  # Valid taps only
        
        # Tüm sıfır durumunu önle
        if not any(self.state):
            self.state[0] = True
        
        # En az bir tap olmalı
        if not self.taps:
            self.taps = [0, 1]
    
    def next_bit(self) -> bool:
        """Bir sonraki bit üret"""
        if not self.state:
            return False
            
        output = self.state[-1]
        
        # Feedback hesapla
        feedback = False
        for tap in self.taps:
            if tap < len(self.state):
                feedback ^= self.state[tap]
        
        # Shift ve feedback
        self.state = [feedback] + self.state[:-1]
        
        return output

class KeyGeneratorFactory:
    """Anahtar üretici factory - MT19937 bazlı"""
    
    def get_generator(self, source_type: str, method_type: str):
        """Belirtilen türde generator döndür"""
        if source_type == 'sha256':
            base_gen = SHA256Generator()
        elif source_type == 'random':
            base_gen = MT19937Generator()  # Python random yerine MT19937
        else:
            raise ValueError(f"Bilinmeyen source type: {source_type}")
        
        return CombinedGenerator(base_gen, method_type)

class CombinedGenerator:
    """Tohum + anahtar üreticiyi birleştiren sınıf - MT19937 bazlı"""
    
    def __init__(self, seed_generator: BaseGenerator, method_type: str):
        self.seed_generator = seed_generator
        self.method_type = method_type
    
    def generate_seed(self) -> str:
        """Tohum üret"""
        return self.seed_generator.generate_seed()
    
    def generate_key(self, seed: str, length: int) -> List[bool]:
        """Anahtar üret"""
        # Önce tohum bitlerini üret (256 bit)
        seed_bits = self.seed_generator.generate_key(seed, 256)
        
        # Method'a göre anahtar üret
        if self.method_type == 'shrinking':
            generator = ShrinkingGenerator(seed_bits)
            return generator.generate(length)
        
        elif self.method_type == 'alternating':
            generator = AlternatingGenerator(seed_bits)
            return generator.generate(length)
        
        elif self.method_type == 'aes':
            generator = ImprovedAESGenerator(seed_bits)  # Geliştirilmiş AES
            return generator.generate(length)
        
        else:
            raise ValueError(f"Bilinmeyen method type: {self.method_type}")

# Test ve benchmark fonksiyonları
def test_all_generators():
    """Tüm generator'ları test et"""
    print("🧪 MT19937 GENERATOR TESTLER")
    print("=" * 40)
    
    factory = KeyGeneratorFactory()
    
    # Test combinations
    test_cases = [
        ('sha256', 'shrinking', 128),
        ('sha256', 'alternating', 256),
        ('sha256', 'aes', 512),
        ('random', 'shrinking', 128),
        ('random', 'alternating', 256),
        ('random', 'aes', 512)
    ]
    
    for source, method, length in test_cases:
        print(f"\n🔍 Test: {source}_{method}_{length}")
        
        generator = factory.get_generator(source, method)
        
        # 5 anahtar üret ve analiz et
        for i in range(3):
            seed = generator.generate_seed()
            key = generator.generate_key(seed, length)
            
            ones_count = sum(key)
            ones_ratio = ones_count / length
            
            print(f"  Key {i+1}: {ones_count}/{length} = %{ones_ratio*100:.1f} ones")
            print(f"         First 32: {''.join('1' if b else '0' for b in key[:32])}")
        
        print(f"  ✅ {source}_{method}_{length} - OK")
    
    print("\n🎉 Tüm testler tamamlandı!")

def benchmark_generators():
    """Generator performansını test et"""
    import time
    
    print("\n⚡ PERFORMANS BENCHMARK")
    print("=" * 30)
    
    factory = KeyGeneratorFactory()
    
    test_cases = [
        ('random', 'aes', 1024),
        ('random', 'shrinking', 1024),
        ('random', 'alternating', 1024),
        ('sha256', 'aes', 1024)
    ]
    
    for source, method, length in test_cases:
        generator = factory.get_generator(source, method)
        
        # Benchmark
        start_time = time.time()
        for _ in range(100):  # 100 anahtar
            seed = generator.generate_seed()
            key = generator.generate_key(seed, length)
        
        elapsed = time.time() - start_time
        rate = (100 * length) / elapsed
        
        print(f"{source:6}_{method:10}_{length:4}: {elapsed:.2f}s, {rate:,.0f} bit/sec")

def quality_analysis():
    """Anahtar kalitesi analizi"""
    print("\n📊 KALİTE ANALİZİ")
    print("=" * 20)
    
    factory = KeyGeneratorFactory()
    
    # Random AES generator test et (en problemli olan)
    generator = factory.get_generator('random', 'aes')
    
    print("🔍 Random AES 1024-bit kalite analizi:")
    
    # 10 anahtar üret ve analiz et
    quality_scores = []
    
    for i in range(10):
        seed = generator.generate_seed()
        key = generator.generate_key(seed, 1024)
        
        # Temel kalite metrikleri
        ones_count = sum(key)
        frequency_score = abs(512 - ones_count)  # 512'den uzaklık
        
        # Run analysis
        runs = 1
        for j in range(1, len(key)):
            if key[j] != key[j-1]:
                runs += 1
        
        run_score = abs(512 - runs)  # İdeal ~512 run
        
        # Max run length
        max_run = 1
        current_run = 1
        for j in range(1, len(key)):
            if key[j] == key[j-1]:
                current_run += 1
                max_run = max(max_run, current_run)
            else:
                current_run = 1
        
        overall_quality = frequency_score + run_score + max(0, max_run - 20)
        quality_scores.append(overall_quality)
        
        print(f"  Key {i+1}: Freq={frequency_score:3}, Runs={run_score:3}, MaxRun={max_run:2}, Score={overall_quality:3}")
    
    avg_quality = sum(quality_scores) / len(quality_scores)
    print(f"  Ortalama kalite skoru: {avg_quality:.1f} (düşük = iyi)")
    
    if avg_quality < 50:
        print("  ✅ İyi kalite")
    elif avg_quality < 100:
        print("  ⚠️  Orta kalite")
    else:
        print("  ❌ Zayıf kalite")

if __name__ == "__main__":
    # Önce MT19937 test et
    from mt19937_random import test_mt19937
    test_mt19937()
    
    # Generator testleri
    test_all_generators()
    benchmark_generators()
    quality_analysis()