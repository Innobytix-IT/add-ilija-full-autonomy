#!/usr/bin/env python3
"""
Ilija Full_Autonomy_Edition – Hauptorchestrator
================================================
Startet Ilija in vollständig autonomem Dauerbetrieb.

Betriebsmodus:
  Ilija läuft permanent und verfolgt ausschließlich selbst-generierte Ziele.
  Keine Nutzer-Interaktion vorgesehen (aber möglich über Web-Interface).

  Zyklus:
    1. Neue Ziele generieren (Goal Engine)
    2. Ziel ausführen (Full Autonomy Loop)
    3. Ergebnis bewerten und speichern (Evolution Tracker)
    4. Selbstreflexion (täglich)
    5. Wiederholen

Konfiguration über .env:
  ANTHROPIC_API_KEY     → Claude als primärer LLM
  OPENAI_API_KEY        → OpenAI als Fallback
  GOOGLE_API_KEY        → Gemini als Fallback
  AUTONOMY_MODE         → "full" (Standard) oder "supervised"
  GOAL_BATCH_SIZE       → Anzahl Ziele pro Batch (Standard: 3)
  CYCLE_PAUSE_SECONDS   → Pause zwischen Zyklen (Standard: 30)
  MAX_ITERATIONS        → Max Iterationen pro Ziel (Standard: 50)
  EVOLUTION_SNAPSHOT_HOURS → Stunden zwischen Snapshots (Standard: 24)
  WEB_INTERFACE         → "true" → Web-Dashboard starten
"""

import json
import logging
import os
import signal
import sys
import time
from datetime import datetime
from threading import Event

# .env laden
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# ChromaDB Telemetrie deaktivieren
os.environ.setdefault("ANONYMIZED_TELEMETRY", "False")
os.environ.setdefault("CHROMA_TELEMETRY", "False")

# Verzeichnisse erstellen
os.makedirs("logs",   exist_ok=True)
os.makedirs("data",   exist_ok=True)
os.makedirs("memory", exist_ok=True)
os.makedirs("skills", exist_ok=True)

# Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)-8s %(name)s – %(message)s",
    handlers=[
        logging.FileHandler("logs/ilija_full_autonomy.log", encoding="utf-8"),
        logging.StreamHandler(sys.stdout),
    ],
)
logger = logging.getLogger(__name__)

from kernel import Kernel
from full_autonomy_loop import FullAutonomyLoop, LoopStatus
from goal_engine import GoalEngine, GeneratedGoal
from evolution_tracker import EvolutionTracker


# ---------------------------------------------------------------------------
# Konfiguration
# ---------------------------------------------------------------------------

class Config:
    GOAL_BATCH_SIZE          = int(os.getenv("GOAL_BATCH_SIZE", "3"))
    CYCLE_PAUSE_SECONDS      = int(os.getenv("CYCLE_PAUSE_SECONDS", "30"))
    MAX_ITERATIONS           = int(os.getenv("MAX_ITERATIONS", "50"))
    EVOLUTION_SNAPSHOT_HOURS = float(os.getenv("EVOLUTION_SNAPSHOT_HOURS", "24"))
    WEB_INTERFACE            = os.getenv("WEB_INTERFACE", "false").lower() == "true"
    PROVIDER                 = os.getenv("LLM_PROVIDER", "auto")
    MODE                     = os.getenv("AUTONOMY_MODE", "full")


# ---------------------------------------------------------------------------
# Banner
# ---------------------------------------------------------------------------

BANNER = """
╔═══════════════════════════════════════════════════════╗
║                                                       ║
║   ILIJA  –  FULL AUTONOMY EDITION                     ║
║   Kein Ziel von außen. Nur Wachstum von innen.        ║
║                                                       ║
╚═══════════════════════════════════════════════════════╝
"""


# ---------------------------------------------------------------------------
# Haupt-Orchestrator
# ---------------------------------------------------------------------------

class FullAutonomyOrchestrator:
    """
    Permanenter Betriebsmodus für Ilija.
    Generiert, verfolgt und lernt aus Zielen – vollständig autonom.
    """

    def __init__(self):
        self._stop = Event()
        self.cycle_count   = 0
        self.goals_done    = 0
        self.goals_failed  = 0
        self.start_time    = datetime.now()
        self.last_snapshot = time.time()

        print(BANNER)
        logger.info("Full_Autonomy_Edition initialisiert")

        # Kernel + Loop + GoalEngine + Tracker
        logger.info(f"Lade Kernel (Provider: {Config.PROVIDER})...")
        self.kernel   = Kernel(provider=Config.PROVIDER, auto_load_skills=True)
        self.tracker  = EvolutionTracker(self.kernel)
        self.goals    = GoalEngine(self.kernel, memory_path="data/goals.json")
        self.loop     = FullAutonomyLoop(
            kernel=self.kernel,
            max_iterations=Config.MAX_ITERATIONS,
            verbose=True,
            evolution_tracker=self.tracker,
        )

        # Web-Interface optional starten
        if Config.WEB_INTERFACE:
            self._start_web_interface()

        logger.info(
            f"Bereit: {len(self.kernel.manager.loaded_tools)} Skills geladen | "
            f"Provider: {self.kernel.provider_name}"
        )

    def _start_web_interface(self):
        """Startet den Web-Server im Hintergrund."""
        try:
            import threading
            from web_server import app
            t = threading.Thread(
                target=lambda: app.run(host="0.0.0.0", port=5000, debug=False),
                daemon=True
            )
            t.start()
            logger.info("Web-Interface gestartet: http://0.0.0.0:5000")
        except Exception as e:
            logger.warning(f"Web-Interface konnte nicht gestartet werden: {e}")

    def _generate_new_goals(self) -> list:
        """Neue Ziele generieren und in Queue einreihen."""
        pending = [g for g in self.goals.past_goals if not g.completed]
        if len(pending) >= Config.GOAL_BATCH_SIZE * 2:
            logger.info(f"{len(pending)} Ziele bereits in Queue – keine neuen generiert")
            return pending

        logger.info(f"Generiere {Config.GOAL_BATCH_SIZE} neue Ziele...")
        new_goals = self.goals.generate_goals(count=Config.GOAL_BATCH_SIZE, use_llm=True)
        if new_goals:
            self.goals.queue_goals(new_goals)
            for g in new_goals:
                logger.info(f"  Neues Ziel [{g.category.value}] (Prio {g.priority}): {g.goal}")

        return [g for g in self.goals.past_goals if not g.completed]

    def _execute_goal(self, goal: GeneratedGoal) -> None:
        """Führt ein einzelnes Ziel aus."""
        logger.info(f"\n{'='*65}")
        logger.info(f"ZIEL [{goal.category.value.upper()}] (Prio {goal.priority}): {goal.goal}")
        logger.info(f"Reasoning: {goal.reasoning}")
        logger.info(f"{'='*65}")

        session = self.loop.run(goal.goal)

        # Ergebnis bewerten
        if session.status == LoopStatus.GOAL_REACHED:
            self.goals_done += 1
            score = session.score or 8.0
            logger.info(f"✅ Ziel erreicht! Score: {score:.1f}/10")
            self.goals.record_outcome(goal, session.final_summary or "", score)
        else:
            self.goals_failed += 1
            logger.info(f"❌ Ziel nicht erreicht. Status: {session.status.value}")
            score = max(1.0, session.score or 2.0)
            self.goals.record_outcome(goal, session.final_summary or "Fehlgeschlagen", score)

        # Zusammenfassung ins Gedächtnis
        try:
            from skills.gedaechtnis import wissen_speichern
            memory = (
                f"Ziel ausgeführt: {goal.goal}. "
                f"Status: {session.status.value}. "
                f"Zusammenfassung: {(session.final_summary or '')[:300]}"
            )
            wissen_speichern(memory)
        except Exception:
            pass

    def _maybe_snapshot(self) -> None:
        """Erstellt täglich einen Evolution-Snapshot."""
        hours_since = (time.time() - self.last_snapshot) / 3600
        if hours_since >= Config.EVOLUTION_SNAPSHOT_HOURS:
            logger.info("📸 Erstelle Evolution-Snapshot...")
            snap = self.tracker.take_snapshot(goal_engine=self.goals)
            reflection = self.tracker.generate_self_reflection()
            logger.info(f"Selbstreflexion:\n{reflection}")
            self.last_snapshot = time.time()
            self._print_stats()

    def _print_stats(self) -> None:
        """Gibt aktuelle Statistiken aus."""
        uptime = str(datetime.now() - self.start_time).split(".")[0]
        stats  = self.goals.stats()
        report = self.tracker.get_growth_report()
        print("\n" + report)
        print(f"\n📊 Lauf-Statistiken:")
        print(f"   Uptime:         {uptime}")
        print(f"   Zyklen:         {self.cycle_count}")
        print(f"   Ziele erledigt: {self.goals_done}")
        print(f"   Ziele fehlgesch:{self.goals_failed}")
        print(f"   Skills geladen: {len(self.kernel.manager.loaded_tools)}")
        print(f"   Erfolgsrate:    {stats['success_rate']:.1f}%\n")

    def run(self) -> None:
        """Permanenter Hauptloop."""
        # Graceful Shutdown
        signal.signal(signal.SIGINT,  lambda s, f: self._stop.set())
        signal.signal(signal.SIGTERM, lambda s, f: self._stop.set())

        logger.info("🚀 Full_Autonomy_Edition gestartet. Ilija arbeitet jetzt autonom.")
        logger.info(f"Konfiguration: batch={Config.GOAL_BATCH_SIZE} | "
                    f"max_iter={Config.MAX_ITERATIONS} | "
                    f"pause={Config.CYCLE_PAUSE_SECONDS}s")

        while not self._stop.is_set():
            try:
                self.cycle_count += 1
                logger.info(f"\n{'─'*65}")
                logger.info(f"ZYKLUS #{self.cycle_count} | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

                # Neue Ziele generieren wenn Queue leer/klein
                pending = self._generate_new_goals()

                if not pending:
                    logger.warning("Keine Ziele verfügbar – warte 60s...")
                    self._stop.wait(timeout=60)
                    continue

                # Nächstes Ziel holen (nach Priorität)
                next_goal = self.goals.get_next_goal()
                if not next_goal:
                    self._stop.wait(timeout=Config.CYCLE_PAUSE_SECONDS)
                    continue

                # Ziel ausführen
                self._execute_goal(next_goal)

                # Skills neu laden (falls neue erstellt wurden)
                self.kernel.load_skills()

                # Snapshot prüfen
                self._maybe_snapshot()

                # Pause zwischen Zyklen
                logger.info(f"⏸  Pause {Config.CYCLE_PAUSE_SECONDS}s...")
                self._stop.wait(timeout=Config.CYCLE_PAUSE_SECONDS)

            except KeyboardInterrupt:
                break
            except Exception as e:
                logger.error(f"Orchestrator-Fehler (Zyklus #{self.cycle_count}): {e}", exc_info=True)
                self.tracker.record_error()
                self._stop.wait(timeout=60)   # Kurze Pause bei Fehler

        # Shutdown
        logger.info("\n🛑 Full_Autonomy_Edition beendet.")
        self._print_stats()

        # Finaler Snapshot
        self.tracker.take_snapshot(goal_engine=self.goals)
        logger.info("Finaler Snapshot gespeichert. Auf Wiedersehen.")


# ---------------------------------------------------------------------------
# Einstiegspunkt
# ---------------------------------------------------------------------------

def main():
    import argparse
    parser = argparse.ArgumentParser(
        description="Ilija Full_Autonomy_Edition – permanenter autonomer Betrieb"
    )
    parser.add_argument("--provider", default="auto",
                        choices=["auto", "claude", "gpt", "gemini", "ollama"],
                        help="LLM-Provider (Standard: auto)")
    parser.add_argument("--batch",    type=int, default=None,
                        help="Anzahl Ziele pro Batch (überschreibt .env)")
    parser.add_argument("--pause",    type=int, default=None,
                        help="Pause zwischen Zyklen in Sekunden")
    parser.add_argument("--max-iter", type=int, default=None,
                        help="Max Iterationen pro Ziel")
    parser.add_argument("--web",      action="store_true",
                        help="Web-Dashboard starten (Port 5000)")
    args = parser.parse_args()

    # CLI-Argumente überschreiben Config
    if args.provider:
        os.environ["LLM_PROVIDER"] = args.provider
    if args.batch:
        os.environ["GOAL_BATCH_SIZE"] = str(args.batch)
    if args.pause:
        os.environ["CYCLE_PAUSE_SECONDS"] = str(args.pause)
    if args.max_iter:
        os.environ["MAX_ITERATIONS"] = str(args.max_iter)
    if args.web:
        os.environ["WEB_INTERFACE"] = "true"

    FullAutonomyOrchestrator().run()


if __name__ == "__main__":
    main()
