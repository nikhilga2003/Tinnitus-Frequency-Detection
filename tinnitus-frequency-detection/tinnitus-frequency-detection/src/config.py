"""
config.py
----------
Test parameters for the tinnitus pitch-matching procedure.
Tune these based on your equipment and safety requirements.
"""

# Audible frequency range to search within (Hz).
# Tinnitus is most commonly reported in the higher range (4kHz-12kHz),
# but the full range is kept configurable.
FREQ_MIN_HZ = 500
FREQ_MAX_HZ = 12000

# Audio playback settings
SAMPLE_RATE = 44100
TONE_DURATION_SEC = 1.0
VOLUME = 0.3  # 0.0-1.0, keep conservative -- this plays directly to a patient's ears

# Pitch-matching search settings
MAX_COMPARISONS = 8          # number of A/B comparisons before converging
CONVERGENCE_THRESHOLD_HZ = 50  # stop early if the search window is this narrow
