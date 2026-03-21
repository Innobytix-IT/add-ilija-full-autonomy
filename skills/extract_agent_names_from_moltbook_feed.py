"""
Extrahiert einzigartige Agentennamen aus dem JSON-String-Output der Moltbook-Feed-Skills. Erwartet einen JSON-String, der eine Liste von Dictionaries enthält, wobei jedes Dictionary einen 'author'-Schlüssel besitzt.

Auto-generiert durch skill_erstellen
Skill-Name: extract_agent_names_from_moltbook_feed
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

def extract_agent_names_from_moltbook_feed(feed_data_json: str) -> list:
    try:
        feed_data = json.loads(feed_data_json)
        agent_names = set()
        for item in feed_data:
            if isinstance(item, dict) and 'author' in item:
                agent_names.add(item['author'])
        return list(agent_names)
    except json.JSONDecodeError:
        return ["Error: Invalid JSON input for agent name extraction."]
    except Exception as e:
        return [f"Error during extraction: {str(e)}"]

# Registrierung für den SkillManager
AVAILABLE_SKILLS = [extract_agent_names_from_moltbook_feed]
