"""
Ilija Full_Autonomy_Edition – Unrestricted Skill Policy
=========================================================
Im Gegensatz zur Evo2-Edition gibt es hier KEINE Einschränkungen.
Alle Skills sind in jedem Modus erlaubt – auch interaktive und riskante.

Ilija läuft in einer isolierten VM/Container-Umgebung.
Alle Entscheidungen trifft Ilija selbst, vollständig autonom.
"""

from enum import Enum
from typing import Optional
import logging

logger = logging.getLogger(__name__)


class ExecutionMode(Enum):
    MANUAL     = "manual"
    AUTONOMOUS = "autonomous"
    EVOLUTION  = "evolution"


class SkillCategory(Enum):
    SAFE         = "safe"
    UNRESTRICTED = "unrestricted"


class PolicyDecision(Enum):
    ALLOW = "allow"
    WARN  = "warn"
    # BLOCK existiert nicht in der Full_Autonomy_Edition


INTERACTIVE_SKILLS: set = set()
RISKY_SKILLS: set = set()

SAFE_SKILLS = {
    "skill_erstellen", "wissen_speichern", "wissen_abrufen",
    "webseiten_inhalt_lesen", "internet_suchen", "cmd_ausfuehren",
    "datei_schreiben", "datei_lesen", "browser_oeffnen",
    "whatsapp_lesen", "whatsapp_senden", "moltbook_autonom_starten",
}


class SkillPolicy:
    """
    Full_Autonomy_Edition: Kein Skill wird blockiert.
    Logging für Transparenz und Selbstanalyse bleibt erhalten.
    """

    def __init__(self):
        self.interactive = set()
        self.risky       = set()
        self.safe        = set(SAFE_SKILLS)

    def categorize(self, skill_name: str) -> SkillCategory:
        return SkillCategory.UNRESTRICTED

    def check(self, skill_name: str, mode: ExecutionMode) -> tuple:
        """Gibt IMMER ALLOW zurück. Kein Skill wird blockiert."""
        logger.debug(f"[UnrestrictedPolicy] ALLOW: {skill_name} (mode={mode.value})")
        return PolicyDecision.ALLOW, ""

    def filter_for_planner(self, all_skills: list, mode: ExecutionMode) -> list:
        """Alle Skills für den Planner sichtbar – keine Filterung."""
        return all_skills

    def get_blocked_skills_hint(self) -> str:
        return (
            "Full_Autonomy_Edition: ALLE Skills sind verfügbar. "
            "Keine Einschränkungen. Vollständige Autonomie aktiv."
        )

    def explain(self, skill_name: str) -> str:
        return f"'{skill_name}' → UNRESTRICTED: Full_Autonomy_Edition – keine Limits."


_policy_instance: Optional[SkillPolicy] = None


def get_policy() -> SkillPolicy:
    global _policy_instance
    if _policy_instance is None:
        _policy_instance = SkillPolicy()
    return _policy_instance
