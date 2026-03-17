"""
Analysiert eine Log-Datei auf Fehler, häufige Zeilen und spezifische Keywords. Erkennt Muster und zählt Vorkommen.

Auto-generiert durch skill_erstellen
Skill-Name: logdateien_analysieren
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
import os
from collections import Counter

def logdateien_analysieren(file_path: str, keyword: str = None, top_n: int = 5):
    """
    Analysiert eine Log-Datei auf Fehler, häufige Zeilen und spezifische Keywords.

    Args:
        file_path (str): Der Pfad zur Log-Datei.
        keyword (str, optional): Ein optionales Keyword, nach dem gesucht werden soll.
        top_n (int, optional): Die Anzahl der häufigsten Zeilen, die zurückgegeben werden sollen. Standard ist 5.

    Returns:
        dict: Ein Dictionary mit Analyseergebnissen, inklusive 'error' bei Problemen.
    """
    if not os.path.exists(file_path):
        return {"error": f"Datei nicht gefunden: {file_path}"}
    if not os.path.isfile(file_path):
        return {"error": f"Pfad ist keine Datei: {file_path}"}

    log_lines = []
    error_count = 0
    keyword_occurrences = []

    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                log_lines.append(line)

                if "ERROR" in line.upper():
                    error_count += 1
                if keyword and keyword.lower() in line.lower():
                    keyword_occurrences.append(line)

        if not log_lines:
            return {"total_lines": 0, "error_count": 0, "most_common_lines": [], "message": "Die Log-Datei ist leer oder enthält keine verarbeitbaren Zeilen."}

        line_counts = Counter(log_lines)
        most_common_lines = line_counts.most_common(top_n)

        result = {
            "total_lines": len(log_lines),
            "error_count": error_count,
            "most_common_lines": most_common_lines
        }
        if keyword:
            result["keyword_search_results"] = keyword_occurrences
            result["keyword_count"] = len(keyword_occurrences)

        return result

    except PermissionError:
        return {"error": f"Keine Berechtigung zum Lesen der Datei: {file_path}"}
    except Exception as e:
        return {"error": f"Fehler beim Lesen oder Analysieren der Datei: {e}"}

# Registrierung für den SkillManager
AVAILABLE_SKILLS = [logdateien_analysieren]
