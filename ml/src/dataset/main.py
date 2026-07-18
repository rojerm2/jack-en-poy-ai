from pathlib import Path

from dataset_generator import generate_dataset

RAW_DATA = Path("../../data/raw/game-history.csv")
OUTPUT_DATA = Path("../../data/processed/training-data.csv")

generate_dataset(RAW_DATA, OUTPUT_DATA)