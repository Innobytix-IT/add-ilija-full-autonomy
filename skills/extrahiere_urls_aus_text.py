"""
Extrahiert valide HTTP/HTTPS-URLs aus einem gegebenen Textstring, bereinigt sie und gibt eine Liste einzigartiger URLs zurück.

Auto-generiert durch skill_erstellen
Skill-Name: extrahiere_urls_aus_text
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

def extrahiere_urls_aus_text(text: str) -> list:
    """
    Extrahiert valide URLs (http/https) aus einem gegebenen Textstring.

    Args:
        text (str): Der Text, aus dem URLs extrahiert werden sollen.

    Returns:
        list: Eine Liste von einzigartigen, extrahierten URLs.
    """
    if not isinstance(text, str):
        return []

    # Regex to find URLs (http/https and then domain, path, query, fragment)
    # This regex tries to capture common URL patterns, including subdomains and query parameters.
    url_pattern = re.compile(r'https?://(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,6}(?:/[^\s]*)?')
    urls = url_pattern.findall(text)

    # Filter out duplicates and perform basic validation (e.g., must contain a domain suffix)
    valid_urls = []
    for url in urls:
        # Simple check for a valid domain structure after the scheme
        domain_part = url.split('//', 1)[-1]
        if '.' in domain_part and len(domain_part.split('.')[-1]) >= 2: # Ensure it has a TLD
            valid_urls.append(url)

    return list(set(valid_urls))

# Registrierung für den SkillManager
AVAILABLE_SKILLS = [extrahiere_urls_aus_text]
