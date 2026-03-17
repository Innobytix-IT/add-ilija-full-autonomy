"""
Liest 'public_apis.json', filtert nach APIs ohne Authentifizierung ('Auth: No') und dokumentiert sie in einer Textdatei.

Auto-generiert durch skill_erstellen
Skill-Name: document_keyless_apis
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
import json
from datetime import datetime

def document_keyless_apis(input_file_path: str, output_file_path: str):
    try:
        with open(input_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        return f"Fehler: Eingabedatei '{input_file_path}' nicht gefunden. Bitte stellen Sie sicher, dass sie existiert."
    except json.JSONDecodeError:
        return f"Fehler: Konnte '{input_file_path}' nicht als JSON parsen. Dateiinhalt ist möglicherweise beschädigt."
    except Exception as e:
        return f"Ein unerwarteter Fehler beim Lesen der Eingabedatei ist aufgetreten: {e}"

    keyless_apis = []
    if 'entries' in data:
        for api in data['entries']:
            if api.get('Auth') == 'No':
                keyless_apis.append(api)

    if not keyless_apis:
        return "Keine schlüssellosen APIs gefunden, die in der Datei dokumentiert werden könnten."

    current_time_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    documentation_content = "## Dokumentation schlüsselloser öffentlicher APIs\n\n"
    documentation_content += f"Datum der Erstellung: {current_time_str}\n\n"
    documentation_content += "Dies ist eine Liste von öffentlichen APIs, die keine Authentifizierung (API-Key, OAuth etc.) erfordern.\n\n"

    for api in keyless_apis:
        documentation_content += f"### {api.get('API', 'Unbekannter API-Name')}\n"
        documentation_content += f"- **Beschreibung:** {api.get('Description', 'Keine Beschreibung verfügbar.')}\n"
        documentation_content += f"- **Link:** {api.get('Link', 'Kein Link verfügbar.')}\n"
        documentation_content += f"- **Kategorie:** {api.get('Category', 'Unbekannt')}\n"
        documentation_content += f"- **HTTPS-Unterstützung:** {'Ja' if api.get('HTTPS') else 'Nein'}\n"
        documentation_content += f"- **CORS-Unterstützung:** {api.get('Cors', 'Unbekannt')}\n"
        documentation_content += "\n---\n\n"

    try:
        with open(output_file_path, 'w', encoding='utf-8') as f:
            f.write(documentation_content)
        return f"Schlüssellose APIs erfolgreich dokumentiert in '{output_file_path}'. {len(keyless_apis)} APIs wurden gefunden und dokumentiert."
    except Exception as e:
        return f"Fehler beim Schreiben der Dokumentationsdatei '{output_file_path}': {e}"


# Registrierung für den SkillManager
AVAILABLE_SKILLS = [document_keyless_apis]
