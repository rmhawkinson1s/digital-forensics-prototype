import json
import datetime
import os
from typing import Any, Dict, List

LOG_FILE = "artifacts/audit_log.json"

def _load_logs() -> List[Dict[str, Any]]:
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def log_action(action: str, details: Any) -> None:
    """Append a structured audit event (FR-15)."""
    os.makedirs("artifacts", exist_ok=True)

    log_entry = {
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
        "action": action,
        "details": details
    }

    logs = _load_logs()
    logs.append(log_entry)

    with open(LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(logs, f, indent=2, ensure_ascii=False)

    print(f"Logged: {action}")
