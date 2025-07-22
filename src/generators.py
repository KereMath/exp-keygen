"""
Anahtar üretici algoritmaları - Basitleştirilmiş versiyon
"""

import hashlib
import secrets
import random
from typing import List, Tuple

class BaseGenerator:
    """Temel üretici sınıfı"""
    
    def generate_seed(self) -> str:
        """Tohum üretir (override edilecek)"""
        raise NotImplementedError
    
    def generate_key(self, seed: str, length: int) -> List[bool]:
        """Anahtar üretir (override edilecek)"""
        raise NotImplementedError

class SHA256Generator(BaseGenerator):
    """SHA256 tabanlı üretici"""
    
    def __init__(self):
        self.seed_counter = 0
    
    def generate_seed(self) -> str:
        """Tohum üret"""
        self.seed_counter += 1
        return f"experiment_seed_2024_{self.seed_counter}"
    
    def generate_key(self, seed: str, length: int) -> List[bool]:
        """SHA256 ile anahtar üret"""
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

class RandomGenerator(BaseGenerator):
    """Rastgele üretici"""
    
    def generate_seed(self) -> str:
        """Rastgele tohum üret"""
        return secrets.token_hex(32)
    
    def generate_key(self, seed: str, length: int) -> List[bool]:
        """Rastgele anahtar üret"""
        # Seed'i kullanarak deterministic rastgelelik
        random.seed(seed)
        return [random.choice([True, False]) for _ in range(length)]

class ShrinkingGenerator:
    """Shrinking generator algoritması"""
    
    def __init__(self, seed_bits: List[bool]):
        # LFSR'ları initialize et
        mid_point = len(seed_bits) // 2
        self.lfsr1 = LFSR(seed_bits[:mid_point], [0, 7, 15, 23])      # Control LFSR
        self.lfsr2 = LFSR(seed_bits[mid_point:], [0, 5, 13, 21])     # Data LFSR
    
    def generate(self, length: int) -> List[bool]:
        """Shrinking generator ile anahtar üret"""
        output = []
        
        while len(output) < length:
            control_bit = self.lfsr1.next_bit()
            data_bit = self.lfsr2.next_bit()
            
            # Control bit 1 ise data bit'i al
            if control_bit:
                output.append(data_bit)
        
        return output[:length]

class AlternatingGenerator:
    """Alternating step generator"""
    
    def __init__(self, seed_bits: List[bool]):
        # 3 LFSR'a böl
        third = len(seed_bits) // 3
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

class AESGenerator:
    """AES benzeri generator (basitleştirilmiş)"""
    
    def __init__(self, seed_bits: List[bool]):
        self.key_bits = seed_bits[:128] if len(seed_bits) >= 128 else seed_bits + [False] * (128 - len(seed_bits))
        self.counter = 0
    
    def generate(self, length: int) -> List[bool]:
        """AES benzeri anahtar üret"""
        output = []
        
        while len(output) < length:
            # Basit "AES" işlemi - gerçekte XOR ve shift
            self.counter += 1
            
            # Key ile counter'ı XOR'la
            counter_bits = self._int_to_bits(self.counter, 128)
            block = [a ^ b for a, b in zip(self.key_bits, counter_bits)]
            
            # Basit substitution (bit yer değiştirme)
            block = self._substitute(block)
            
            output.extend(block)
        
        return output[:length]
    
    def _int_to_bits(self, value: int, bit_count: int) -> List[bool]:
        """Integer'ı bit listesine dönüştür"""
        bits = []
        for i in range(bit_count):
            bits.append((value >> i) & 1 == 1)
        return bits
    
    def _substitute(self, bits: List[bool]) -> List[bool]:
        """Basit bit substitution"""
        # Basit permutation
        result = bits.copy()
        for i in range(0, len(result)-1, 2):
            result[i], result[i+1] = result[i+1], result[i]
        return result

class LFSR:
    """Linear Feedback Shift Register"""
    
    def __init__(self, initial_state: List[bool], taps: List[int]):
        self.state = initial_state.copy()
        self.taps = taps
        
        # Tüm sıfır durumunu önle
        if not any(self.state):
            self.state[0] = True
    
    def next_bit(self) -> bool:
        """Bir sonraki bit üret"""
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
    """Anahtar üretici factory"""
    
    def get_generator(self, source_type: str, method_type: str):
        """Belirtilen türde generator döndür"""
        if source_type == 'sha256':
            base_gen = SHA256Generator()
        elif source_type == 'random':
            base_gen = RandomGenerator()
        else:
            raise ValueError(f"Bilinmeyen source type: {source_type}")
        
        return CombinedGenerator(base_gen, method_type)

class CombinedGenerator:
    """Tohum + anahtar üreticiyi birleştiren sınıf"""
    
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
            generator = AESGenerator(seed_bits)
            return generator.generate(length)
        
        else:
            raise ValueError(f"Bilinmeyen method type: {self.method_type}")