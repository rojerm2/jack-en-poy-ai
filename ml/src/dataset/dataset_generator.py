from pathlib import Path
import pandas as pd

WINDOW_SIZE = 3

def generate_dataset(input_file: Path, output_file: Path) -> None:
    """
    Convert raw gameplay history into a supervised learning dataset.
    """

    history = pd.read_csv(input_file)

    player_moves = history["playerMove"].tolist()

    rows = []

    for i in range(WINDOW_SIZE, len(player_moves)):

        rows.append(
            {
                "prev3": player_moves[i - 3],
                "prev2": player_moves[i - 2],
                "prev1": player_moves[i - 1],
                "nextMove": player_moves[i],
            }
        )

    dataset = pd.DataFrame(rows)

    output_file.parent.mkdir(parents=True, exist_ok=True)

    dataset.to_csv(output_file, index=False)

    print(f"Generated {len(dataset)} training samples.")