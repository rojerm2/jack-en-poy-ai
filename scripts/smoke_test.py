"""Run actual Java/Python processes on temporary loopback ports and data files."""
import argparse
import json
import os
from pathlib import Path
import socket
import subprocess
import sys
import tempfile
import time
import uuid

import httpx

ROOT = Path(__file__).resolve().parents[1]
ML = ROOT / "ml"
sys.path.insert(0, str(ML))
from analytics import summarize
from src.dataset.dataset_generator import generate_dataset
from src.prediction import Predictor
from src.training import train


def unused_port():
    with socket.socket() as listener:
        listener.bind(("127.0.0.1", 0))
        return listener.getsockname()[1]


def stop(process):
    if process is not None and process.poll() is None:
        process.terminate()
        try:
            process.wait(timeout=10)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait(timeout=5)


def ready(client, url, process):
    deadline = time.monotonic() + 45
    while time.monotonic() < deadline:
        if process.poll() is not None:
            raise RuntimeError("Service exited before readiness")
        try:
            if client.get(url).status_code == 200:
                return
        except httpx.RequestError:
            pass
        time.sleep(.2)
    raise RuntimeError(f"Readiness timed out: {url}")


def play(client, api, session, move):
    response = client.post(api + "/api/game/play", json={"sessionId": session, "playerMove": move})
    response.raise_for_status()
    result = response.json()
    assert result["success"] is True
    game = result["data"]
    assert game["sessionId"] == session
    assert game["analytics"]["totalRounds"] == game["round"]
    assert sum(game["analytics"][key] for key in ["playerWins", "computerWins", "draws"]) == game["round"]
    return game


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--jar", type=Path, default=ROOT / "core/jack-en-poy-ai/target/jack-en-poy-ai-1.0.0.jar")
    args = parser.parse_args()
    jar = args.jar.resolve()
    if not jar.is_file():
        parser.error("Package the backend with the Maven wrapper before running this test")

    processes = []
    log_handles = []
    with tempfile.TemporaryDirectory(prefix="jack-en-poy-smoke-") as temporary:
        workspace = Path(temporary)
        model = workspace / "model.joblib"
        dataset = workspace / "dataset.csv"
        history = workspace / "live.csv"
        generate_dataset(ML / "data/raw/game-history.csv", dataset)
        train(dataset, model)
        ports = {unused_port() for _ in range(2)}
        while len(ports) < 2:
            ports.add(unused_port())
        backend_port, python_port = sorted(ports)
        api = f"http://127.0.0.1:{backend_port}"
        prediction_api = f"http://127.0.0.1:{python_port}"
        environment = dict(os.environ, SERVER_PORT=str(backend_port), SERVER_ADDRESS="127.0.0.1",
                           ML_SERVICE_URL=prediction_api, ML_TIMEOUT_MS="600", ML_ENABLED="true",
                           GAME_HISTORY_PATH=str(history), MODEL_PATH=str(model))
        flags = subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0
        def launch(command, directory, name):
            log = (workspace / f"{name}.log").open("w", encoding="utf-8")
            log_handles.append(log)
            process = subprocess.Popen(command, cwd=directory, env=environment, stdout=log, stderr=subprocess.STDOUT, creationflags=flags)
            processes.append(process)
            return process

        try:
            with httpx.Client(timeout=3, trust_env=False) as client:
                backend = launch(["java", "-jar", str(jar)], ROOT / "core/jack-en-poy-ai", "backend")
                ready(client, api + "/api/game/analytics?sessionId=" + str(uuid.uuid4()), backend)
                invalid = client.post(api + "/api/game/play", json={"playerMove": "INVALID"})
                assert invalid.status_code == 400
                offline_session = str(uuid.uuid4())
                sequence = ["ROCK", "PAPER", "SCISSORS", "ROCK"]
                for move in sequence:
                    offline = play(client, api, offline_session, move)
                    assert offline["prediction"]["strategy"] == "RANDOM"
                assert offline["prediction"]["fallbackReason"] == "service_unavailable"

                python = launch([sys.executable, "-m", "uvicorn", "service:app", "--host", "127.0.0.1", "--port", str(python_port)], ML, "python")
                ready(client, prediction_api + "/health", python)
                online_session = str(uuid.uuid4())
                for index, move in enumerate(sequence):
                    online = play(client, api, online_session, move)
                    assert online["prediction"]["strategy"] == ("RANDOM" if index < 3 else "ML")
                expected = Predictor(model).predict(sequence[:3])["predictedMove"]
                assert online["prediction"]["predictedMove"] == expected
                assert online["computerMove"] == {"ROCK": "PAPER", "PAPER": "SCISSORS", "SCISSORS": "ROCK"}[expected]
                assert online["analytics"]["mlRounds"] == 1
                snapshot = client.get(api + "/api/game/analytics", params={"sessionId": online_session}).json()["data"]
                assert snapshot == online["analytics"]
                for move, counter in {"ROCK": "PAPER", "PAPER": "SCISSORS", "SCISSORS": "ROCK"}.items():
                    repeated_session = str(uuid.uuid4())
                    for index in range(5):
                        repeated = play(client, api, repeated_session, move)
                        if index < 3:
                            assert repeated["prediction"]["strategy"] == "RANDOM"
                        else:
                            assert repeated["prediction"]["strategy"] == "ADAPTIVE"
                            assert repeated["prediction"]["predictedMove"] == move
                            assert repeated["prediction"]["confidence"] is None
                            assert repeated["computerMove"] == counter
                            assert repeated["result"] == "COMPUTER_WIN"
                    assert repeated["analytics"]["adaptiveRounds"] == 2
                    assert repeated["analytics"]["adaptiveWinRate"] == 1
                    assert repeated["analytics"]["randomRounds"] == 3
                    assert repeated["analytics"]["mlRounds"] == 0
                stop(python)
                failed = play(client, api, online_session, "PAPER")
                assert failed["prediction"]["strategy"] == "RANDOM"
                assert failed["prediction"]["fallbackReason"] == "service_unavailable"
                assert failed["analytics"]["randomRounds"] == 4

                persisted = summarize(history)
                assert persisted["totalRounds"] == 24
                assert persisted["mlPredictions"] == 1
                assert persisted["adaptivePredictions"] == 6
                assert persisted["adaptivePredictionAccuracy"] == 1
                print(json.dumps({"status": "passed", "withoutPython": True, "withPython": True,
                                  "serviceFailureFallback": True, "completedHistoryPrediction": True,
                                  "authoritativeScoresAndAnalytics": True, "repeatedMovesCountered": True, "recordedRounds": 24}, indent=2))
        except Exception:
            for process in reversed(processes):
                stop(process)
            for log in log_handles:
                log.close()
            for file in workspace.glob("*.log"):
                print(f"{file.name}:\n" + "\n".join(file.read_text(encoding="utf-8", errors="replace").splitlines()[-35:]), file=sys.stderr)
            raise
        finally:
            for process in reversed(processes):
                stop(process)
            for log in log_handles:
                log.close()


if __name__ == "__main__":
    main()
