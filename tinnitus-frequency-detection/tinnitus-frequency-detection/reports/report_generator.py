"""
report_generator.py
----------------------
Generates a simple text summary report from stored sessions --
useful for handing a printed/exported summary to a clinician.

Usage:
    python report_generator.py --patient "Jane Doe"
    python report_generator.py --all
"""

import argparse
import sys

sys.path.append("..")
from database.db_manager import init_db, get_all_sessions, get_patient_history


def print_report(sessions: list) -> None:
    if not sessions:
        print("No sessions found.")
        return

    for s in sessions:
        print(f"Session #{s['session_id']} — {s['patient_name']}")
        print(f"  Estimated frequency : {s['estimated_frequency_hz']} Hz")
        print(f"  Comparisons taken   : {s['steps_taken']}")
        print(f"  Converged           : {'Yes' if s['converged'] else 'No'}")
        print(f"  Recorded at         : {s['recorded_at']}")
        if s.get("notes"):
            print(f"  Notes               : {s['notes']}")
        print("-" * 40)


def main():
    parser = argparse.ArgumentParser(description="Generate a report of tinnitus test sessions.")
    parser.add_argument("--patient", help="Filter by patient name")
    parser.add_argument("--all", action="store_true", help="Show all sessions")
    parser.add_argument("--db", default="../data/sessions.db")
    args = parser.parse_args()

    conn = init_db(args.db)

    if args.patient:
        sessions = get_patient_history(conn, args.patient)
    else:
        sessions = get_all_sessions(conn)

    print_report(sessions)


if __name__ == "__main__":
    main()
