import argparse
import json
from pathlib import Path

from retrain import atomic_json
from src.comparison import compare_models
from src.training import DEFAULT_DATA, ROOT


def main():
    parser = argparse.ArgumentParser(description="Compare models on chronological folds, then report final holdout scores")
    parser.add_argument("--dataset", type=Path, default=DEFAULT_DATA)
    parser.add_argument("--report", type=Path, default=ROOT / "reports/comparison.json")
    args = parser.parse_args()
    try:
        report = compare_models(args.dataset)
        atomic_json(report, args.report)
    except (ValueError, OSError) as error:
        parser.exit(2, f"Comparison failed: {error}\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
