# Tinnitus Frequency Detection

A system that identifies the specific sound frequency perceived by tinnitus patients, using an interactive pitch-matching test, to aid diagnosis and discussion with an audiologist.

## Overview
Tinnitus is often described by patients only in vague terms ("a ringing" or "a buzzing"). Pitch-matching is a technique that narrows this down to an estimated frequency by playing test tones and asking the patient whether their perceived tone is higher, lower, or the same. This project implements that procedure as a simple, repeatable, and loggable test.

## Features
- Binary-search pitch-matching algorithm on a log-frequency scale (converges in ~5-8 comparisons instead of a linear sweep)
- Pure tone generation with fade-in/out to avoid audible clicks
- Interactive CLI test session
- SQLite database to store and review session history per patient
- Report generator to print/export a patient's test history

## Tech Stack
| Layer | Technology |
|---|---|
| Language | Python |
| Audio | NumPy (tone synthesis), sounddevice (playback) |
| Database | SQLite |
| Interface | CLI (interactive prompts) |

## Repository Structure
```
tinnitus-frequency-detection/
├── src/
│   ├── config.py            # Test parameters (frequency range, volume, etc.)
│   ├── tone_generator.py    # Generates & plays pure tone audio
│   └── pitch_matching.py    # Core binary-search matching algorithm
├── app/
│   └── cli_test.py          # Interactive test session (entry point)
├── database/
│   └── db_manager.py        # SQLite storage for patient sessions
├── reports/
│   └── report_generator.py  # Prints/exports session history
├── data/
│   └── sessions.db          # Created at runtime (gitignored)
├── docs/
│   └── methodology.md       # How the algorithm works + limitations
├── requirements.txt
├── .gitignore
├── README.md
└── LICENSE
```

## How It Works
1. `cli_test.py` starts a session and asks for the patient's name.
2. `pitch_matching.py` picks a test frequency (starting at the midpoint of the configured range) and asks `tone_generator.py` to play it.
3. The patient responds higher / lower / same via the CLI.
4. The search range narrows each round until it converges or hits the comparison limit.
5. The final estimated frequency is saved to SQLite via `db_manager.py`.
6. `report_generator.py` can print a summary of any patient's session history at any time.

## Setup
```bash
pip install -r requirements.txt
cd app
python cli_test.py
```

To view results later:
```bash
cd reports
python report_generator.py --all
python report_generator.py --patient "Jane Doe"
```

## Verified Behavior
The search algorithm was tested against a simulated patient with a known "true" tinnitus frequency of 6000 Hz — it converged to an estimate of 5987.7 Hz in 5 comparisons.

## Important Limitations
This is an educational/prototype implementation, **not a certified clinical or diagnostic instrument**. Volume levels are not calibrated to safe dB SPL standards. See [docs/methodology.md](docs/methodology.md) for full details and appropriate use.

## Future Improvements
- Add octave-confusion controls (common failure mode in real pitch-matching tests)
- Add loudness matching alongside pitch matching
- Web-based version using the browser's Web Audio API
- PDF export of session reports for clinicians

## License
MIT — see [LICENSE](LICENSE)
