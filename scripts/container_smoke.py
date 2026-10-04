"""Build and verify Compose using a separate disposable test project."""
import csv
import io
import json
import os
from pathlib import Path
import subprocess
import time
import uuid
import urllib.error
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
PROJECT = "jack-en-poy-check-" + str(os.getpid())
COMMAND = ["docker", "compose", "--project-name", PROJECT]
URL = "http://127.0.0.1:8088"

def compose(*args, check=True):
    return subprocess.run(COMMAND + list(args), cwd=ROOT, text=True, capture_output=True, check=check)

def request(path, data=None):
    payload = json.dumps(data).encode() if data is not None else None
    message = urllib.request.Request(URL + path, data=payload, headers={"Content-Type": "application/json"})
    return urllib.request.urlopen(message, timeout=12)

def wait_ready():
    deadline = time.monotonic() + 60
    while time.monotonic() < deadline:
        try:
            with request("/api/health") as response:
                if response.status == 200:
                    return
        except (urllib.error.URLError, TimeoutError):
            pass
        time.sleep(1)
    raise RuntimeError("Backend did not become ready")

def main():
    try:
        started = compose("up", "--build", "--detach", "--wait", "--wait-timeout", "180")
        print(started.stdout)
        wait_ready()
        with request("/") as response:
            assert "Jack-En-Poy AI" in response.read().decode()
            assert response.headers["X-Content-Type-Options"] == "nosniff"
            assert "frame-ancestors 'none'" in response.headers["Content-Security-Policy"]
        for service, port in [("backend", "8080"), ("ml", "8001")]:
            assert not compose("port", service, port, check=False).stdout.strip()
        try:
            request("/api/game/play", {"playerMove": "BAD"})
            raise AssertionError("Invalid move was accepted")
        except urllib.error.HTTPError as error:
            assert error.code == 400
        session = str(uuid.uuid4())
        for round_number in range(1, 6):
            with request("/api/game/play", {"sessionId": session, "playerMove": "ROCK"}) as response:
                game = json.load(response)["data"]
            assert game["round"] == round_number
            if round_number > 3:
                assert game["prediction"]["strategy"] == "ADAPTIVE"
                assert game["computerMove"] == "PAPER"
                assert game["result"] == "COMPUTER_WIN"
        compose("stop", "ml")
        with request("/api/game/play", {"sessionId": session, "playerMove": "PAPER"}) as response:
            game = json.load(response)["data"]
        assert game["prediction"]["fallbackReason"] == "service_unavailable"
        before = compose("exec", "-T", "backend", "cat", "/data/history/live-history.csv").stdout
        assert len(list(csv.DictReader(io.StringIO(before)))) == 6
        compose("restart", "backend")
        wait_ready()
        after = compose("exec", "-T", "backend", "cat", "/data/history/live-history.csv").stdout
        assert before == after
        print(json.dumps({"status": "passed", "composeBuildAndHealth": True,
                          "privateServices": True, "repetitionCounter": True,
                          "mlFailureFallback": True, "persistentHistory": True}))
    except Exception:
        print(compose("logs", "--tail", "60", check=False).stdout)
        raise
    finally:
        # This unique project owns only the volumes created by this test invocation.
        compose("down", "--volumes", "--remove-orphans", check=False)

if __name__ == "__main__":
    main()
