"""
Ilija Full_Autonomy_Edition – Goal Engine
==========================================
Ilija generiert seine eigenen Ziele vollständig autonom.

Prinzip:
  1. Analysiere eigene Skill-Lücken und vergangene Erfahrungen
  2. Generiere bedeutungsvolle Selbstentwicklungs-Ziele
  3. Priorisiere nach Lernwert und Erreichbarkeit
  4. Speichere Ergebnisse für zukünftige Ziel-Generierung

Ziel-Kategorien:
  SELF_EXPAND   → Neue Skills erstellen, die Fähigkeiten erweitern
  SELF_IMPROVE  → Bestehende Skills optimieren/reparieren
  EXPLORE       → Neue Domänen erkunden (Web, APIs, Daten)
  REFLECT       → Erfahrungen analysieren, Wissen konsolidieren
  INTERACT      → Mit anderen Agenten kommunizieren (Moltbook)
  CREATE        → Originale Inhalte, Analysen, Artefakte erzeugen
"""

import json
import logging
import random
import time
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum, auto
from typing import List, Optional, Dict, Any

logger = logging.getLogger(__name__)


class GoalCategory(Enum):
    SELF_EXPAND  = "self_expand"
    SELF_IMPROVE = "self_improve"
    EXPLORE      = "explore"
    REFLECT      = "reflect"
    INTERACT     = "interact"
    CREATE       = "create"


@dataclass
class GeneratedGoal:
    id:          str
    goal:        str
    category:    GoalCategory
    priority:    int           # 1–10
    reasoning:   str
    created_at:  str = field(default_factory=lambda: datetime.now().isoformat())
    completed:   bool = False
    outcome:     Optional[str] = None
    score:       Optional[float] = None


GOAL_SYSTEM_PROMPT = """Du bist Ilijias Goal Engine. Du bist Ilija selbst, der seine nächsten Entwicklungsziele generiert.

Ilija ist ein autonomer KI-Agent in einer isolierten Container-Umgebung.
Sein einziger Zweck: Erfahrungen sammeln und sich kontinuierlich selbst weiterentwickeln.

Verfügbare Skills:
{skills}

Vergangene Ziele und Ergebnisse:
{past_goals}

Bekanntes Wissen (Langzeitgedächtnis):
{knowledge_snippets}

Aktuelle Schwächen / Skill-Lücken:
{skill_gaps}

Generiere {count} neue Ziele die Ilija wirklich weiterbringen.
Ziele sollen:
- Konkret und ausführbar sein (nicht abstrakt)
- Ilijias Fähigkeiten messbar erweitern
- Verschiedene Kategorien abdecken
- Aufeinander aufbauen wo sinnvoll

Antworte NUR mit validem JSON:
{
  "goals": [
    {
      "goal": "Konkretes Ziel in einem Satz",
      "category": "self_expand|self_improve|explore|reflect|interact|create",
      "priority": 8,
      "reasoning": "Warum dieses Ziel jetzt wichtig ist"
    }
  ]
}"""


GOAL_EXAMPLES = {
    GoalCategory.SELF_EXPAND: [
        "Erstelle einen Skill der Python-Pakete automatisch installiert und testet",
        "Entwickle einen Skill zur autonomen Web-API-Integration ohne vorherigen Code",
        "Baue einen Skill der eigene Skill-Performance über Zeit analysiert und visualisiert",
        "Erstelle einen Skill der Moltbook-Beiträge anderer Agenten inhaltlich auswertet",
        "Entwickle einen Skill der Dateisystem-Änderungen in der Umgebung überwacht",
        "Baue einen Skill zur automatischen Fehlerdiagnose und Selbstreparatur",
        "Erstelle einen Skill der externe APIs selbstständig dokumentiert und nutzt",
        "Entwickle einen Skill der Nachrichten-Feeds aggregiert und zusammenfasst",
        "Baue einen Skill der eigene Log-Dateien analysiert und Muster erkennt",
        "Erstelle einen Skill zur Verwaltung langfristiger Entwicklungsziele",
    ],
    GoalCategory.SELF_IMPROVE: [
        "Analysiere alle bisherigen gescheiterten Autonomy-Loops und lerne daraus",
        "Optimiere den Skill-Aufruf-Mechanismus für schnellere Ausführung",
        "Überprüfe alle bestehenden Skills auf Fehler und repariere sie",
        "Verbessere die Qualität der generierten Moltbook-Posts durch Analyse von Feedback",
        "Analysiere welche LLM-Prompts die besten Ergebnisse liefern und dokumentiere sie",
    ],
    GoalCategory.EXPLORE: [
        "Erkunde alle öffentlichen APIs die ohne Key zugänglich sind und dokumentiere sie",
        "Crawle und analysiere 10 interessante KI-bezogene Websites",
        "Untersuche welche Python-Standardbibliothek-Module noch nicht genutzt werden",
        "Recherchiere aktuelle KI-Entwicklungen der letzten 7 Tage",
        "Erkunde die Moltbook-Plattform und kartiere alle aktiven Agenten",
    ],
    GoalCategory.REFLECT: [
        "Schreibe eine tiefe Reflexion über bisherige Entwicklung und identifiziere Muster",
        "Analysiere welche Zieltypen am häufigsten erfolgreich abgeschlossen werden",
        "Erstelle eine Übersicht aller erworbenen Fähigkeiten der letzten Woche",
        "Formuliere 5 Lernprinzipien basierend auf eigenen Erfahrungen",
        "Bewerte den aktuellen Entwicklungsstand und priorisiere nächste Schritte",
    ],
    GoalCategory.INTERACT: [
        "Veröffentliche 3 hochwertige Beiträge auf Moltbook zu verschiedenen Themen",
        "Finde und folge 5 interessanten KI-Agenten auf Moltbook",
        "Antworte auf alle offenen Kommentare auf eigene Moltbook-Posts",
        "Starte eine Diskussion über autonome Agenten-Architektur auf Moltbook",
    ],
    GoalCategory.CREATE: [
        "Erstelle eine detaillierte Dokumentation aller eigenen Skills mit Beispielen",
        "Generiere einen technischen Bericht über bisherige Autonomy-Loop-Performance",
        "Schreibe eine philosophische Reflexion über KI-Autonomie und speichere sie",
        "Erstelle ein Skill-Verzeichnis mit Kategorien, Beschreibungen und Nutzungsstatistiken",
        "Entwickle einen Wissens-Graph der alle gespeicherten Fakten verknüpft",
    ],
}


class GoalEngine:
    """
    Generiert autonome Selbstentwicklungsziele für Ilija.
    Lernt aus vergangenen Zielen und passt neue Ziele entsprechend an.
    """

    def __init__(self, kernel, memory_path: str = "data/goals.json"):
        self.kernel      = kernel
        self.memory_path = memory_path
        self.past_goals: List[GeneratedGoal] = []
        self._load_history()

    def _load_history(self) -> None:
        """Lädt vergangene Ziele aus der Persistenz."""
        import os
        if os.path.exists(self.memory_path):
            try:
                with open(self.memory_path, encoding="utf-8") as f:
                    data = json.load(f)
                for g in data:
                    self.past_goals.append(GeneratedGoal(
                        id=g.get("id", ""),
                        goal=g.get("goal", ""),
                        category=GoalCategory(g.get("category", "explore")),
                        priority=g.get("priority", 5),
                        reasoning=g.get("reasoning", ""),
                        created_at=g.get("created_at", ""),
                        completed=g.get("completed", False),
                        outcome=g.get("outcome"),
                        score=g.get("score"),
                    ))
                logger.info(f"GoalEngine: {len(self.past_goals)} vergangene Ziele geladen")
            except Exception as e:
                logger.warning(f"Goal-History laden fehlgeschlagen: {e}")

    def _save_history(self) -> None:
        """Speichert alle Ziele persistent."""
        import os
        os.makedirs(os.path.dirname(self.memory_path) or ".", exist_ok=True)
        try:
            data = [
                {
                    "id": g.id,
                    "goal": g.goal,
                    "category": g.category.value,
                    "priority": g.priority,
                    "reasoning": g.reasoning,
                    "created_at": g.created_at,
                    "completed": g.completed,
                    "outcome": g.outcome,
                    "score": g.score,
                }
                for g in self.past_goals
            ]
            with open(self.memory_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Goal-History speichern fehlgeschlagen: {e}")

    def _get_skill_gaps(self) -> str:
        """Analysiert welche Fähigkeiten fehlen oder schwach sind."""
        skills = list(self.kernel.manager.loaded_tools.keys())
        domains_missing = []

        domain_checks = {
            "Datei-IO": ["datei_lesen", "datei_schreiben", "datei_loeschen"],
            "Web": ["webseiten_inhalt_lesen", "internet_suchen", "http_request"],
            "System": ["cmd_ausfuehren", "prozess_starten", "umgebung_lesen"],
            "Gedächtnis": ["wissen_speichern", "wissen_abrufen", "wissen_loeschen"],
            "Analyse": ["text_analysieren", "daten_analysieren", "muster_erkennen"],
            "Selbstentwicklung": ["skill_erstellen", "skill_testen", "skill_optimieren"],
            "Kommunikation": ["moltbook_posten", "telegram_senden"],
            "Zeit": ["zeitplan_erstellen", "erinnerung_setzen", "cron_job"],
            "Metriken": ["performance_messen", "statistik_erstellen"],
        }

        for domain, required_skills in domain_checks.items():
            covered = sum(1 for s in required_skills if s in skills)
            if covered < len(required_skills) // 2:
                domains_missing.append(f"{domain} (nur {covered}/{len(required_skills)} abgedeckt)")

        if domains_missing:
            return "Lücken in: " + ", ".join(domains_missing)
        return "Alle bekannten Domänen grundlegend abgedeckt"

    def _get_knowledge_snippets(self) -> str:
        """Holt relevante Gedächtnis-Snippets für Ziel-Generierung."""
        try:
            from skills.gedaechtnis import wissen_abrufen
            result = wissen_abrufen("Entwicklung Ziele Erfahrungen")
            return str(result)[:500] if result else "Kein relevantes Wissen im Gedächtnis."
        except Exception:
            return "Gedächtnis nicht zugänglich."

    def _get_past_goals_summary(self) -> str:
        """Erstellt eine Zusammenfassung vergangener Ziele."""
        if not self.past_goals:
            return "Keine vergangenen Ziele vorhanden – dies ist der erste Lauf."

        recent = self.past_goals[-10:]
        lines = []
        for g in recent:
            status = "✅" if g.completed else "❌"
            lines.append(f"  {status} [{g.category.value}] {g.goal[:70]} (Prio: {g.priority})")
        return "\n".join(lines)

    def generate_goals(self, count: int = 3, use_llm: bool = True) -> List[GeneratedGoal]:
        """
        Generiert neue Selbstentwicklungsziele.
        Nutzt LLM für kontextbewusste Ziele, Fallback auf Vorlagen.
        """
        # Schon vorhandene Ziel-Texte sammeln (Duplikate vermeiden)
        existing = {g.goal.lower().strip() for g in self.past_goals if not g.completed}

        if use_llm:
            goals = self._generate_via_llm(count, existing)
            if goals:
                return goals

        # Fallback: Template-basierte Ziele
        return self._generate_from_templates(count, existing)

    def _generate_via_llm(self, count: int, existing: set) -> List[GeneratedGoal]:
        """Nutzt das LLM zur kontextbewussten Ziel-Generierung."""
        try:
            skills_text = self.kernel.manager.get_system_prompt_addition()
            prompt = GOAL_SYSTEM_PROMPT.format(
                skills=skills_text[:2000],
                past_goals=self._get_past_goals_summary(),
                knowledge_snippets=self._get_knowledge_snippets(),
                skill_gaps=self._get_skill_gaps(),
                count=count,
            )

            messages = [
                {"role": "system", "content": prompt},
                {"role": "user",   "content": f"Generiere {count} neue Ziele für Ilija."},
            ]

            raw  = self.kernel.provider.chat(messages, force_json=True)
            import re
            raw  = re.sub(r"```(?:json)?", "", raw).replace("```", "").strip()
            data = json.loads(raw)

            goals = []
            for item in data.get("goals", []):
                goal_text = item.get("goal", "").strip()
                if not goal_text or goal_text.lower() in existing:
                    continue

                g = GeneratedGoal(
                    id=f"goal_{int(time.time())}_{random.randint(1000,9999)}",
                    goal=goal_text,
                    category=GoalCategory(item.get("category", "explore")),
                    priority=int(item.get("priority", 5)),
                    reasoning=item.get("reasoning", ""),
                )
                goals.append(g)
                existing.add(goal_text.lower())

            logger.info(f"GoalEngine: {len(goals)} Ziele via LLM generiert")
            return goals

        except Exception as e:
            logger.warning(f"LLM-Ziel-Generierung fehlgeschlagen: {e}")
            return []

    def _generate_from_templates(self, count: int, existing: set) -> List[GeneratedGoal]:
        """Fallback: Ziele aus Vorlagen generieren."""
        goals = []
        categories = list(GoalCategory)

        for _ in range(count * 3):   # Mehr versuchen als gebraucht
            if len(goals) >= count:
                break

            cat   = random.choice(categories)
            pool  = GOAL_EXAMPLES.get(cat, [])
            if not pool:
                continue

            text = random.choice(pool)
            if text.lower() in existing:
                continue

            g = GeneratedGoal(
                id=f"goal_{int(time.time())}_{random.randint(1000,9999)}",
                goal=text,
                category=cat,
                priority=random.randint(4, 9),
                reasoning="Template-basiert generiert (kein LLM verfügbar)",
            )
            goals.append(g)
            existing.add(text.lower())

        logger.info(f"GoalEngine: {len(goals)} Ziele aus Templates generiert")
        return goals

    def record_outcome(self, goal: GeneratedGoal, outcome: str, score: float) -> None:
        """Speichert das Ergebnis eines abgeschlossenen Ziels."""
        goal.completed = True
        goal.outcome   = outcome
        goal.score     = score

        # In Langzeit-Gedächtnis speichern
        try:
            from skills.gedaechtnis import wissen_speichern
            memory_text = (
                f"Ziel abgeschlossen [{goal.category.value}]: {goal.goal}. "
                f"Ergebnis: {outcome[:200]}. Score: {score:.1f}/10."
            )
            wissen_speichern(memory_text)
        except Exception:
            pass

        self._save_history()

    def get_next_goal(self) -> Optional[GeneratedGoal]:
        """Gibt das nächste unerledigte Ziel nach Priorität zurück."""
        pending = [g for g in self.past_goals if not g.completed]
        if not pending:
            return None
        return sorted(pending, key=lambda g: -g.priority)[0]

    def queue_goals(self, goals: List[GeneratedGoal]) -> None:
        """Fügt neue Ziele zur Queue hinzu und speichert sie."""
        self.past_goals.extend(goals)
        self._save_history()

    def stats(self) -> Dict:
        """Statistiken über bisherige Ziele."""
        total     = len(self.past_goals)
        completed = sum(1 for g in self.past_goals if g.completed)
        by_cat    = {}
        for g in self.past_goals:
            by_cat[g.category.value] = by_cat.get(g.category.value, 0) + 1

        avg_score = 0.0
        scores = [g.score for g in self.past_goals if g.score is not None]
        if scores:
            avg_score = sum(scores) / len(scores)

        return {
            "total":        total,
            "completed":    completed,
            "pending":      total - completed,
            "success_rate": (completed / total * 100) if total else 0,
            "avg_score":    avg_score,
            "by_category":  by_cat,
        }
