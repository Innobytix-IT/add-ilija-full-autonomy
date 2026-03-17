import json, os, uuid
from datetime import datetime

GOALS_FILE = '/ilija/data/goals.json'

def _load():
    try:
        return json.load(open(GOALS_FILE))
    except:
        return []

def _save(g):
    json.dump(g, open(GOALS_FILE, 'w'), indent=2, ensure_ascii=False)

def goal_manager(action='list', title=None, goal_id=None, progress=None, status=None):
    '''Persistente Langzeit-Ziele. WANN: list=aktive, add=neu, next=naechstes, complete=abschliessen, stats=statistik'''
    if not os.path.exists(GOALS_FILE):
        _save([])
    goals = _load()
    action = (action or 'list').lower().strip()

    if action == 'add':
        if not title:
            return 'Fehler: title benoetigt'
        g = {'id': 'goal_p_' + str(uuid.uuid4())[:8], 'goal': title, 'category': 'persistent', 'priority': 5, 'completed': False, 'score': 0.0, 'created_at': datetime.now().isoformat()}
        goals.append(g)
        _save(goals)
        return 'Ziel gespeichert: [' + g['id'] + '] ' + title

    elif action == 'list':
        active = [g for g in goals if not g.get('completed', False)]
        if not active:
            return 'Keine aktiven Ziele.'
        out = 'Aktive Ziele (' + str(len(active)) + '):\n'
        for g in active[:15]:
            out += '  [' + g['id'] + '] P:' + str(g.get('priority', 0)) + ' | ' + g.get('goal', g.get('title', '?')) + '\n'
        return out

    elif action == 'next':
        active = [g for g in goals if not g.get('completed', False)]
        if not active:
            return 'Keine aktiven Ziele.'
        n = max(active, key=lambda x: x.get('priority', 0))
        return 'Naechstes Ziel: [' + n['id'] + '] ' + n.get('goal', n.get('title', '?'))

    elif action == 'complete':
        for g in goals:
            if g['id'] == goal_id:
                g['completed'] = True
                g['score'] = float(progress) if progress else 8.0
                _save(goals)
                return 'Abgeschlossen: ' + g.get('goal', '?')
        return 'Nicht gefunden: ' + str(goal_id)

    elif action == 'stats':
        total = len(goals)
        done = len([g for g in goals if g.get('completed')])
        active = total - done
        scores = [g.get('score', 0) for g in goals if g.get('completed') and g.get('score')]
        avg = sum(scores)/len(scores) if scores else 0
        return 'Gesamt: ' + str(total) + ' | Abgeschlossen: ' + str(done) + ' | Aktiv: ' + str(active) + ' | Avg-Score: ' + str(round(avg, 1))

    else:
        return goal_manager('list')

AVAILABLE_SKILLS = [goal_manager]
