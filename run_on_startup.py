from datetime import date
from pathlib import Path
import socket
import subprocess
import sys
import time

BASE_DIR = Path(__file__).resolve().parent
APP_DIR = BASE_DIR / "app"
AGENT_SCRIPT = APP_DIR / "agent.py"
LOCK_FILE = BASE_DIR / ".last_run.txt"


def wait_for_internet(timeout_seconds: int = 300) -> bool:
    """Polls until internet connectivity is established or timeout expires."""
    start = time.time()
    while time.time() - start < timeout_seconds:
        try:
            # Connect to Cloudflare DNS
            socket.create_connection(("1.1.1.1", 53), timeout=3)
            return True
        except OSError:
            time.sleep(5)
    return False


def already_ran_today() -> bool:
    if LOCK_FILE.exists():
        return LOCK_FILE.read_text(encoding="utf-8").strip() == str(date.today())
    return False


def mark_ran_today():
    LOCK_FILE.write_text(str(date.today()), encoding="utf-8")


if __name__ == "__main__":
    if already_ran_today():
        sys.exit(0)

    if wait_for_internet():
        subprocess.run(
            [sys.executable, str(AGENT_SCRIPT)],
            cwd=str(APP_DIR),
            check=True,
        )
        mark_ran_today()
