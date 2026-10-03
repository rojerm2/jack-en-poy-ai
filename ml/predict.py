import argparse
import json
from pathlib import Path

from src.prediction import Predictor
from src.training import DEFAULT_MODEL


def main():
    parser = argparse.ArgumentParser(description="Predict from completed moves, oldest to newest")
    parser.add_argument("moves", nargs="+", choices=["ROCK", "PAPER", "SCISSORS"])
    parser.add_argument("--model", type=Path, default=DEFAULT_MODEL)
    args = parser.parse_args()
    print(json.dumps(Predictor(args.model).predict(args.moves), indent=2))


if __name__ == "__main__":
    main()
