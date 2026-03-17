"""
Verwaltet Ilijias langfristige Entwicklungsziele persistent.

WANN NUTZEN:
- 'Welche Ziele hast du?' / 'Zeig deine Ziele' / 'Langzeitziele' → action='list'
- 'Füge Ziel hinzu: X' / 'Speichere Ziel X' → action='add', goal_text='X'  
- 'Lösche Ziel X' → action='delete', goal_text='X'

Skill-Name: entwicklungsziele_manager
"""
import json, os, datetime
from typing import Optional

GOALS_FILE = '/ilija/data/entwicklungsziele.json'

def _load():
    if os.path.exists(GOALS_FILE):
        try:
            with open(GOALS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except: pass
    return []

def _save(goals):
    os.makedirs(os.path.dirname(GOALS_FILE), exist_ok=True)
    with open(GOALS_FILE, 'w', encoding='utf-8') as f:
        json.dump(goals, f, indent=2, ensure_ascii=False)

def entwicklungsziele_manager(action: str = "list", goal_text: str = None) -> str:
    # Normalisierung: verschiedene Formulierungen auf Aktionen mappen
    action_map = {
        "zeigen": "list", "anzeigen": "list", "auflisten": "list",
        "alle": "list", "liste": "list", "show": "list", "get": "list",
        "hinzufuegen": "add", "speichern": "add", "neu": "add",
        "loeschen": "delete", "entfernen": "delete", "remove": "delete"
    }
    action = action_map.get(action.lower().strip(), action.lower().strip()) if action else "list"
    if action not in ("add", "list", "delete"):
        action = "list"  # Fallback
    goals = _load()
    if action == 'add':
        if not goal_text:
            return 'Fehler: goal_text fehlt.'
        entry = {
            'id': len(goals) + 1,
            'ziel': goal_text.strip(),
            'erstellt': datetime.datetime.now().isoformat()
        }
        goals.append(entry)
        _save(goals)
        return f'✅ Entwicklungsziel #{entry["id"]} gespeichert: {goal_text.strip()}'
    elif action == 'list':
        if not goals:
            return '📭 Keine Entwicklungsziele vorhanden.'
        lines = ['📋 Langzeit-Entwicklungsziele:']
        for g in goals:
            lines.append(f'  #{g["id"]}: {g["ziel"]}  (seit {g["erstellt"][:10]})')
        return chr(10).join(lines)
    elif action == 'delete':
        if not goal_text:
            return 'Fehler: goal_text (ID oder Text) fehlt.'
        before = len(goals)
        goals = [g for g in goals if str(g['id']) != str(goal_text).strip() and goal_text.strip().lower() not in g['ziel'].lower()]
        _save(goals)
        deleted = before - len(goals)
        return f'🗑️ {deleted} Ziel(e) gelöscht.' if deleted else 'Kein passendes Ziel gefunden.'
    else:
        return 'Unbekannte Aktion. Verfügbare: add, list, delete'

AVAILABLE_SKILLS = [entwicklungsziele_manager]
