import os
import time
import psutil

from config import ACCESS_LOG

def parse_traffic_log(log_file: str = ACCESS_LOG) -> dict:
    stats = {}
    if not os.path.isfile(log_file):
        return stats
    with open(log_file, "r") as f:
        for line in f:
            parts = line.split()
            if len(parts) < 8 or parts[7] == "-":
                continue
            try:
                b = int(parts[4])
            except:
                continue
            stats[parts[7]] = stats.get(parts[7], 0) + b
    return stats


def format_uptime() -> str:
    delta = time.time() - psutil.boot_time()
    days = int(delta // 86400)
    hours = int((delta % 86400) // 3600)
    mins = int((delta % 3600) // 60)
    return f"{days}d {hours}h {mins}m"

def format_bytes(b: int) -> str:
    return f"{b / 1024 / 1024:.2f} MB"