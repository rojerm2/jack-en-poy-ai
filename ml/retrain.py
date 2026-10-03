import argparse
from contextlib import contextmanager
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import shutil
import tempfile
import uuid

import joblib

from src.dataset.dataset_generator import generate_dataset
from src.prediction import Predictor
from src.training import DEFAULT_MODEL, ROOT, atomic_dump, train


@contextmanager
def model_lock(output):
    output.parent.mkdir(parents=True, exist_ok=True)
    lock = output.with_suffix(".lock")
    try:
        descriptor = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    except FileExistsError as error:
        raise RuntimeError("Another training operation holds the model lock") from error
    try:
        os.close(descriptor)
        yield
    finally:
        lock.unlink(missing_ok=True)


def archive_model(output):
    if not output.exists():
        return None
    archive = output.parent / "archive" / f"{datetime.now(timezone.utc):%Y%m%dT%H%M%S}-{uuid.uuid4().hex[:8]}.joblib"
    archive.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(output, archive)
    return str(archive)


def atomic_json(value, path):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(dir=path.parent, suffix=".json")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as stream:
            json.dump(value, stream, indent=2)
            stream.write("\n")
        os.replace(temporary, path)
    finally:
        Path(temporary).unlink(missing_ok=True)


def retrain(history, output=DEFAULT_MODEL, report=None):
    history, output = Path(history), Path(output)
    report = Path(report or ROOT / "reports/retraining.json")
    if len({history.resolve(), output.resolve(), report.resolve()}) != 3:
        raise ValueError("History, model and report must be separate files")
    with model_lock(output), tempfile.TemporaryDirectory() as temporary:
        workspace = Path(temporary)
        # Read once so a round appended during training cannot change this dataset.
        snapshot = history.read_bytes()
        raw = workspace / "history.csv"
        raw.write_bytes(snapshot)
        dataset = workspace / "dataset.csv"
        generated = generate_dataset(raw, dataset)
        candidate = workspace / "candidate.joblib"
        metadata = train(dataset, candidate)
        Predictor(candidate).predict(["ROCK", "PAPER", "SCISSORS"])
        artifact = joblib.load(candidate)
        artifact["historySha256"] = hashlib.sha256(snapshot).hexdigest()
        artifact["generatedSamples"] = len(generated)
        previous = archive_model(output)
        atomic_dump(artifact, output)
        metadata.update({"historySha256": artifact["historySha256"], "generatedSamples": len(generated), "previousModelArchive": previous})
        atomic_json(metadata, report)
        return metadata


def rollback(archive, output=DEFAULT_MODEL):
    archive, output = Path(archive), Path(output)
    with model_lock(output):
        validated = Predictor(archive)
        previous = archive_model(output)
        atomic_dump(validated.artifact, output)
        return {"modelVersion": validated.artifact["modelVersion"], "previousModelArchive": previous}


def main():
    parser = argparse.ArgumentParser(description="Retrain from a frozen history snapshot or restore a locally archived model")
    inputs = parser.add_mutually_exclusive_group()
    inputs.add_argument("--history", type=Path, default=ROOT / "data/raw/live-history.csv")
    inputs.add_argument("--rollback", type=Path)
    parser.add_argument("--output", type=Path, default=DEFAULT_MODEL)
    parser.add_argument("--report", type=Path, default=ROOT / "reports/retraining.json")
    args = parser.parse_args()
    try:
        result = rollback(args.rollback, args.output) if args.rollback else retrain(args.history, args.output, args.report)
    except (ValueError, RuntimeError, OSError) as error:
        parser.exit(2, f"Retraining failed: {error}\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
