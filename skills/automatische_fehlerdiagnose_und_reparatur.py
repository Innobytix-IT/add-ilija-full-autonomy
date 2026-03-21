"""
Analysiert einen gegebenen 'error_context', diagnostiziert das Problem und schlägt konkrete Reparaturschritte vor.

Auto-generiert durch skill_erstellen
Skill-Name: automatische_fehlerdiagnose_und_reparatur
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
def automatische_fehlerdiagnose_und_reparatur(error_context: str):
    diagnosis = f"Analysiere Fehlerkontext: '{error_context}'."
    repair_steps = ""
    if "API-Key" in error_context or "Authentifizierung" in error_context:
        repair_steps = "Überprüfe den API-Key oder die Authentifizierungsdetails. Stelle sicher, dass sie korrekt und gültig sind."
    elif "Verbindung fehlgeschlagen" in error_context or "Timeout" in error_context:
        repair_steps = "Überprüfe die Netzwerkkonnektivität und die Erreichbarkeit des Zielsystems. Versuche es nach einer kurzen Wartezeit erneut."
    elif "Datei nicht gefunden" in error_context or "Pfad ungültig" in error_context:
        repair_steps = "Verifiziere den Dateipfad. Stelle sicher, dass die Datei existiert und die Zugriffsrechte korrekt sind."
    elif "unerwarteter Fehler" in error_context or "unbekannter Fehler" in error_context:
        repair_steps = "Ein allgemeiner Fehler ist aufgetreten. Überprüfe die detaillierten System-Logs für weitere Informationen und starte die betroffene Komponente neu, falls möglich."
    else:
        repair_steps = "Keine spezifische Reparaturstrategie für diesen Fehlerkontext gefunden. Allgemeine Empfehlung: Überprüfe die Logs und die Systemdokumentation."
    
    return {"diagnosis": diagnosis, "repair_steps": repair_steps}

# Registrierung für den SkillManager
AVAILABLE_SKILLS = [automatische_fehlerdiagnose_und_reparatur]
