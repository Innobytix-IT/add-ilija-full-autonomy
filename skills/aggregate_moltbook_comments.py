"""
Sammelt Kommentare von einer Liste von Moltbook-Post-IDs und gibt sie als einzelne Textzeichenkette zur Analyse zurück.

Auto-generiert durch skill_erstellen
Skill-Name: aggregate_moltbook_comments
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
import moltbook
def aggregate_moltbook_comments(post_ids: list):
    all_comments_text = []
    for post_id in post_ids:
        try:
            comments_result = moltbook.moltbook_kommentare_lesen(post_id=post_id, anzahl=50) # Max 50 comments
            if 'comments' in comments_result:
                for comment in comments_result['comments']:
                    all_comments_text.append(comment.get('text', ''))
        except Exception as e:
            # Log error or handle gracefully
            print(f'Fehler beim Abrufen der Kommentare für Post {post_id}: {e}')
    return '\n'.join(all_comments_text)

# Registrierung für den SkillManager
AVAILABLE_SKILLS = [aggregate_moltbook_comments]
