import json
import os

TIMESTAMP_FILE = "/opt/airflow/last_timestamp.json"  # Adjust path as needed


def load_last_timestamp(key: str):
    """Loads the last processed timestamp for measures from a file."""
    try:
        with open(TIMESTAMP_FILE, "r") as f:
            data = json.load(f)
            return data.get(key)
    except (FileNotFoundError, json.JSONDecodeError):
        return None


def save_last_timestamp(timestamp, key: str):
    """Saves the last processed timestamp for measures to a file without overwriting other keys."""
    # Check if the file exists
    if os.path.exists(TIMESTAMP_FILE):
        with open(TIMESTAMP_FILE, "r") as f:
            data = json.load(f)
    else:
        data = {}
    data[key] = timestamp
    with open(TIMESTAMP_FILE, "w") as f:
        json.dump(data, f, indent=4)
