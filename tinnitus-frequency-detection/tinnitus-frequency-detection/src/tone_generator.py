"""
tone_generator.py
-------------------
Generates and plays pure sine-wave tones at a given frequency.
Used to present comparison tones during the pitch-matching test.

Requires: numpy, sounddevice
    pip install numpy sounddevice
"""

import numpy as np

try:
    import sounddevice as sd
    AUDIO_AVAILABLE = True
except OSError:
    # sounddevice needs a real audio backend (PortAudio) -- unavailable
    # in some headless/CI environments. Tone math still works without it.
    AUDIO_AVAILABLE = False


def generate_tone(frequency_hz: float, duration_sec: float, sample_rate: int, volume: float) -> np.ndarray:
    """Generates a pure sine wave with a short fade-in/out to avoid audible clicks."""
    t = np.linspace(0, duration_sec, int(sample_rate * duration_sec), endpoint=False)
    tone = volume * np.sin(2 * np.pi * frequency_hz * t)

    # 10ms fade in/out to prevent clicking artifacts at tone start/end
    fade_samples = int(0.01 * sample_rate)
    fade_samples = min(fade_samples, len(tone) // 2)
    fade_in = np.linspace(0, 1, fade_samples)
    fade_out = np.linspace(1, 0, fade_samples)
    tone[:fade_samples] *= fade_in
    tone[-fade_samples:] *= fade_out

    return tone.astype(np.float32)


def play_tone(frequency_hz: float, duration_sec: float, sample_rate: int, volume: float) -> None:
    """Plays a tone through the default audio output device."""
    if not AUDIO_AVAILABLE:
        print(f"[audio unavailable] Would play {frequency_hz:.1f} Hz for {duration_sec}s")
        return

    tone = generate_tone(frequency_hz, duration_sec, sample_rate, volume)
    sd.play(tone, sample_rate)
    sd.wait()
