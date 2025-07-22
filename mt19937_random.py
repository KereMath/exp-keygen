"""
MT19937 Python Wrapper - Orjinal C++ MT19937'yi kullanır
Python'un kendi random modülü yerine
"""

import ctypes
import os
import sys
import platform # platform.system() için
import subprocess # subprocess.run için
import logging
from typing import List, Union
from pathlib import Path

# Loglama ayarları
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class MT19937Random:
    """Orjinal MT19937 implementasyonunu kullanır"""
    
    def __init__(self):
        """C++ kütüphanesini yükle"""
        self._lib = None
        self._load_library()
        self._setup_functions()
        
        # Otomatik initialize
        self._lib.mt19937_init()
        
    def _get_library_filename(self) -> str:
        """İşletim sistemine göre kütüphane dosya adını döndürür."""
        if sys.platform == "win32":
            return "mt19937_wrapper.dll"
        elif sys.platform == "darwin": # macOS
            return "libmt19937_wrapper.dylib"
        else: # Linux ve diğer Unix benzeri sistemler
            return "libmt19937_wrapper.so"

    def _load_library(self):
        """C++ shared library'yi yükle. Yoksa derle."""
        lib_name = self._get_library_filename()
        
        # Olası kütüphane yollarını kontrol et
        possible_paths = [
            Path(__file__).parent / lib_name, # Script'in olduğu dizin
            Path(".") / lib_name,             # Mevcut çalışma dizini
            Path("./lib") / lib_name,         # lib alt dizini
            Path("./src") / lib_name,         # src alt dizini
        ]
        
        found_lib_path = None
        for lib_path in possible_paths:
            if lib_path.exists():
                try:
                    self._lib = ctypes.CDLL(str(lib_path))
                    found_lib_path = lib_path
                    logging.info(f"✅ MT19937 C++ kütüphanesi '{lib_path}' başarıyla yüklendi.")
                    break
                except OSError as e:
                    # DLL bulundu ama yüklenemedi (muhtemelen bağımlılıklar eksik)
                    logging.warning(f"Kütüphane '{lib_path}' yüklenirken hata oluştu: {e}. Diğer yollar deneniyor...")
                    continue
        
        if found_lib_path is None:
            logging.info(f"'{lib_name}' bulunamadı. Kütüphane derleniyor...")
            self._compile_library()
            # Derleme sonrası tekrar yüklemeyi dene (bu sefer ana dizinde olmalı)
            try:
                self._lib = ctypes.CDLL(str(Path(__file__).parent / lib_name))
                logging.info(f"✅ MT19937 C++ kütüphanesi '{lib_name}' başarıyla derlendi ve yüklendi.")
            except OSError as e:
                logging.error(f"Derleme sonrası kütüphane yüklenirken kritik hata: {e}")
                raise RuntimeError(f"❌ MT19937 C++ kütüphanesi derlendi ancak yüklenemedi! Hata: {e}. Bağımlılık DLL'lerinin (libstdc++-6.dll, libgcc_s_seh-1.dll, libwinpthread-1.dll) 'mt19937_wrapper.dll' ile aynı dizinde olduğundan emin olun.")
        
    def _compile_library(self):
        """C++ kodunu otomatik compile et"""
        cpp_file = Path(__file__).parent / "mt19937_wrapper.cpp"
        lib_name = self._get_library_filename()
        output_lib_path = Path(__file__).parent / lib_name # Çıktı DLL'in yolu
        
        if not cpp_file.exists():
            raise FileNotFoundError(f"'{cpp_file}' bulunamadı. Lütfen ana klasöre kopyalayın.")

        compile_command = []
        if sys.platform == "win32":
            compile_command = ["g++", "-shared", "-fPIC", "-O2", "-std=c++11", str(cpp_file), "-o", str(output_lib_path)]
        elif sys.platform == "darwin":
            compile_command = ["g++", "-shared", "-fPIC", "-O2", "-std=c++11", str(cpp_file), "-o", str(output_lib_path)]
        else: # Linux
            compile_command = ["g++", "-shared", "-fPIC", "-O2", "-std=c++11", str(cpp_file), "-o", str(output_lib_path)]
        
        logging.info(f"🔧 MT19937 C++ kütüphanesi derleniyor: {' '.join(compile_command)}")
        
        # g++'ın yolunu PATH'e ekleyerek subprocess'in bulmasını sağla
        current_env = os.environ.copy()
        mingw_bin_path = r"C:\msys64\mingw64\bin" # Kullanıcının verdiği yol
        if mingw_bin_path not in current_env.get('PATH', ''):
            current_env['PATH'] = f"{mingw_bin_path};{current_env.get('PATH', '')}"
            logging.info(f"Geçici olarak PATH'e '{mingw_bin_path}' eklendi.")

        try:
            result = subprocess.run(compile_command, check=True, capture_output=True, text=True, env=current_env)
            logging.info("Derleme çıktısı:")
            logging.info(result.stdout)
            if result.stderr:
                logging.warning("Derleme uyarıları/hataları:")
                logging.warning(result.stderr)
            logging.info("✅ MT19937 C++ kütüphanesi başarıyla derlendi.")
        except subprocess.CalledProcessError as e:
            logging.error(f"Derleme hatası: {e}")
            logging.error(f"Derleme standard çıktısı: {e.stdout}")
            logging.error(f"Derleme hata çıktısı: {e.stderr}")
            raise RuntimeError("❌ MT19937 C++ kütüphanesi compile edilemedi! g++ yüklü mü? Detaylar için yukarıdaki logları kontrol edin.")
        except FileNotFoundError:
            raise RuntimeError("❌ g++ bulunamadı! Lütfen MinGW-w64 (Windows) veya GCC (Linux/macOS) kurun ve PATH'e ekleyin veya 'C:\\msys64\\mingw64\\bin' yolunu kontrol edin.")
    
    def _setup_functions(self):
        """C fonksiyonlarının signature'larını ayarla"""
        if not self._lib:
            raise RuntimeError("MT19937 library yüklenemedi!")
        
        # Function signatures
        self._lib.mt19937_init.argtypes = []
        self._lib.mt19937_init.restype = None
        
        self._lib.mt19937_seed.argtypes = [ctypes.c_uint32]
        self._lib.mt19937_seed.restype = None

        self._lib.mt19937_seed_array.argtypes = [ctypes.POINTER(ctypes.c_uint32), ctypes.c_int]
        self._lib.mt19937_seed_array.restype = None
        
        self._lib.mt19937_uint32.argtypes = []
        self._lib.mt19937_uint32.restype = ctypes.c_uint32

        self._lib.mt19937_uint32_array.argtypes = [ctypes.POINTER(ctypes.c_uint32), ctypes.c_int]
        self._lib.mt19937_uint32_array.restype = None
        
        self._lib.mt19937_bit.argtypes = []
        self._lib.mt19937_bit.restype = ctypes.c_int

        self._lib.mt19937_bits.argtypes = [ctypes.POINTER(ctypes.c_ubyte), ctypes.c_int]
        self._lib.mt19937_bits.restype = None
        
        self._lib.mt19937_bit_array.argtypes = [ctypes.POINTER(ctypes.c_int), ctypes.c_int]
        self._lib.mt19937_bit_array.restype = None
        
        self._lib.mt19937_double.argtypes = []
        self._lib.mt19937_double.restype = ctypes.c_double
        
        self._lib.mt19937_int_range.argtypes = [ctypes.c_int, ctypes.c_int]
        self._lib.mt19937_int_range.restype = ctypes.c_int
        
        self._lib.mt19937_hex_seed.argtypes = [ctypes.c_char_p, ctypes.c_int]
        self._lib.mt19937_hex_seed.restype = None
    
    def seed(self, seed_value: int):
        """MT19937'yi tek bir seed ile initialize et"""
        self._lib.mt19937_seed(ctypes.c_uint32(seed_value))

    def seed_array(self, seed_array_val: List[int]):
        """MT19937'yi bir seed dizisi ile initialize et"""
        arr_type = ctypes.c_uint32 * len(seed_array_val)
        self._lib.mt19937_seed_array(arr_type(*seed_array_val), len(seed_array_val))
    
    def random(self) -> float:
        """[0, 1) aralığında random float"""
        return self._lib.mt19937_double()
    
    def randint(self, min_val: int, max_val: int) -> int:
        """[min_val, max_val] aralığında random int"""
        return self._lib.mt19937_int_range(min_val, max_val)

    def get_uint32(self) -> int:
        """Tek bir rastgele uint32 değeri döndürür."""
        return self._lib.mt19937_uint32()

    def get_uint32_array(self, count: int) -> List[int]:
        """Belirtilen sayıda rastgele uint32 değeri içeren bir dizi döndürür."""
        output_array = (ctypes.c_uint32 * count)()
        self._lib.mt19937_uint32_array(output_array, count)
        return list(output_array)
    
    def choice(self, choices: List) -> Union[int, float, str, bool]:
        """List'ten random element seç"""
        # Boş liste kontrolü
        if not choices:
            raise ValueError("Boş listeden seçim yapılamaz.")
        index = self.randint(0, len(choices) - 1)
        return choices[index]
    
    def randbit(self) -> bool:
        """Random bit (True/False)"""
        return bool(self._lib.mt19937_bit())
    
    def randbits(self, count: int) -> List[bool]:
        """Random bit array (her bit ayrı bir bool olarak)"""
        # C array oluştur
        result_array = (ctypes.c_int * count)()
        
        # C fonksiyonu çağır
        self._lib.mt19937_bit_array(result_array, count)
        
        # Python list'e dönüştür
        return [bool(result_array[i]) for i in range(count)]

    def get_bits_as_bytes(self, bit_count: int) -> bytes:
        """Belirtilen sayıda rastgele biti bayt olarak döndürür."""
        byte_count = (bit_count + 7) // 8
        output_array = (ctypes.c_ubyte * byte_count)()
        self._lib.mt19937_bits(output_array, bit_count)
        return bytes(output_array)
    
    def token_hex(self, nbytes: int = 32) -> str:
        """Hex token üret (secrets.token_hex benzeri)"""
        # C buffer oluştur
        buffer_size = nbytes * 2 + 1  # hex + null terminator
        buffer = ctypes.create_string_buffer(buffer_size)
        
        # C fonksiyonu çağır
        self._lib.mt19937_hex_seed(buffer, nbytes)
        
        return buffer.value.decode('ascii')

# Global instance
_mt_random = None

def get_mt_random() -> MT19937Random:
    """Global MT19937 instance al"""
    global _mt_random
    if _mt_random is None:
        _mt_random = MT19937Random()
    return _mt_random

# Convenience functions (Python random module tarzı)
def seed(seed_value: int):
    """Global seed ayarla"""
    get_mt_random().seed(seed_value)

def random() -> float:
    """Random float [0, 1)"""
    return get_mt_random().random()

def randint(a: int, b: int) -> int:
    """Random int [a, b]"""
    return get_mt_random().randint(a, b)

def choice(seq: List):
    """Random choice"""
    return get_mt_random().choice(seq)

def randbit() -> bool:
    """Random bit"""
    return get_mt_random().randbit()

def randbits(k: int) -> List[bool]:
    """Random bit array"""
    return get_mt_random().randbits(k)

def token_hex(nbytes: int = 32) -> str:
    """Hex token"""
    return get_mt_random().token_hex(nbytes)

# Test fonksiyonu
def test_mt19937():
    """MT19937 testleri"""
    logging.info("🧪 MT19937 C++ Wrapper Test")
    logging.info("=" * 30)
    
    mt = MT19937Random()
    
    # Basic tests
    logging.info(f"Random float: {mt.random()}")
    logging.info(f"Random int (1-100): {mt.randint(1, 100)}")
    logging.info(f"Random choice: {mt.choice(['A', 'B', 'C', 'D'])}")
    logging.info(f"Random bit: {mt.randbit()}")
    
    # Bit array test
    bits = mt.randbits(32)
    bit_str = ''.join('1' if b else '0' for b in bits)
    logging.info(f"32 random bits: {bit_str}")

    # Uint32 array test
    uint32_arr = mt.get_uint32_array(5)
    logging.info(f"5 random uint32 values: {uint32_arr}")

    # Bits as bytes test
    bytes_from_bits = mt.get_bits_as_bytes(24) # 3 bytes
    logging.info(f"24 random bits as bytes (hex): {bytes_from_bits.hex()}")
    
    # Hex token test
    hex_token = mt.token_hex(16)
    logging.info(f"Hex token (16 bytes): {hex_token}")
    
    # Seed consistency test
    mt.seed(12345)
    val1 = mt.randint(1, 1000000)
    
    mt.seed(12345)  # Same seed
    val2 = mt.randint(1, 1000000)
    
    logging.info(f"Seed consistency: {val1} == {val2} ? {val1 == val2}")
    
    # Seed array test
    seed_arr = [1, 2, 3, 4]
    mt.seed_array(seed_arr)
    val_arr_seeded1 = mt.get_uint32()
    mt.seed_array(seed_arr)
    val_arr_seeded2 = mt.get_uint32()
    logging.info(f"Seed array consistency: {val_arr_seeded1} == {val_arr_seeded2} ? {val_arr_seeded1 == val_arr_seeded2}")

    logging.info("✅ MT19937 test tamamlandı!")

if __name__ == "__main__":
    test_mt19937()
