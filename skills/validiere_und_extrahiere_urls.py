"""
Extrahiert URLs aus Web-Recherche-Ergebnissen, validiert ihr Format und gibt eine bereinigte Liste zurück. Behebt frühere Probleme mit ungültigen URLs.

Auto-generiert durch skill_erstellen
Skill-Name: validiere_und_extrahiere_urls
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
import re

def validiere_und_extrahiere_urls(research_results_json: str):
    valid_urls = []
    try:
        results = json.loads(research_results_json)
        if not isinstance(results, list):
            return {"error": "Input is not a list of results.", "valid_urls": []}

        for item in results:
            url = item.get('link') or item.get('url')
            # Basic URL validation regex, ensures it starts with http(s)://
            if url and re.match(r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+', url):
                valid_urls.append(url)
    except json.JSONDecodeError:
        return {"error": "Invalid JSON input.", "valid_urls": []}
    except Exception as e:
        return {"error": f"An unexpected error occurred: {str(e)}", "valid_urls": []}
    return {"valid_urls": list(set(valid_urls))}

# Registrierung für den SkillManager
AVAILABLE_SKILLS = [validiere_und_extrahiere_urls]
