from __future__ import annotations

import json
import os
import time
from typing import Dict, Any


def write_validation_report(report: Dict[str, Any], dataset_name: str) -> str:
    os.makedirs("./reports", exist_ok=True)
    ts = int(time.time())
    path = f"./reports/{dataset_name}_validation_{ts}.json"

    with open(path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    return path