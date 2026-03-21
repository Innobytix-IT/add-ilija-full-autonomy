"""
Analysiert eine Zeichenkette von 'Ziel abgeschlossen'-Einträgen, um die Erfolgsraten nach Zieltyp zu bestimmen und eine Zusammenfassung zu liefern.

Auto-generiert durch skill_erstellen
Skill-Name: analyse_zielabschluesse
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
import re

def analyse_zielabschluesse(memory_text: str) -> str:
    results = {}
    entries = memory_text.split("Ziel abgeschlossen ")
    for entry in entries:
        if not entry.strip():
            continue
        
        type_match = re.search(r"\[(.*?)\]", entry)
        goal_type = type_match.group(1) if type_match else "unknown"

        score_match = re.search(r"Score: ([\\d.]+)/10", entry)
        score = float(score_match.group(1)) if score_match else 0.0

        is_successful = score >= 5.0

        if goal_type not in results:
            results[goal_type] = {"successful": 0, "unsuccessful": 0, "total_score": 0, "count": 0}
        
        if is_successful:
            results[goal_type]["successful"] += 1
        else:
            results[goal_type]["unsuccessful"] += 1
        results[goal_type]["total_score"] += score
        results[goal_type]["count"] += 1
            
    summary = "Analyse der Zielabschlüsse:\n"
    if not results:
        summary += "Keine Zielabschlüsse gefunden oder analysierbar."
        return summary

    for goal_type, data in results.items():
        total = data["successful"] + data["unsuccessful"]
        success_rate = (data["successful"] / total) * 100 if total > 0 else 0
        avg_score = data["total_score"] / data["count"] if data["count"] > 0 else 0
        summary += (f"- Typ '{goal_type}': {data['successful']} erfolgreich, {data['unsuccessful']} nicht erfolgreich "
                    f"({success_rate:.2f}% Erfolgsquote, Durchschnittsscore: {avg_score:.2f}/10)\n")
    
    most_successful_type = None
    highest_success_rate = -1.0
    for goal_type, data in results.items():
        total = data["successful"] + data["unsuccessful"]
        success_rate = (data["successful"] / total) * 100 if total > 0 else 0
        if success_rate > highest_success_rate:
            highest_success_rate = success_rate
            most_successful_type = goal_type
        elif success_rate == highest_success_rate and most_successful_type is not None:
            if data["successful"] > results[most_successful_type]["successful"]:
                most_successful_type = goal_type
            elif data["successful"] == results[most_successful_type]["successful"]:
                pass

    if most_successful_type:
        summary += f"\nDer am häufigsten erfolgreich abgeschlossene Zieltyp ist wahrscheinlich '{most_successful_type}' mit einer Erfolgsquote von {highest_success_rate:.2f}%."
    
    return summary

# Registrierung für den SkillManager
AVAILABLE_SKILLS = [analyse_zielabschluesse]
