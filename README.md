# Cryptographic Key Generation Quality Analysis

**Experimental code and data for statistical quality analysis of MT19937-based cryptographic key generation algorithms.**

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.XXXXXXX.svg)](https://doi.org/10.5281/zenodo.XXXXXXX)
*Note: Update DOI after Zenodo release*

## Overview

This repository contains the source code and experimental data for analyzing the statistical quality of cryptographic keys generated using **MT19937-based pseudorandom number generation** with three different generation methods.

**Key Features:**
- **3 generation methods:** Shrinking Generator, Alternating Step Generator, AES-like Generator
- **Random source:** MT19937 (Mersenne Twister) via C++ implementation
- **6 key lengths:** 128, 256, 512, 1024, 2048, 4096 bits
- **9 statistical tests** for randomness quality assessment
- **18 experimental combinations** (3 methods x 6 lengths)
- **18,000 total keys** (1,000 per combination)
- Complete two-stage experimental pipeline

## Contents

**Code (Python + C++):**
- Key generation algorithms (3 methods)
- MT19937 C++ implementation (hardware entropy)
- Statistical testing suite (9 tests)

**Data (Experimental results - 121 MB):**
- Generated keys (18,000 keys)
- Test results (statistical analysis)
- Final reports (aggregated metrics)

**Note:** The codebase supports both SHA256 (deterministic) and MT19937 (pseudorandom) sources, but the included experimental data uses **MT19937 only**.

## Requirements

### Software
- **Python 3.8+** (tested on 3.9)
- **pandas** library for data analysis
- **C++ compiler** (g++ or MinGW-w64 for Windows)


## Quick Start

### 1. Setup Environment

```bash
# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Linux/Mac)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Compile MT19937 Library

**Windows (MinGW):**
```bash
g++ -shared -fPIC -O2 -std=c++11 mt19937_wrapper.cpp -o mt19937_wrapper.dll
```

**Linux:**
```bash
g++ -shared -fPIC -O2 -std=c++11 mt19937_wrapper.cpp -o libmt19937_wrapper.so
```

**macOS:**
```bash
g++ -shared -fPIC -O2 -std=c++11 mt19937_wrapper.cpp -o libmt19937_wrapper.dylib
```

### 3. Run Pipeline

#### Stage 1: Generate Keys (Optional - data already included)
```bash
python generate_keys_only.py
```

**Output:** `output/keys/*.txt` (18 files, ~24 MB)


#### Stage 2: Statistical Testing (Optional - results already included)
```bash
python test_keys_only.py
```

**Output:**
- `output/test_results/*.csv` - Individual test results
- `output/detailed_results/*.csv` - Detailed per-key analysis
- `output/reports/*.csv` - Aggregated statistics


### Reproduce Full Experiment
```bash
python generate_keys_only.py && python test_keys_only.py
```

## Experimental Design

### Key Generation Methods

| Method | Description | LFSR Count |
|--------|-------------|------------|
| **Shrinking** | Control bit selects data bit | 2 |
| **Alternating** | Control bit switches between LFSRs | 3 |
| **AES-like** | Substitution-permutation network with round keys | - |

### Random Source

**MT19937 (Mersenne Twister)**
- **Type:** Pseudorandom number generator
- **Implementation:** Native C++ `std::mt19937`
- **Seeding:** Hardware entropy via `std::random_device`


### Statistical Tests

1. **Frequency Test** - Bit distribution balance (0s vs 1s)
2. **Run Count Test** - Number of consecutive bit runs
3. **Run Length (L1) Test** - Longest run detection
4. **Template Tests (4-1 to 4-4)** - 4-bit pattern distribution
5. **Linear Complexity Test** - Berlekamp-Massey algorithm
6. **Blind Spot Complexity Test** - Local complexity variations

**Evaluation Thresholds:**
- **0.01** - 99% confidence level (strict)
- **0.05** - 95% confidence level (standard)

## Repository Structure

```
keygen-experiment/
├── generate_keys_only.py       # Key generation script
├── test_keys_only.py            # Statistical testing script
├── mt19937_wrapper.cpp          # C++ MT19937 implementation
├── mt19937_random.py            # Python wrapper for DLL
├── requirements.txt             # Python dependencies
├── src/
│   ├── config.py                # Experiment configuration
│   ├── generators_mt19937.py    # Key generation algorithms
│   ├── testers_fixed.py         # Statistical test suite
│   └── utils_fixed.py           # File I/O and logging utilities
├── output1/                     # Experimental data (121 MB)
│   ├── keys/                    # Raw key files (18 files)
│   ├── test_results/            # CSV test results
│   ├── detailed_results/        # Per-key analysis
│   └── reports/                 # Aggregated reports
└── logs/                        # Execution logs
```

## Technical Details

### MT19937 Implementation

This project uses **native C++ MT19937** (`std::mt19937`) instead of Python's `random` module


**Architecture:**
```
Python (generate_keys_only.py)
    |
    v
Python Wrapper (mt19937_random.py)
    | (ctypes interface)
    v
C++ DLL (mt19937_wrapper.dll)
    |
    v
std::mt19937 (C++ Standard Library)
```

**DLL Compilation:** The C++ source is compiled into a shared library (DLL/SO/DYLIB) and called from Python using `ctypes`.

### Pipeline Design

The experimental pipeline is split into **two independent stages**:

**Stage 1: Key Generation**
- Reads configuration (3 methods x 6 lengths)
- Generates 1,000 keys per combination
- Saves to `output/keys/*.txt`

**Stage 2: Statistical Testing**
- Loads keys from disk
- Applies 9 tests to each key
- Evaluates with 2 threshold values
- Saves detailed results and aggregated reports


## Data Format

### Key Files (`output1/keys/*.txt`)
```
Format: One key per line, binary string representation
Example: random_aes_1024_keys.txt

1010110101...1001101  (1024 bits)
0110101001...0101010  (1024 bits)
...
(1000 keys total)
```

### Test Results (`output1/test_results/*.csv`)
```csv
key_id,key_bits,passed,frequency,run_count,run_L1,...
1,101011...,True,502,487,23,...
2,011010...,False,611,521,45,...
```

### Aggregated Reports (`output1/reports/final_experiment_results.csv`)
```csv
source_type,method_type,key_length,threshold,total_keys,passed_keys,pass_rate_percent
random,aes,128,0.01,1000,975,97.5
random,aes,128,0.05,1000,957,95.7
...
```


## License

This project is licensed under the **MIT License** - see [LICENSE](LICENSE) file for details.


## Acknowledgments

- MT19937 algorithm: Matsumoto & Nishimura (1998)
- Statistical tests based on NIST SP 800-22

