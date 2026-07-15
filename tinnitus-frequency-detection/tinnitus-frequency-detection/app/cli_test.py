"""
cli_test.py
------------
Command-line interface to run a full tinnitus pitch-matching
session with a patient: plays test tones, collects responses,
saves the result to the database, and prints a summary report.

Run:
    cd app
    python cli_test.py
"""

import sys

sys.path.append("..")
from src import config
from src.pitch_matching import PitchMatchingSession
from src.tone_generator import play_tone
from database.db_manager import init_db, save_session


def ask_patient(test_freq: float) -> str:
    play_tone(test_freq, config.TONE_DURATION_SEC, config.SAMPLE_RATE, config.VOLUME)
    while True:
        response = input(
            f"  Test tone played at {test_freq:.0f} Hz. "
            f"Is your tinnitus higher, lower, or the same? [h/l/s]: "
        ).strip().lower()
        if response in ("h", "higher"):
            return "higher"
        elif response in ("l", "lower"):
            return "lower"
        elif response in ("s", "same"):
            return "same"
        print("  Please enter 'h', 'l', or 's'.")


def main():
    print("=== Tinnitus Frequency Matching Test ===")
    patient_name = input("Patient name: ").strip()

    session = PitchMatchingSession(
        freq_min_hz=config.FREQ_MIN_HZ,
        freq_max_hz=config.FREQ_MAX_HZ,
        max_comparisons=config.MAX_COMPARISONS,
        convergence_threshold_hz=config.CONVERGENCE_THRESHOLD_HZ,
    )

    result = session.run(ask_patient)

    print("\n--- Result ---")
    print(f"Estimated tinnitus frequency: {result['estimated_frequency_hz']} Hz")
    print(f"Comparisons taken: {result['steps_taken']}")
    print(f"Converged: {'Yes' if result['converged'] else 'No (reached max comparisons)'}")

    conn = init_db()
    session_id = save_session(conn, patient_name, result)
    print(f"\nSaved as session #{session_id}.")


if __name__ == "__main__":
    main()
