import argparse
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from src.dataset.dataset_generator import generate_dataset


def main():
    parser = argparse.ArgumentParser(description="Generate three-move training windows")
    parser.add_argument("--input", type=Path, default=ROOT / "data/raw/game-history.csv")
    parser.add_argument("--output", type=Path, default=ROOT / "data/processed/training-data.csv")
    args = parser.parse_args()
    dataset = generate_dataset(args.input, args.output)
    print(f"Generated {len(dataset)} training samples: {args.output}")


if __name__ == "__main__":
    main()
