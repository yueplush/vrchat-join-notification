#!/usr/bin/env python3
"""
VRChat Join Notifier (Linux)
- Watches VRChat log files for "OnPlayerJoined" events.
- Sends a desktop notification via `notify-send` when someone joins your instance.
"""
import time, os, re, sys, subprocess
from pathlib import Path

TITLE = "VRChat"
ICON = None   # e.g. "/path/to/icon.png"
SOUND = None  # e.g. "/usr/share/sounds/freedesktop/stereo/message.oga"

JOIN_PATTERNS = [
    re.compile(r"OnPlayerJoined", re.IGNORECASE),
    re.compile(r"\bplayer\s+joined\b", re.IGNORECASE),
]
EXTRACT_PATTERNS = [
    re.compile(r"OnPlayerJoined.*?\s([^\]\)\}]+)$", re.IGNORECASE),
    re.compile(r'displayName"\s*:\s*"([^"]+)"', re.IGNORECASE),
]

HOME = Path.home()
CANDIDATE_DIRS = [
    HOME / ".local/share/Steam/steamapps/compatdata/438100/pfx/drive_c/users/steamuser/AppData/LocalLow/VRChat/VRChat",
    HOME / ".steam/steam/steamapps/compatdata/438100/pfx/drive_c/users/steamuser/AppData/LocalLow/VRChat/VRChat",
    HOME / ".var/app/com.valvesoftware.Steam/.local/share/Steam/steamapps/compatdata/438100/pfx/drive_c/users/steamuser/AppData/LocalLow/VRChat/VRChat",
    HOME / ".config/unity3d/VRChat/VRChat",
]
LOG_GLOBS = ["output_log_*.txt", "Player.log", "output_log.txt"]

def find_latest_log():
    latest, latest_mtime = None, -1
    for d in CANDIDATE_DIRS:
        if not d.exists():
            continue
        for pattern in LOG_GLOBS:
            for p in d.glob(pattern):
                try:
                    m = p.stat().st_mtime
                    if m > latest_mtime:
                        latest_mtime, latest = m, p
                except FileNotFoundError:
                    pass
    return latest

def notify(body: str):
    args = ["notify-send", TITLE, body, "-u", "normal"]
    if ICON: args.extend(["-i", ICON])
    try:
        subprocess.run(args, check=False)
    except Exception as e:
        print(f"[warn] notify-send failed: {e}", file=sys.stderr)
    if SOUND:
        try: subprocess.run(["paplay", SOUND], check=False)
        except Exception as e: print(f"[warn] paplay failed: {e}", file=sys.stderr)

def extract_name(line: str) -> str:
    for rx in EXTRACT_PATTERNS:
        m = rx.search(line)
        if m:
            name = m.group(1).strip().strip("[]{}()<>\"' ")
            return name
    return ""

def tail_f(path: Path):
    print(f"[info] Following: {path}")
    f = open(path, "r", errors="ignore", encoding="utf-8", newline="")
    f.seek(0, os.SEEK_END)
    last_check = time.time()

    while True:
        line = f.readline()
        if not line:
            if time.time() - last_check > 5:
                last_check = time.time()
                latest = find_latest_log()
                if latest and latest != path:
                    print(f"[info] Switching to newer log: {latest}")
                    f.close()
                    path = latest
                    f = open(path, "r", errors="ignore", encoding="utf-8", newline="")
                    f.seek(0, os.SEEK_END)
            time.sleep(0.5)
            continue
        for pat in JOIN_PATTERNS:
            if pat.search(line):
                name = extract_name(line)
                if name:
                    notify(f"Player joined: {name}")
                    print(f"[join] {name}")
                else:
                    notify("A player joined your instance")
                    print("[join] <unknown>")
                break

def main():
    path = find_latest_log()
    if not path:
        print("VRChat log not found.", file=sys.stderr)
        sys.exit(2)
    try:
        tail_f(path)
    except KeyboardInterrupt:
        print("\n[info] Exiting.")
        sys.exit(0)

if __name__ == "__main__":
    main()

