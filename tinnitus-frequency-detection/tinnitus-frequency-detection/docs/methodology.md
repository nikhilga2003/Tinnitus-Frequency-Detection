# Methodology

## What this project does
This tool implements a simplified **pitch-matching** procedure, a technique used in tinnitus research and audiology to estimate the dominant frequency a patient perceives as their tinnitus tone.

## How the search works
1. A test tone is played at the geometric midpoint of the current frequency search range (log scale, since pitch perception is closer to logarithmic than linear).
2. The patient reports whether their tinnitus sounds **higher**, **lower**, or the **same** as the test tone.
3. Based on the response, the search range is halved (binary search on a log scale).
4. This repeats until either:
   - the patient reports "same", or
   - the search window narrows below `CONVERGENCE_THRESHOLD_HZ`, or
   - `MAX_COMPARISONS` is reached.

This converges on an estimate in a small number of comparisons (typically 5-8) rather than sweeping through every possible frequency.

## Important limitations
- This is an **educational/prototype implementation**, not a certified clinical or diagnostic instrument.
- Real audiometric pitch-matching studies typically use calibrated equipment, control for octave confusion (patients sometimes report a frequency an octave off from their true perception), and average across multiple trials.
- Volume levels here are arbitrary (`VOLUME` in `config.py`) and are **not calibrated to safe dB SPL levels** — do not use this to play tones directly into a patient's ears without proper audiometric equipment and supervision.
- Results should be treated as a rough estimate to aid discussion with a qualified audiologist, not a diagnosis.

## Possible extensions
- Add loudness matching (in addition to pitch) to estimate tinnitus intensity
- Add octave-confusion controls (present a tone one octave above/below the candidate match)
- Export session results as a PDF report for clinical use
- Web-based version with a browser audio API instead of a CLI tool
