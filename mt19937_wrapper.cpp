/*
 * MT19937 Wrapper - Orjinal Mersenne Twister Implementation
 * Python'dan çağırılabilen C++ fonksiyonları
 */

#include <random>
#include <vector>
#include <cstring>
#include <cstdint>
#include <algorithm> // std::generate için eklendi
#include <functional> // std::ref için eklendi

// C linkage for Python interop
extern "C" {

// Global MT19937 generators
static std::mt19937 g_mt_generator;
static std::random_device g_rd;
static bool g_initialized = false;

/**
 * Initialize MT19937 with hardware entropy
 */
void mt19937_init() {
    if (!g_initialized) {
        std::vector<uint32_t> seed_data(std::mt19937::state_size);
        // std::generate fonksiyonunu kullanabilmek için <algorithm> eklendi
        // std::ref kullanabilmek için <functional> eklendi
        std::generate(seed_data.begin(), seed_data.end(), std::ref(g_rd));
        std::seed_seq seq(seed_data.begin(), seed_data.end());
        g_mt_generator.seed(seq);
        g_initialized = true;
    }
}

/**
 * Initialize MT19937 with specific seed
 */
void mt19937_seed(uint32_t seed) {
    g_mt_generator.seed(seed);
    g_initialized = true;
}

/**
 * Initialize MT19937 with seed array
 */
void mt19937_seed_array(uint32_t* seeds, int length) {
    std::vector<uint32_t> seed_data(seeds, seeds + length);
    std::seed_seq seq(seed_data.begin(), seed_data.end());
    g_mt_generator.seed(seq);
    g_initialized = true;
}

/**
 * Generate single random uint32
 */
uint32_t mt19937_uint32() {
    if (!g_initialized) {
        mt19937_init();
    }
    return g_mt_generator();
}

/**
 * Generate array of random uint32
 */
void mt19937_uint32_array(uint32_t* output, int count) {
    if (!g_initialized) {
        mt19937_init();
    }
    
    for (int i = 0; i < count; i++) {
        output[i] = g_mt_generator();
    }
}

/**
 * Generate single random bit (0 or 1)
 */
int mt19937_bit() {
    if (!g_initialized) {
        mt19937_init();
    }
    return g_mt_generator() & 1;
}

/**
 * Generate array of random bits as bytes (8 bits per byte)
 */
void mt19937_bits(unsigned char* output, int bit_count) {
    if (!g_initialized) {
        mt19937_init();
    }
    
    int byte_count = (bit_count + 7) / 8;  // Round up
    
    for (int i = 0; i < byte_count; i++) {
        uint32_t random_val = g_mt_generator();
        
        // Pack 8 bits into one byte
        unsigned char byte_val = 0;
        for (int j = 0; j < 8 && (i * 8 + j) < bit_count; j++) {
            if (random_val & (1u << j)) {
                byte_val |= (1u << j);
            }
        }
        
        output[i] = byte_val;
    }
}

/**
 * Generate random bits as individual integers (1 bit per int)
 */
void mt19937_bit_array(int* output, int bit_count) {
    if (!g_initialized) {
        mt19937_init();
    }
    
    for (int i = 0; i < bit_count; i++) {
        output[i] = g_mt_generator() & 1;
    }
}

/**
 * Generate random float in range [0, 1)
 */
double mt19937_double() {
    if (!g_initialized) {
        mt19937_init();
    }
    
    return std::uniform_real_distribution<double>(0.0, 1.0)(g_mt_generator);
}

/**
 * Generate random integer in range [min, max]
 */
int mt19937_int_range(int min_val, int max_val) {
    if (!g_initialized) {
        mt19937_init();
    }
    
    return std::uniform_int_distribution<int>(min_val, max_val)(g_mt_generator);
}

/**
 * Get current state (for debugging)
 */
void mt19937_get_state(uint32_t* state_output) {
    // Note: This would require access to internal state
    // For now, just return current generator output
    *state_output = mt19937_uint32();
}

/**
 * Reset generator to initial state
 */
void mt19937_reset() {
    g_initialized = false;
    mt19937_init();
}

/**
 * Generate hex string seed (like Python secrets.token_hex)
 */
void mt19937_hex_seed(char* output, int byte_length) {
    if (!g_initialized) {
        mt19937_init();
    }
    
    const char hex_chars[] = "0123456789abcdef";
    
    for (int i = 0; i < byte_length; i++) {
        uint32_t random_byte = g_mt_generator() & 0xFF;
        output[i * 2] = hex_chars[(random_byte >> 4) & 0xF];
        output[i * 2 + 1] = hex_chars[random_byte & 0xF];
    }
    
    output[byte_length * 2] = '\0';  // Null terminate
}

} // extern "C"
