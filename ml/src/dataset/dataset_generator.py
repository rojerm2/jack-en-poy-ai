from pathlib import Path
import pandas as pd

WINDOW_SIZE = 3
MOVES = ("ROCK", "PAPER", "SCISSORS")
FEATURES = ["prev3", "prev2", "prev1"]
COLUMNS = FEATURES + ["nextMove"]


def generate_dataset(input_file: Path, output_file: Path) -> pd.DataFrame:
    """Build windows within each session, preserving chronological target order."""
    history = pd.read_csv(input_file)
    if "playerMove" not in history:
        raise ValueError("History must contain playerMove")
    if not history["playerMove"].isin(MOVES).all():
        raise ValueError("History contains an invalid player move")
    sessions = {}
    rows = []
    for record in history.to_dict("records"):
        session = record.get("sessionId", "legacy")
        if pd.isna(session):
            raise ValueError("History contains a missing sessionId")
        previous = sessions.setdefault(session, [])
        if len(previous) >= WINDOW_SIZE:
            rows.append(dict(zip(COLUMNS, previous[-WINDOW_SIZE:] + [record["playerMove"]])))
        previous.append(record["playerMove"])
    dataset = pd.DataFrame(rows, columns=COLUMNS)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    dataset.to_csv(output_file, index=False)
    return dataset
