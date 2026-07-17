# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Project Is

A **Frequency-Domain Electromagnetic (FDEM) geophysical survey system** that maps subsurface conductors (buried pipes, objects, geology). An operator walks or carts the instrument across a field while the system:
1. Plays a driving waveform (100 Hz pure sine by default) out of the Raspberry Pi audio port into a transmitter coil
2. Acquires the induced response on two secondary receiver coils via MCC172 DAQ HATs
3. Records GPS coordinates simultaneously
4. Post-processes with lock-in amplifier techniques to extract the in-phase/out-of-phase envelopes and georeferenced maps

There is a secondary acquisition path (**MEDA**) using a standalone serial fluxgate magnetometer instead of the DAQ.

## Repository Layout

```
FDEM/
├── scan.sh / scan_MEDA.sh      # Field launchers (run on Raspberry Pi)
├── signal_acquisition.py       # DAQ recorder (MCC172 HATs, 2 kHz, 3 channels)
├── gps.py                      # GPS recorder (u-blox, ~1 Hz)
├── button_mag.py               # Fluxgate (MEDA) recorder (serial, ~4 Hz)
├── wav_gen.py                  # Generates driving waveform WAV files
├── wav_checker.py              # Inspects WAV spectra
├── utilities/
│   ├── wave_gen_utils.py       # Pure tone / chirp / frequency-comb generators
│   ├── signal_analysis_utils.py # Lock-in DSP algorithms
│   └── daqhats_utils.py        # MCC HAT helpers
├── signal_analysis.ipynb       # Raw signal visualization and FFT
├── lock_in.ipynb               # Digital lock-in signal processing (synthetic + real)
├── mag_mapping.ipynb           # GPS–signal fusion and geospatial maps
├── MEDA_analysis.ipynb         # Fluxgate magnetometer analysis
└── misc_scripts/               # Legacy/experimental scripts
```

`data/` is gitignored and synced separately via `rclone` to OneDrive.

## Development Environment

- **Analysis** runs on macOS with conda Python (3.12+). The VS Code workspace is configured to use conda as the package manager.
- **Acquisition** runs on a Raspberry Pi with the `daqhats` library installed (gitignored; must be installed separately on the Pi from MCC's repo).
- No `requirements.txt` or `environment.yml` exists. Key packages: `numpy`, `scipy`, `pandas`, `plotly`, `utm`, `ublox_gps`, `daqhats`.

## Architecture: Two-Machine Split

**Raspberry Pi (field acquisition)**
- `scan.sh` orchestrates everything: it plays the WAV via `aplay`, launches `signal_acquisition.py` and `gps.py` in parallel, waits for both to finish, then `rclone`-syncs the output CSVs to OneDrive.
- `signal_acquisition.py` uses two stacked MCC172 HATs at addresses 0 (primary feedback) and 2 (Ch 1 and Ch 2 secondary). Clock and trigger are synced master/slave across the two boards. Output: `mag.csv` with columns `Times (s), Primary (V), Ch 1 (V), Ch 2 (V)` at 2 kHz.
- `gps.py` records lat/lon/heading at ~1 Hz. Both acquisition scripts timestamp using **wall-clock seconds-of-day** (`hours×3600 + minutes×60 + seconds`) so the two files can be joined on a common time axis.

**macOS (analysis)**
- `mag_mapping.ipynb` is the primary end-to-end analysis notebook: loads `mag.csv` + `gps.csv`, synchronizes them, computes RMS and lock-in envelopes, filters out GPS turns (heading change > 5°), spline-interpolates signal to GPS timestamps, converts lat/lon → UTM via `utm`, and exports `arcgis_data.csv` + scatter-plot maps.
- `lock_in.ipynb` documents and tests the lock-in pipeline in detail (synthetic signal first, then real data).

## Core DSP: Lock-In Amplifier (`utilities/signal_analysis_utils.py`)

The key function is `get_harmonic_envelope(received, sample_rate, driving, driving_freq, order)`:
1. Computes the analytic (complex) Hilbert transform of the driving signal raised to the `order`-th harmonic
2. Multiplies the received signal by this reference to demodulate
3. Applies a boxcar low-pass FIR filter to extract the slowly-varying envelope
4. Returns `(in_phase, out_of_phase, magnitude)` envelopes

`get_total_envelope` provides a broadband alternative (Hilbert transform of the low-passed received signal). The `autocorrelation` function uses FFT-based circular correlation.

## Signal Generation (`utilities/wave_gen_utils.py`)

Three waveform types all return 16-bit int arrays (amplitude 32767):
- `gen_pure_wave(duration, f, sample_rate)` — single-frequency sine
- `gen_chirp(duration, f_i, f_f, sample_rate)` — linear frequency sweep
- `gen_comb(duration, f_min, num_teeth, spacing, sample_rate)` — sum of N evenly spaced sinusoids

`wav_gen.py` writes one of these to a WAV file; `scan.sh` plays it with `aplay`.

## Hardcoded Paths to Be Aware Of

- Export paths in `signal_acquisition.py` and `gps.py` are hardcoded to `~apa/Documents/FDEM/data/` (the Pi user's home directory).
- `scan.sh` references a specific rclone remote; update if the remote name changes.
- Analysis notebooks load from `data/mag.csv` and `data/gps.csv` relative to the repo root.
