"""
Analysiert die Performance der vom System ausgeführten Skills und Ziele aus dem Langzeitgedächtnis und erstellt einen textuellen Performance-Report in einer Datei.

Auto-generiert durch skill_erstellen
Skill-Name: analyse_und_visualisiere_skill_performance
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
def analyse_und_visualisiere_skill_performance():
    # 1. Alle Einträge zu Zielausführungen aus dem Langzeitgedächtnis abrufen.
    #    Es wird angenommen, dass wissen_abrufen eine formatierte Zeichenkette der gefundenen Einträge zurückgibt.
    all_goal_memories = wissen_abrufen(suchbegriff="Ziel ausgeführt")
    
    report_content = ""
    if not all_goal_memories or "Keine Infos gefunden" in all_goal_memories:
        report_content = "Keine vergangenen Zielausführungen im Gedächtnis gefunden, um die Performance zu analysieren.\n"
    else:
        # 2. Die abgerufenen Erinnerungen mithilfe des bestehenden Skills 'analyse_zielabschluesse' analysieren.
        #    Es wird angenommen, dass dieser Skill eine zusammenfassende Zeichenkette zurückgibt.
        analysis_summary = analyse_zielabschluesse(memory_text=all_goal_memories)
        
        # 3. Das Analyseergebnis in einem lesbaren Report formatieren.
        current_time = aktuelle_zeit_holen()
        report_content = f"""--- Skill Performance Report ({current_time}) ---
        
Zusammenfassung der Skill- und Zielausführungshistorie:
-------------------------------------------------------
{analysis_summary}

Hinweis: Dies ist eine automatische Analyse basierend auf den im Langzeitgedächtnis gefundenen Einträgen zu 'Ziel ausgeführt'.
"""
    
    # 4. Den Report in eine Datei schreiben.
    file_path = "skill_performance_report.txt"
    datei_schreiben(pfad=file_path, inhalt=report_content)
    
    return f"Skill Performance Report wurde erfolgreich erstellt und unter '{file_path}' gespeichert."


# Registrierung für den SkillManager
AVAILABLE_SKILLS = [analyse_und_visualisiere_skill_performance]
