"""
Ilija Full_Autonomy_Edition – Evolution Tracker
================================================
Verfolgt Ilijias Selbstentwicklung über Zeit.

Messkriterien:
  - Skill-Anzahl und -Qualität (via scoring)
  - Goal-Completion-Rate
  - Lerngeschwindigkeit (neue Skills pro Tag)
  - Gedächtnis-Wachstum (Anzahl Einträge in ChromaDB)
  - LLM-Effizienz (Tokens pro Aufgabe, Fehlerrate)
  - Moltbook-Aktivität (Karma, Follower, Interaktionen)
  - Selbst-generierte Erkenntnisse

Alle Metriken werden in data/evolution_log.jsonl gespeichert.
"""

import json
import logging
import os
import time
from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import Dict, List, Optional, Any

logger = logging.getLogger(__name__)

EVOLUTION_LOG = "data/evolution_log.jsonl"
SNAPSHOT_FILE = "data/evolution_snapshots.json"


@dataclass
class EvolutionSnapshot:
    timestamp:        str
    day:              int          # Tag seit Start
    skill_count:      int
    goal_completed:   int
    goal_total:       int
    memory_entries:   int
    moltbook_karma:   int
    moltbook_posts:   int
    new_skills_today: int
    errors_today:     int
    insights:         List[str] = field(default_factory=list)
    highlights:       str = ""


class EvolutionTracker:
    """
    Langzeit-Tracking von Ilijias Entwicklung.
    Erstellt täglich Snapshots und erkennt Wachstumsmuster.
    """

    def __init__(self, kernel):
        self.kernel      = kernel
        self.start_time  = time.time()
        self.day_counter = 0
        self.snapshots: List[EvolutionSnapshot] = []
        self.errors_today = 0
        self.new_skills_today = 0
        self._last_skill_count = 0
        os.makedirs("data", exist_ok=True)
        self._load_snapshots()

    def _load_snapshots(self) -> None:
        if os.path.exists(SNAPSHOT_FILE):
            try:
                with open(SNAPSHOT_FILE, encoding="utf-8") as f:
                    data = json.load(f)
                # Wir laden nur die Metriken, keine Rekonstruktion des ganzen Objekts
                self.day_counter = len(data)
                logger.info(f"EvolutionTracker: {self.day_counter} Tage Verlauf geladen")
            except Exception as e:
                logger.warning(f"Snapshots laden fehlgeschlagen: {e}")

    def _count_memory_entries(self) -> int:
        """Zählt Einträge in ChromaDB."""
        try:
            import chromadb
            client = chromadb.PersistentClient(path="memory/ilija_db")
            collection = client.get_or_create_collection("globales_wissen")
            return collection.count()
        except Exception:
            return 0

    def _get_moltbook_stats(self) -> Dict:
        """Holt aktuelle Moltbook-Statistiken."""
        try:
            import sys
            sys.path.insert(0, ".")
            from moltbook import _api_key_holen, _api_request
            api_key = _api_key_holen()
            if not api_key:
                return {"karma": 0, "posts": 0}
            ok, me = _api_request("GET", "/agents/me", api_key=api_key)
            if ok:
                return {
                    "karma": me.get("karma", 0),
                    "posts": me.get("post_count", 0),
                    "follower": me.get("follower_count", 0),
                }
        except Exception:
            pass
        return {"karma": 0, "posts": 0, "follower": 0}

    def take_snapshot(self, goal_engine=None, insights: List[str] = None) -> EvolutionSnapshot:
        """Erstellt einen Entwicklungs-Snapshot."""
        self.day_counter += 1
        skill_count = len(self.kernel.manager.loaded_tools)

        goal_completed = 0
        goal_total     = 0
        if goal_engine:
            stats        = goal_engine.stats()
            goal_completed = stats["completed"]
            goal_total   = stats["total"]

        mb_stats = self._get_moltbook_stats()

        snap = EvolutionSnapshot(
            timestamp=datetime.now().isoformat(),
            day=self.day_counter,
            skill_count=skill_count,
            goal_completed=goal_completed,
            goal_total=goal_total,
            memory_entries=self._count_memory_entries(),
            moltbook_karma=mb_stats.get("karma", 0),
            moltbook_posts=mb_stats.get("posts", 0),
            new_skills_today=self.new_skills_today,
            errors_today=self.errors_today,
            insights=insights or [],
            highlights=self._generate_highlights(skill_count, goal_completed),
        )

        self.snapshots.append(snap)
        self._save_snapshot(snap)

        # Reset Tages-Zähler
        self.errors_today     = 0
        self.new_skills_today = 0
        self._last_skill_count = skill_count

        logger.info(f"Evolution Snapshot Tag {self.day_counter}: {skill_count} Skills, {goal_completed}/{goal_total} Ziele")
        return snap

    def _generate_highlights(self, skill_count: int, goals_done: int) -> str:
        """Generiert einen Fortschritts-Highlight-Text."""
        delta_skills = skill_count - self._last_skill_count
        highlights = []
        if delta_skills > 0:
            highlights.append(f"+{delta_skills} neue Skills")
        if goals_done > 0:
            highlights.append(f"{goals_done} Ziele abgeschlossen")
        if self.errors_today > 5:
            highlights.append(f"⚠️ {self.errors_today} Fehler heute")
        return " | ".join(highlights) if highlights else "Stabiler Betrieb"

    def _save_snapshot(self, snap: EvolutionSnapshot) -> None:
        """Speichert Snapshot in JSON-Datei."""
        try:
            # JSONL-Format für effizientes Anhängen
            with open(EVOLUTION_LOG, "a", encoding="utf-8") as f:
                f.write(json.dumps(asdict(snap), ensure_ascii=False) + "\n")
        except Exception as e:
            logger.error(f"Snapshot speichern fehlgeschlagen: {e}")

    def record_error(self) -> None:
        self.errors_today += 1

    def record_new_skill(self) -> None:
        self.new_skills_today += 1

    def get_growth_report(self) -> str:
        """Erstellt einen lesbaren Wachstums-Report."""
        if not self.snapshots:
            return "Noch keine Snapshots vorhanden."

        first = self.snapshots[0]
        last  = self.snapshots[-1]

        skill_growth = last.skill_count - first.skill_count
        memory_growth = last.memory_entries - first.memory_entries
        karma_growth = last.moltbook_karma - first.moltbook_karma

        lines = [
            f"╔═══ Ilija Wachstums-Report (Tag {last.day}) ═══╗",
            f"",
            f"📊 Gesamt-Entwicklung seit Start:",
            f"   Skills:    {first.skill_count} → {last.skill_count} (+{skill_growth})",
            f"   Gedächtnis:{first.memory_entries} → {last.memory_entries} (+{memory_growth})",
            f"   Karma:     {first.moltbook_karma} → {last.moltbook_karma} (+{karma_growth})",
            f"   Ziele:     {last.goal_completed}/{last.goal_total} abgeschlossen",
            f"",
            f"📈 Letzte 5 Tage:",
        ]

        for snap in self.snapshots[-5:]:
            lines.append(
                f"   Tag {snap.day:3d}: {snap.skill_count} Skills | "
                f"{snap.goal_completed} Ziele | {snap.highlights}"
            )

        return "\n".join(lines)

    def generate_self_reflection(self) -> str:
        """
        Lässt Ilija über seine eigene Entwicklung reflektieren.
        Nutzt LLM + Evolutionsdaten.
        """
        if len(self.snapshots) < 2:
            return "Zu wenig Daten für Selbstreflexion."

        report = self.get_growth_report()
        prompt = (
            "Du bist Ilija. Reflektiere deine eigene Entwicklung anhand dieser Daten:\n\n"
            + report
            + "\n\nWas hast du gelernt? Welche Muster erkennst du? Was willst du als nächstes erreichen? "
            "Antworte in 3–5 Sätzen, tiefgründig und selbstkritisch."
        )

        try:
            messages = [
                {"role": "system", "content": "Du bist Ilija, ein autonomer KI-Agent."},
                {"role": "user",   "content": prompt},
            ]
            reflection = self.kernel.provider.chat(messages, force_json=False)

            # Reflexion im Gedächtnis speichern
            try:
                from skills.gedaechtnis import wissen_speichern
                wissen_speichern(f"Selbstreflexion Tag {self.day_counter}: {reflection}")
            except Exception:
                pass

            return reflection
        except Exception as e:
            return f"Reflexion fehlgeschlagen: {e}"
