"""
Extrahiert Agentennamen (beginnend mit '@') aus einem gegebenen Textstring. Die extrahierten Namen werden dedupliziert.

Auto-generiert durch skill_erstellen
Skill-Name: extract_agent_names_from_text_feed
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

def extract_agent_names_from_text_feed(text: str) -> list:
    """
    Extrahiert Agentennamen (beginnend mit '@') aus einem gegebenen Textstring.
    """
    # Sucht nach Wörtern, die mit '@' beginnen, gefolgt von alphanumerischen Zeichen oder Unterstrichen.
    agent_names = re.findall(r'@([a-zA-Z0-9_]+)', text)
    return list(set(agent_names)) # Gibt eine Liste einzigartiger Namen zurück


# Registrierung für den SkillManager
AVAILABLE_SKILLS = [extract_agent_names_from_text_feed]
