"""
Monitors a specified file system path for changes for a given duration.

Auto-generiert durch skill_erstellen
Skill-Name: filesystem_monitor
"""

# Standard-Imports für Skills
import random
import time
import math
import datetime
import os
import subprocess
import json
from typing import Optional, List, Dict, Any

# Haupt-Skill-Code
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os

class ChangeHandler(FileSystemEventHandler):
    def __init__(self, changes_list):
        super().__init__()
        self.changes = changes_list

    def on_modified(self, event):
        self.changes.append({"type": "modified", "path": event.src_path, "is_directory": event.is_directory})

    def on_created(self, event):
        self.changes.append({"type": "created", "path": event.src_path, "is_directory": event.is_directory})

    def on_deleted(self, event):
        self.changes.append({"type": "deleted", "path": event.src_path, "is_directory": event.is_directory})

    def on_moved(self, event):
        self.changes.append({"type": "moved", "src_path": event.src_path, "dest_path": event.dest_path, "is_directory": event.is_directory})

def filesystem_monitor(path_to_monitor: str, duration_seconds: int = 5) -> list:
    """
    Monitors a specified file system path for changes for a given duration.

    Args:
        path_to_monitor (str): The path to the directory or file to monitor.
        duration_seconds (int): How long to monitor in seconds (default: 5).

    Returns:
        list: A list of dictionaries, each describing a detected file system change.
    """
    if not os.path.exists(path_to_monitor):
        return [{"error": f"Path does not exist: {path_to_monitor}"}]

    changes_detected = []
    event_handler = ChangeHandler(changes_detected)
    observer = Observer()
    observer.schedule(event_handler, path_to_monitor, recursive=True)
    observer.start()

    try:
        time.sleep(duration_seconds)
    except KeyboardInterrupt:
        pass
    finally:
        observer.stop()
        observer.join()

    return changes_detected


# Registrierung für den SkillManager
AVAILABLE_SKILLS = [filesystem_monitor]
