"""Einstiegspunkt für den kompletten Export-Vorgang."""

import argparse

from config import JSON_OUTPUT_PATH, TEST_JSON_OUTPUT_PATH
from base import run_jobs
from jobs import EXPORT_JOBS


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Exportiert alle Rankings/Stats als JSON."
    )
    parser.add_argument(
        "--test", action="store_true", help="Export in tests/data/ statt docs/data/"
    )
    parser.add_argument("--quiet", action="store_true", help="Keine Konsolenausgabe")
    args = parser.parse_args()

    output_dir = TEST_JSON_OUTPUT_PATH if args.test else JSON_OUTPUT_PATH
    print(f"Exportiere nach: {output_dir}\n")

    run_jobs(EXPORT_JOBS, output_dir, verbose=not args.quiet)

    print("\nFertig!")


if __name__ == "__main__":
    main()
