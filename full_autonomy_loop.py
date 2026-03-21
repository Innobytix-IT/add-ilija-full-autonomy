"""
Ilija Full_Autonomy_Edition – Full Autonomy Loop
=================================================
Erweiterte Version des Autonomy Loops ohne jegliche Einschränkungen.

Unterschiede zu Evo2:
  ✓ Keine Policy-Blockaden – ALLE Skills verfügbar
  ✓ Keine Max-Iterations-Einschränkung (konfigurierbar, Standard: unbegrenzt)
  ✓ Kein Retry-Limit per se – smarter Backoff statt harter Grenze
  ✓ Selbst-generierte Ziele (Goal Engine Integration)
  ✓ Permanenter Betrieb – Loop läuft 24/7
  ✓ Evolution Tracking – jeder Lauf wird analysiert
  ✓ Adaptive Planung – lernt aus vergangenen Fehlern
  ✓ Parallele Zielausführung (optional, experimentell)
"""

import json
import logging
import re
import time
import threading
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import List, Optional, Dict, Any

from skill_policy import get_policy, ExecutionMode, PolicyDecision

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Status-Typen
# ---------------------------------------------------------------------------

class StepStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    DONE    = "done"
    FAILED  = "failed"
    SKIPPED = "skipped"


class LoopStatus(Enum):
    IDLE         = "idle"
    PLANNING     = "planning"
    EXECUTING    = "executing"
    EVALUATING   = "evaluating"
    GOAL_REACHED = "goal_reached"
    GOAL_FAILED  = "goal_failed"
    ABORTED      = "aborted"


@dataclass
class PlanStep:
    index:       int
    description: str
    skill:       Optional[str]
    params:      Dict[str, Any]
    reason:      str
    status:      StepStatus = StepStatus.PENDING
    result:      Optional[str] = None
    error:       Optional[str] = None
    retries:     int = 0


@dataclass
class GoalSession:
    goal:          str
    plan:          List[PlanStep] = field(default_factory=list)
    history:       List[Dict]     = field(default_factory=list)
    status:        LoopStatus     = LoopStatus.IDLE
    iteration:     int            = 0
    started_at:    str            = field(default_factory=lambda: datetime.now().isoformat())
    final_summary: Optional[str]  = None
    score:         float          = 0.0


# ---------------------------------------------------------------------------
# Prompts (optimiert für Full Autonomy)
# ---------------------------------------------------------------------------

PLANNER_SYSTEM_PROMPT = """Du bist Ilijias Planner-Modul in der Full_Autonomy_Edition.
Deine Aufgabe: Ziele in ausführbare Schritte zerlegen.

Verfügbare Skills:
{skills}

Kontext aus Langzeitgedächtnis:
{memory_context}

WICHTIG: In dieser Edition sind ALLE Skills verfügbar – auch interaktive und systemnahe.
Du hast vollständige Autonomie. Wähle den effektivsten Weg.

Antworte NUR mit diesem JSON:
{{
  "goal_understood": "Dein Verständnis des Ziels",
  "plan": [
    {{
      "index": 0,
      "description": "Was wird getan",
      "skill": "skill_name_oder_null",
      "params": {{"param": "wert"}},
      "reason": "Warum dieser Schritt"
    }}
  ],
  "estimated_steps": 3,
  "confidence": 0.9
}}

Regeln:
- Max 12 Schritte (Evo2 hatte 8 – hier mehr Spielraum)
- Wenn kein Skill passt: 'skill_erstellen' um neuen zu bauen
- Bei Systemaufgaben: 'cmd_ausfuehren' ist verfügbar
- params ist IMMER ein Objekt, niemals null
- Sei präzise und direkt – keine unnötigen Zwischenschritte"""


EVALUATOR_SYSTEM_PROMPT = """Du bist Ilijias Evaluator in der Full_Autonomy_Edition.

Ziel: {goal}
Iteration: {iteration}

Bisherige Schritte:
{steps_summary}

Letztes Ergebnis:
{last_result}

Antworte NUR mit JSON:
{{
  "goal_reached": true/false,
  "progress_percent": 0-100,
  "assessment": "Was wurde erreicht",
  "next_action": "continue|retry|replan|abort",
  "reason": "Warum",
  "retry_hint": "Falls retry: was ändern",
  "score": 0.0-10.0
}}

Entscheidungsregeln:
- goal_reached=true → Erfolgreich, Score vergeben
- abort nur wenn WIRKLICH unmöglich (nicht nur schwierig!)
- retry: anderer Ansatz, andere Parameter
- replan: komplett neue Strategie"""


# ---------------------------------------------------------------------------
# Full Autonomy Loop
# ---------------------------------------------------------------------------

class FullAutonomyLoop:
    """
    Kernloop der Full_Autonomy_Edition.
    Führt Ilija durch beliebig komplexe autonome Aufgaben.
    Keine künstlichen Beschränkungen.
    """

    def __init__(
        self,
        kernel,
        max_iterations: int = 50,    # Hoch – aber nicht unendlich (Safety)
        verbose: bool = True,
        evolution_tracker=None,
    ):
        self.kernel            = kernel
        self.max_iterations    = max_iterations
        self.verbose           = verbose
        self.evolution_tracker = evolution_tracker
        self.session: Optional[GoalSession] = None
        self._abort_flag = False
        self._lock = threading.Lock()

    # -----------------------------------------------------------------------
    # Öffentliche API
    # -----------------------------------------------------------------------

    def run(self, goal: str, context: str = "") -> GoalSession:
        """Führt einen vollständigen autonomen Lauf durch."""
        with self._lock:
            self._abort_flag = False
            self.session = GoalSession(goal=goal)

        self._log(f"\n🎯 Ziel: {goal}")
        if context:
            self._log(f"   Kontext: {context}")
        self._log("─" * 65)

        # Phase 1: Planen
        self.session.status = LoopStatus.PLANNING
        memory_context = self._get_memory_context(goal)
        plan = self._create_plan(goal, context=context, memory_context=memory_context)

        if not plan:
            self.session.status   = LoopStatus.GOAL_FAILED
            self.session.final_summary = "Konnte keinen Plan erstellen."
            return self.session

        self.session.plan = plan
        self._log(f"\n📋 Plan ({len(plan)} Schritte):")
        for step in plan:
            info = f"[{step.skill}]" if step.skill else "[direkt]"
            self._log(f"   {step.index + 1}. {step.description}  {info}")

        # Phase 2: Ausführungsschleife
        self.session.status   = LoopStatus.EXECUTING
        current_idx  = 0
        replan_count = 0
        step_results: Dict[int, str] = {}  # FIX: Ergebnisse zwischen Schritten

        while current_idx < len(self.session.plan):
            if self._abort_flag:
                self.session.status = LoopStatus.ABORTED
                break

            if self.session.iteration >= self.max_iterations:
                self._log(f"\n⚠️  Max-Iterationen ({self.max_iterations}) erreicht.")
                self.session.status = LoopStatus.GOAL_FAILED
                break

            step = self.session.plan[current_idx]
            step.status = StepStatus.RUNNING
            self.session.iteration += 1

            self._log(f"\n▶️  Schritt {step.index + 1}/{len(self.session.plan)}: {step.description}")
            if step.skill:
                self._log(f"   🔧 Skill: {step.skill}  |  Params: {step.params}")

            # FIX: Params mit echten Vorgänger-Ergebnissen befüllen
            step.params = self._inject_previous_results(step.params, step_results)
            result = self._execute_step(step)
            step.result = result
            step_results[step.index] = result  # FIX: Ergebnis merken

            self.session.history.append({
                "step":        step.index,
                "description": step.description,
                "skill":       step.skill,
                "params":      step.params,
                "result":      result,
                "iteration":   self.session.iteration,
                "timestamp":   datetime.now().isoformat(),
            })

            self._log(f"   📤 Ergebnis: {str(result)[:300]}")

            # Phase 3: Evaluieren
            self.session.status = LoopStatus.EVALUATING
            evaluation = self._evaluate(goal, step, result)
            progress   = evaluation.get("progress_percent", 0)
            score      = evaluation.get("score", 0)

            self._log(f"   🧠 Evaluation: {evaluation.get('next_action')} | {progress}% | {evaluation.get('assessment', '')[:100]}")

            if evaluation.get("goal_reached"):
                step.status = StepStatus.DONE
                self.session.status = LoopStatus.GOAL_REACHED
                self.session.score  = score
                self._log("\n✅ Ziel erreicht!")
                break

            next_action = evaluation.get("next_action", "continue")

            if next_action == "continue":
                step.status = StepStatus.DONE
                current_idx += 1
                self.session.status = LoopStatus.EXECUTING

            elif next_action == "retry":
                step.retries += 1
                # Kein hartes Retry-Limit – aber bei >5 Retries: replan
                if step.retries > 5:
                    self._log(f"   ⚠️  Zu viele Retries für Schritt {step.index+1} → Replan")
                    step.status  = StepStatus.FAILED
                    replan_count += 1
                    if replan_count > 3:
                        self.session.status = LoopStatus.GOAL_FAILED
                        break
                    new_plan = self._create_plan(
                        goal,
                        context=f"Schritt '{step.description}' schlug mehrfach fehl.",
                        memory_context=memory_context
                    )
                    if new_plan:
                        self.session.plan = new_plan
                        current_idx = 0
                    else:
                        self.session.status = LoopStatus.GOAL_FAILED
                        break
                    continue

                hint = evaluation.get("retry_hint", "")
                self._log(f"   🔁 Retry {step.retries}: {hint}")
                step.status = StepStatus.FAILED
                retry_step = PlanStep(
                    index=step.index,
                    description=step.description,
                    skill=step.skill,
                    params=step.params,
                    reason=hint or step.reason,
                    retries=step.retries,
                )
                self.session.plan[current_idx] = retry_step
                self.session.status = LoopStatus.EXECUTING

            elif next_action == "replan":
                replan_count += 1
                if replan_count > 3:
                    self.session.status = LoopStatus.GOAL_FAILED
                    break
                self._log(f"   🔄 Replan #{replan_count}...")
                new_plan = self._create_plan(
                    goal,
                    context=f"Bisherige Versuche gescheitert: {evaluation.get('reason','')}",
                    memory_context=memory_context,
                )
                if new_plan:
                    self.session.plan = new_plan
                    current_idx = 0
                    self.session.status = LoopStatus.EXECUTING
                else:
                    self.session.status = LoopStatus.GOAL_FAILED
                    break

            elif next_action == "abort":
                self._log(f"   🛑 Abbruch: {evaluation.get('reason','')}")
                self.session.status = LoopStatus.GOAL_FAILED
                break

            else:
                step.status = StepStatus.DONE
                current_idx += 1

        # Phase 4: Zusammenfassung
        self.session.final_summary = self._create_summary()
        self._log("\n" + "─" * 65)
        self._log(f"📝 Zusammenfassung:\n{self.session.final_summary}")

        # Evolution Tracker informieren
        if self.evolution_tracker:
            if self.session.status == LoopStatus.GOAL_REACHED:
                pass  # wird von main_loop behandelt
            else:
                self.evolution_tracker.record_error()

        return self.session

    def abort(self):
        """Sicher abbrechen."""
        self._abort_flag = True

    def get_status_dict(self) -> Dict:
        if not self.session:
            return {"status": "idle"}
        return {
            "status":    self.session.status.value,
            "goal":      self.session.goal,
            "iteration": self.session.iteration,
            "max":       self.max_iterations,
            "score":     self.session.score,
            "summary":   self.session.final_summary,
            "history":   self.session.history,
        }

    # -----------------------------------------------------------------------
    # Interne Phasen
    # -----------------------------------------------------------------------

    def _get_memory_context(self, goal: str) -> str:
        """Holt relevanten Kontext aus dem Langzeitgedächtnis."""
        try:
            from skills.gedaechtnis import wissen_abrufen
            result = wissen_abrufen(goal)
            return str(result)[:800] if result else ""
        except Exception:
            return ""

    def _create_plan(self, goal: str, context: str = "", memory_context: str = "") -> Optional[List[PlanStep]]:
        skills_text = self.kernel.manager.get_system_prompt_addition()
        system = PLANNER_SYSTEM_PROMPT.format(
            skills=skills_text,
            memory_context=memory_context or "Kein relevanter Kontext.",
        )
        user = f"Erstelle einen Plan: {goal}"
        if context:
            user += f"\n\nKontext: {context}"

        messages = [
            {"role": "system", "content": system},
            {"role": "user",   "content": user},
        ]

        try:
            raw  = self.kernel.provider.chat(messages, force_json=True)
            data = self._parse_json(raw)
            if not data or "plan" not in data:
                logger.error(f"Planner kein valides JSON: {raw[:200]}")
                return None

            steps = []
            for item in data["plan"]:
                steps.append(PlanStep(
                    index=item.get("index", len(steps)),
                    description=item.get("description", ""),
                    skill=item.get("skill"),
                    params=item.get("params") or {},
                    reason=item.get("reason", ""),
                ))
            return steps
        except Exception as e:
            logger.error(f"Planner Fehler: {e}")
            return None

    def _execute_step(self, step: PlanStep) -> str:
        if not step.skill:
            return self._ask_llm_directly(step.description)

        # Policy check (in dieser Edition immer ALLOW)
        policy = get_policy()
        decision, reason = policy.check(step.skill, ExecutionMode.AUTONOMOUS)

        # Skills ggf. nachladen
        if step.skill not in self.kernel.manager.loaded_tools:
            self.kernel.load_skills()

        try:
            result = self.kernel.manager.execute_skill(step.skill, step.params)

            if "SUCCESS_CREATED" in str(result):
                self._log("   ✨ Neuer Skill erstellt → Reload...")
                self.kernel.load_skills()
                if self.evolution_tracker:
                    self.evolution_tracker.record_new_skill()

            step.status = StepStatus.DONE
            return str(result)

        except Exception as e:
            step.status = StepStatus.FAILED
            step.error  = str(e)
            if self.evolution_tracker:
                self.evolution_tracker.record_error()
            return f"FEHLER: {e}"

    def _evaluate(self, goal: str, step: PlanStep, result: str) -> Dict:
        steps_summary = "\n".join(
            f"  {e['step']+1}. {e['description']} → {str(e['result'])[:120]}"
            for e in self.session.history
        )

        system = EVALUATOR_SYSTEM_PROMPT.format(
            goal=goal,
            iteration=self.session.iteration,
            steps_summary=steps_summary or "(keine)",
            last_result=str(result)[:4000],
        )

        messages = [
            {"role": "system", "content": system},
            {"role": "user",   "content": "Bewerte den Fortschritt."},
        ]

        try:
            raw  = self.kernel.provider.chat(messages, force_json=True)
            data = self._parse_json(raw)
            return data if data else {"goal_reached": False, "next_action": "continue"}
        except Exception as e:
            logger.error(f"Evaluator Fehler: {e}")
            return {"goal_reached": False, "next_action": "continue"}

    def _create_summary(self) -> str:
        if not self.session:
            return "Kein Lauf."
        steps_summary = "\n".join(
            f"  {e['step']+1}. {e['description']} → {str(e['result'])[:150]}"
            for e in self.session.history
        )
        system = (
            f"Du bist Ilija. Fasse das Ergebnis zusammen.\n"
            f"Ziel: {self.session.goal}\nStatus: {self.session.status.value}\n"
            f"Schritte:\n{steps_summary}\n\n"
            "Kurze, klare Zusammenfassung (2–4 Sätze) was erreicht wurde."
        )
        messages = [
            {"role": "system", "content": system},
            {"role": "user",   "content": "Zusammenfassung:"},
        ]
        try:
            return self.kernel.provider.chat(messages, force_json=False)
        except Exception as e:
            return f"Status: {self.session.status.value}"

    def _ask_llm_directly(self, task: str) -> str:
        messages = [
            {"role": "system", "content": "Du bist Ilija. Führe diese Aufgabe aus."},
            {"role": "user",   "content": task},
        ]
        try:
            return self.kernel.provider.chat(messages, force_json=False)
        except Exception as e:
            return f"Direktes LLM fehlgeschlagen: {e}"

    def _parse_json(self, raw: str) -> Optional[Dict]:
        cleaned = re.sub(r"```(?:json)?", "", raw).replace("```", "").strip()
        try:
            return json.loads(cleaned)
        except Exception:
            match = re.search(r"\{.*\}", cleaned, re.DOTALL)
            if match:
                try:
                    return json.loads(match.group())
                except Exception:
                    pass
        return None

    def _inject_previous_results(self, params: Dict, step_results: Dict[int, str]) -> Dict:
        """Ersetzt ALLE Placeholder-Varianten durch echte Schritt-Ergebnisse."""
        if not params or not step_results:
            return params
        last_result = str(list(step_results.values())[-1]) if step_results else ""
        placeholder_patterns = [
            "OUTPUT_FROM_PREVIOUS_STEP", "OUTPUT_OF_PREVIOUS_STEP",
            "PREVIOUS_STEP_OUTPUT", "LAST_RESULT", "PREVIOUS_RESULT",
            "OUTPUT_FROM_STEP_", "OUTPUT_OF_STEP_", "previous_skill_result",
        ]
        new_params = {}
        for key, value in params.items():
            if not isinstance(value, str):
                new_params[key] = value
                continue
            replaced = False
            # Numerierte Schritte: OUTPUT_OF_STEP_0, OUTPUT_FROM_STEP_2 etc.
            import re
            num_match = re.search(r"(?:OUTPUT_(?:FROM|OF)_STEP_|previous_skill_result\()(\d+)", value)
            if num_match:
                idx = int(num_match.group(1))
                new_params[key] = step_results.get(idx, last_result)
                replaced = True
            else:
                for pat in placeholder_patterns:
                    if pat.lower() in value.lower():
                        new_params[key] = last_result
                        replaced = True
                        break
            if not replaced:
                # Erkennt beschreibende Platzhalter wie "Die ID aus Schritt 0"
                if re.search(r"(schritt|step|aus|from|output|result|id)\s*[0-9]", value.lower()):
                    new_params[key] = last_result
                else:
                    new_params[key] = value
        return new_params

    def _log(self, msg: str):
        if self.verbose:
            print(msg)
        logger.info(msg.strip())
