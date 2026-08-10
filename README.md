# crypto-keygen-study

Experimental pipeline and dataset for measuring the statistical quality of cryptographic keys produced by three key-generation constructions seeded from a C++ MT19937 source.

DOI: [10.5281/zenodo.17751787](https://doi.org/10.5281/zenodo.17751787)

## What it is

A two-stage Python experiment, backed by a small C++ shared library, that:

1. **Generates keys** with three constructions — a shrinking generator (2 LFSRs), an alternating-step generator (3 LFSRs), and an AES-like substitution–permutation generator — at six key lengths (128, 256, 512, 1024, 2048, 4096 bits), 1,000 keys per combination.
2. **Tests every key** with a suite of 9 statistical randomness tests (frequency, run count, length-1 runs, four 4-bit template counts, Berlekamp–Massey linear complexity, and a "blind spot" complexity measure), evaluated against precomputed acceptance intervals at two significance thresholds (0.01 and 0.05).

The repository ships with the complete experimental dataset in `output1/` (~121 MB): 18,000 generated keys (3 methods × 6 lengths × 1,000 keys, MT19937 source), per-key test results, and aggregated pass-rate reports.

## Why it exists

This is the code-and-data companion to a research experiment on key-generation quality (archived on Zenodo under the DOI above). The question it explores: when the same pseudorandom source (MT19937) feeds different key-derivation constructions, how do the resulting keys fare under classical randomness tests, and how does that vary with key length and test strictness? The statistical tests are count-based variants inspired by NIST SP 800-22.

## How it works

```
generate_keys_only.py                    test_keys_only.py
  │                                        │
  │ src/config.py (combinations)           │ loads output/keys/*.txt
  │ src/generators_mt19937.py              │ src/testers_fixed.py (9 tests)
  │   ├─ seed source: MT19937 or SHA256    │   acceptance intervals per
  │   └─ method: shrinking /               │   key length × threshold
  │      alternating / AES-like SPN        │
  ▼                                        ▼
output/keys/*.txt                        output/test_results/, detailed_results/,
(one binary key per line)                reports/*.csv
```

- **Entropy source.** `mt19937_wrapper.cpp` exposes the C++ standard library's `std::mt19937` (seeded across its full state from `std::random_device`) through a C ABI. `mt19937_random.py` loads the compiled DLL/SO via `ctypes` and will attempt to compile it automatically if missing. Python's own `random` module is deliberately never used. A prebuilt `mt19937_wrapper.dll` and the MinGW runtime DLLs it needs are included for Windows.
- **Seeding.** For each key, a seed generator (MT19937-backed, or alternatively an SHA256 hash chain) produces 256 seed bits, which initialize the chosen construction's state (LFSR registers, or the SPN's 128-bit key).
- **The "AES-like" generator** is a counter-mode SPN: XOR key with counter, then 4 rounds of a 4-bit S-box, a fixed bit permutation, and an MT19937-derived round key. It borrows AES's shape, not its algorithm — see caveats.
- **Testing.** Each test returns an integer statistic; a key passes a test if the statistic falls inside a hard-coded acceptance interval for that key length and threshold (`src/testers_fixed.py`). Per-test and overall pass rates are aggregated into `reports/final_experiment_results.csv`.

## Building & running

Requirements: Python 3.8+, `pandas`, and a C++ compiler (g++ / MinGW-w64 on Windows).

```bash
# 1. Environment
python -m venv venv
venv\Scripts\activate            # Windows (Linux/macOS: source venv/bin/activate)
pip install -r requirements.txt

# 2. Compile the MT19937 shared library
g++ -shared -fPIC -O2 -std=c++11 mt19937_wrapper.cpp -o mt19937_wrapper.dll      # Windows
g++ -shared -fPIC -O2 -std=c++11 mt19937_wrapper.cpp -o libmt19937_wrapper.so    # Linux
g++ -shared -fPIC -O2 -std=c++11 mt19937_wrapper.cpp -o libmt19937_wrapper.dylib # macOS

# 3. Run the pipeline (optional — results are already committed in output1/)
python generate_keys_only.py     # stage 1: writes output/keys/
python test_keys_only.py         # stage 2: writes output/test_results/, detailed_results/, reports/
```

On Windows, the batch helpers `setup_experiment.bat`, `compile_mt19937.bat`, `generate_keys.bat`, and `test_keys.bat` wrap the same steps.

### Repository layout

```
generate_keys_only.py    # stage 1: key generation
test_keys_only.py        # stage 2: statistical testing
mt19937_wrapper.cpp      # C ABI over std::mt19937
mt19937_random.py        # ctypes loader / auto-compiler for the DLL
src/
  config.py              # sources, methods, key lengths, thresholds
  generators_mt19937.py  # LFSR, shrinking, alternating, AES-like SPN
  testers_fixed.py       # 9 tests + acceptance intervals
  utils_fixed.py         # key file I/O, logging
output1/                 # committed experimental dataset (~121 MB)
  keys/  test_results/  detailed_results/  reports/
```

## Status & caveats

- **Research code, not production cryptography.** MT19937 is not a cryptographically secure RNG, and the LFSR constructions here are study subjects, not recommended key generators. Do not use any of this to generate real keys.
- **"AES-like" is not AES.** The SPN generator uses a 4-bit S-box, an ad-hoc bit permutation, and 4 rounds; it shares no components with actual AES.
- **Committed data covers half the configured experiment.** `src/config.py` defines 36 combinations (2 sources × 3 methods × 6 lengths), and `generate_keys_only.py` will regenerate all 36 (~36,000 keys). The committed dataset in `output1/` covers only the 18 MT19937 (`random_*`) combinations.
- **`output/` vs `output1/`.** The scripts read and write `output/`; the archived results live in `output1/`. Rename or copy if you want the test stage to run against the committed keys.
- **Test-suite scope.** The 9 tests are integer-count variants inspired by NIST SP 800-22, with acceptance intervals hard-coded per key length and threshold; this is not the full NIST battery and intervals are not derived in-repo. Note also an internal inconsistency: the aggregate pass check uses exclusive interval bounds while the per-test check uses inclusive bounds (`src/testers_fixed.py`).
- **Language.** Code comments, log messages, and console output are largely in Turkish.
- **Repo size.** Roughly 121 MB of CSV/text results are committed; clone accordingly.

## License

MIT — see [LICENSE](LICENSE).

## Acknowledgments

- MT19937: Matsumoto & Nishimura (1998), via `std::mt19937`.
- Statistical tests inspired by NIST SP 800-22.