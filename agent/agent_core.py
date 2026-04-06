"""
agent_core.py
=============
Main orchestration class for the Agentic-AI-Assistant.

▪ Loads planner (Java) via JPype bridge when the compiled JAR is present
▪ Calls high-performance vector tool (C++) via ctypes when libvector.so exists
▪ Falls back to pure-Python equivalents when native artifacts are unavailable
▪ Handles tool routing via LangGraph StateGraph

Requirements (see requirements.txt):
    - langgraph    (graph orchestration)
    - jpype1       (Python ↔ Java bridge, optional at runtime)
    - ctypes       (stdlib – Python ↔ C++)
"""

import ctypes
import logging
import math
from pathlib import Path
from typing import TypedDict

from langgraph.graph import END, StateGraph

log = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Java Planner (optional – requires compiled agent/java/planner.jar)
# ---------------------------------------------------------------------------
_JavaPlanner = None
_JAR_PATH = Path(__file__).parent / "java" / "planner.jar"

try:
    import jpype  # noqa: PLC0415

    if _JAR_PATH.exists():
        if not jpype.isJVMStarted():
            jpype.startJVM(classpath=[str(_JAR_PATH)])
        _JavaPlanner = jpype.JClass("com.trojan.ai.Planner")
        log.info("Java planner loaded from %s", _JAR_PATH)
    else:
        log.info("planner.jar not found at %s – using Python fallback planner.", _JAR_PATH)
except Exception as _e:  # noqa: BLE001
    log.warning("Java planner unavailable (%s) – using Python fallback planner.", _e)


# ---------------------------------------------------------------------------
# C++ Vector Utility (optional – requires compiled agent/cpp/libvector.so)
# ---------------------------------------------------------------------------
_lib_vec = None
_LIB_PATH = Path(__file__).parent / "cpp" / "libvector.so"

try:
    if _LIB_PATH.exists():
        _lib_vec = ctypes.cdll.LoadLibrary(str(_LIB_PATH))
        _lib_vec.cosine_similarity.restype = ctypes.c_double
        _lib_vec.cosine_similarity.argtypes = (
            ctypes.POINTER(ctypes.c_double),
            ctypes.POINTER(ctypes.c_double),
            ctypes.c_int,
        )
        log.info("C++ vector library loaded from %s", _LIB_PATH)
    else:
        log.info("libvector.so not found at %s – using pure-Python cosine similarity.", _LIB_PATH)
except Exception as _e:  # noqa: BLE001
    log.warning("C++ vector library unavailable (%s) – using pure-Python fallback.", _e)


def cosine_sim(py_vec1: list, py_vec2: list) -> float:
    """Return cosine similarity.  Uses C++ library when available."""
    if _lib_vec is not None:
        length = len(py_vec1)
        array_type = ctypes.c_double * length
        v1 = array_type(*py_vec1)
        v2 = array_type(*py_vec2)
        return _lib_vec.cosine_similarity(v1, v2, length)

    # Pure-Python fallback
    dot = sum(a * b for a, b in zip(py_vec1, py_vec2))
    mag1 = math.sqrt(sum(a * a for a in py_vec1))
    mag2 = math.sqrt(sum(b * b for b in py_vec2))
    return dot / (mag1 * mag2) if mag1 * mag2 else 0.0


# ---------------------------------------------------------------------------
# Web-search tool (optional – requires duckduckgo-search)
# ---------------------------------------------------------------------------
def _web_search(query: str) -> str:
    try:
        from agent.tools.web_search import search_and_summarize  # noqa: PLC0415

        return search_and_summarize(query)
    except Exception as exc:  # noqa: BLE001
        return f"[web_search unavailable: {exc}]"


# ---------------------------------------------------------------------------
# LangGraph State
# ---------------------------------------------------------------------------
class AgentState(TypedDict):
    prompt: str
    steps: list
    idx: int
    history: list


# ---------------------------------------------------------------------------
# AgenticAssistant
# ---------------------------------------------------------------------------
class AgenticAssistant:
    """
    High-level Agent that delegates:
        1. planning          → Java planner (falls back to keyword heuristic)
        2. vector similarity → C++ library  (falls back to pure Python)
        3. web search        → DuckDuckGo tool
        4. orchestration     → LangGraph StateGraph
    """

    def __init__(self) -> None:
        self._java_planner = _JavaPlanner() if _JavaPlanner is not None else None

        graph = StateGraph(AgentState)
        graph.add_node("plan", self._do_plan)
        graph.add_node("execute", self._do_execute)
        graph.set_entry_point("plan")
        graph.add_edge("plan", "execute")
        graph.add_conditional_edges(
            "execute",
            lambda s: "end" if s["idx"] >= len(s["steps"]) else "execute",
            {"execute": "execute", "end": END},
        )
        self._graph = graph.compile()

    # ---------------------------------------------------------------------- #
    # Private helpers
    # ---------------------------------------------------------------------- #

    def _plan_fallback(self, prompt: str) -> list:
        """Keyword-based planner used when the Java JAR is not present."""
        steps: list = []
        lower = prompt.lower()
        if "vector" in lower:
            steps.append("vector_similarity")
        if "search" in lower or "web" in lower:
            steps.append("web_search")
        steps.append("llm_summary")
        return steps

    # ---------------------------------------------------------------------- #
    # LangGraph node functions
    # ---------------------------------------------------------------------- #

    def _do_plan(self, state: AgentState) -> AgentState:
        """Decompose the user prompt into an ordered list of steps."""
        prompt = state["prompt"]
        if self._java_planner is not None:
            steps = [str(s) for s in self._java_planner.createPlan(prompt)]
        else:
            steps = self._plan_fallback(prompt)
        log.debug("Plan: %s", steps)
        return {"prompt": prompt, "steps": steps, "idx": 0, "history": []}

    def _do_execute(self, state: AgentState) -> AgentState:
        """Execute the next pending step and advance the index."""
        steps = state["steps"]
        idx = state["idx"]
        history = list(state.get("history", []))

        if idx >= len(steps):
            return state

        current = steps[idx]
        if current == "vector_similarity":
            score = cosine_sim([1, 0, 1], [0.5, 0, 0.5])
            result = f"cosine_similarity([1,0,1], [0.5,0,0.5]) = {score:.4f}"
        elif current == "web_search":
            result = _web_search(state["prompt"])
        else:
            result = f"[{current}] Processed: {state['prompt'][:120]}"

        log.debug("Step %d (%s): %s", idx, current, result)
        history.append(result)
        return {"prompt": state["prompt"], "steps": steps, "idx": idx + 1, "history": history}

    # ---------------------------------------------------------------------- #
    # Public API
    # ---------------------------------------------------------------------- #

    def run(self, prompt: str) -> str:
        """Run a full agent cycle and return the combined output."""
        initial: AgentState = {"prompt": prompt, "steps": [], "idx": 0, "history": []}
        final_state = self._graph.invoke(initial)
        history = final_state.get("history", [])
        return "\n".join(str(h) for h in history) if history else f"[HelixAgent] {prompt}"


# ---------------------------------------------------------------------------
# Quick CLI demo
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    assistant = AgenticAssistant()
    output = assistant.run("Compare vectors and then draft summary")
    print("Agent Output:", output)
