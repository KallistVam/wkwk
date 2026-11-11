import json
from pathlib import Path


class ProcessManager:
    """Stores simulated processes in a JSON file; these are not Windows processes."""

    VALID_STATUSES = {"Ready", "Running", "Terminated"}

    def __init__(self, database=None):
        project_root = Path(__file__).resolve().parent.parent
        self.database = Path(database) if database else project_root / "data" / "processes.json"
        self.database.parent.mkdir(parents=True, exist_ok=True)
        self.processes = []
        self.load_processes()

    def load_processes(self):
        if not self.database.exists():
            self.save_processes()
            return
        try:
            loaded = json.loads(self.database.read_text(encoding="utf-8"))
            if not isinstance(loaded, list):
                loaded = []
            self.processes = [
                p for p in loaded
                if isinstance(p, dict)
                and {"pid", "name", "status", "priority"} <= p.keys()
                and isinstance(p["pid"], int)
                and isinstance(p["name"], str)
                and p["status"] in self.VALID_STATUSES
                and isinstance(p["priority"], int)
            ]
        except (OSError, json.JSONDecodeError):
            self.processes = []

    def save_processes(self):
        self.database.write_text(
            json.dumps(self.processes, indent=4, ensure_ascii=False),
            encoding="utf-8"
        )

    def create_process(self, name, priority=1):
        if not isinstance(name, str) or not name.strip():
            return None
        try:
            priority = int(priority)
        except (TypeError, ValueError):
            return None
        if not 1 <= priority <= 10:
            return None

        pid = max((p["pid"] for p in self.processes), default=1000) + 1
        process = {
            "pid": pid,
            "name": name.strip(),
            "status": "Ready",
            "priority": priority,
        }
        self.processes.append(process)
        self.save_processes()
        return process.copy()

    def run_process(self, pid):
        for process in self.processes:
            if process["pid"] == pid and process["status"] == "Ready":
                process["status"] = "Running"
                self.save_processes()
                return True
        return False

    def stop_process(self, pid):
        for process in self.processes:
            if process["pid"] == pid and process["status"] == "Running":
                process["status"] = "Terminated"
                self.save_processes()
                return True
        return False

    def delete_process(self, pid):
        original_count = len(self.processes)
        self.processes = [p for p in self.processes if p["pid"] != pid]
        if len(self.processes) == original_count:
            return False
        self.save_processes()
        return True

    def get_processes(self):
        return [p.copy() for p in self.processes]
