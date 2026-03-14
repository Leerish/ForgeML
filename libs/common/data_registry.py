from __future__ import annotations
import json, os, hashlib, time
from dataclasses import dataclass, asdict
from typing import Dict, Any, Optional, List
from .config import settings

def sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

@dataclass
class DatasetManifest:
    dataset_name: str
    version: str
    created_at: float
    s3_uri: str
    sha256: str
    rows: Optional[int] = None
    cols: Optional[int] = None
    schema: Optional[Dict[str, str]] = None
    metadata: Optional[Dict[str, Any]] = None

def _registry_path(dataset_name: str) -> str:
    os.makedirs(settings.REGISTRY_DIR, exist_ok=True)
    return os.path.join(settings.REGISTRY_DIR, f"{dataset_name}.jsonl")

def append_manifest(m: DatasetManifest) -> None:
    path = _registry_path(m.dataset_name)
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(asdict(m)) + "\n")

def list_versions(dataset_name: str) -> List[Dict[str, Any]]:
    path = _registry_path(dataset_name)
    if not os.path.exists(path):
        return []
    out = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            out.append(json.loads(line))
    return out

def next_version(dataset_name: str) -> str:
    versions = list_versions(dataset_name)
    return f"v{len(versions) + 1:03d}"

def make_manifest(
    dataset_name: str,
    s3_uri: str,
    local_path: str,
    rows: Optional[int] = None,
    cols: Optional[int] = None,
    schema: Optional[Dict[str, str]] = None,
    metadata: Optional[Dict[str, Any]] = None,
) -> DatasetManifest:
    return DatasetManifest(
        dataset_name=dataset_name,
        version=next_version(dataset_name),
        created_at=time.time(),
        s3_uri=s3_uri,
        sha256=sha256_file(local_path),
        rows=rows,
        cols=cols,
        schema=schema,
        metadata=metadata or {},
    )