#!/usr/bin/env python3
"""Phase 1 CLI entry point for the AEO Validator agent workflow."""

from __future__ import annotations

import argparse
import json
import sys

from dotenv import load_dotenv

from workflow import analyze_url


def main() -> int:
    load_dotenv()

    parser = argparse.ArgumentParser(description="Analyze a URL for AI search readiness.")
    parser.add_argument(
        "url",
        nargs="?",
        default="https://example.com",
        help="Target website URL (default: https://example.com)",
    )
    args = parser.parse_args()

    print(f"Analyzing {args.url} ...")
    result = analyze_url(args.url)
    print(json.dumps(result.model_dump(), indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
