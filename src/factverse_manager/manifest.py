"""Create integrity manifests for generated artifacts."""
import hashlib
import json
from pathlib import Path

def sha256_file(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()

def create_manifest(paths, manifest_path):
    entries = []
    for raw in paths:
        path = Path(raw)
        if not path.is_file():
            entries.append({"path": str(path), "exists": False, "sha256": None, "size_bytes": None})
            continue
        entries.append({"path": str(path), "exists": True, "sha256": sha256_file(path), "size_bytes": path.stat().st_size})
    target = Path(manifest_path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps({"algorithm": "sha256", "artifacts": entries}, indent=2), encoding="utf-8")
    return str(target)

def verify_manifest(manifest_path):
    data = json.loads(Path(manifest_path).read_text(encoding="utf-8"))
    issues = []
    for entry in data.get("artifacts", []):
        path = Path(entry["path"])
        if not entry.get("exists") or not path.is_file():
            issues.append(f"Missing artifact: {path}")
        elif sha256_file(path) != entry.get("sha256"):
            issues.append(f"Hash mismatch: {path}")
    return {"ok": not issues, "issues": issues, "checked": len(data.get("artifacts", []))}
