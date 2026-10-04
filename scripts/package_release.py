"""Package tested release outputs and write a checksum manifest."""
import hashlib
import json
from pathlib import Path
import re
import shutil
import xml.etree.ElementTree as ET
import zipfile

ROOT = Path(__file__).resolve().parents[1]
VERSION = "1.1.0"
OUTPUT = ROOT / "release"

def archive(path, inputs):
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED) as bundle:
        for source, target in inputs:
            if source.is_dir():
                for item in sorted(source.rglob("*")):
                    if item.is_file() and "__pycache__" not in item.parts:
                        bundle.write(item, str(Path(target) / item.relative_to(source)))
            else:
                bundle.write(source, target)

def main():
    metadata = json.loads((ROOT / "web/jack-en-poy-ai/package.json").read_text())
    pom = ET.parse(ROOT / "core/jack-en-poy-ai/pom.xml").getroot()
    backend_version = pom.find("{http://maven.apache.org/POM/4.0.0}version").text
    service_version = re.search(r'version="([^"]+)"', (ROOT / "ml/service.py").read_text()).group(1)
    assert metadata["version"] == backend_version == service_version == VERSION, "Release versions differ"
    jar = ROOT / f"core/jack-en-poy-ai/target/jack-en-poy-ai-{VERSION}.jar"
    demo = ROOT / "web/jack-en-poy-ai/dist-demo"
    model = ROOT / "ml/models/player-move.joblib"
    assert jar.is_file() and (demo / "index.html").is_file() and model.is_file(), "Build and train before packaging"
    OUTPUT.mkdir(exist_ok=True)
    shutil.copyfile(jar, OUTPUT / jar.name)
    archive(OUTPUT / f"jack-en-poy-browser-demo-{VERSION}.zip", [(demo, "."), (ROOT / "LICENSE", "LICENSE")])
    ml_inputs = [(ROOT / "ml/src", "src"), (ROOT / "ml/requirements-lock.txt", "requirements-lock.txt"),
                 (ROOT / "ml/README.md", "README.md"), (ROOT / "ml/tests", "tests"),
                 (ROOT / "ml/pytest.ini", "pytest.ini"), (ROOT / "ml/data/raw/game-history.csv", "data/raw/game-history.csv"),
                 (ROOT / "ml/data/processed/training-data.csv", "data/processed/training-data.csv"), (ROOT / "LICENSE", "LICENSE"),
                 (model, "models/player-move.joblib")]
    ml_inputs.extend((path, path.name) for path in sorted((ROOT / "ml").glob("*.py")))
    archive(OUTPUT / f"jack-en-poy-ml-{VERSION}.zip", ml_inputs)
    assets = [OUTPUT / jar.name, OUTPUT / f"jack-en-poy-browser-demo-{VERSION}.zip", OUTPUT / f"jack-en-poy-ml-{VERSION}.zip"]
    manifest = "".join(f"{hashlib.sha256(path.read_bytes()).hexdigest()}  {path.name}\n" for path in assets)
    (OUTPUT / "SHA256SUMS.txt").write_text(manifest, encoding="utf-8")
    print(manifest)

if __name__ == "__main__":
    main()
