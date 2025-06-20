"""
agent_core.py
=============
Main orchestration class for the Agentic-AI-Assistant.

▪ Loads planner (Java) via JPype bridge
▪ Calls high-performance vector tool (C++) via ctypes
▪ Handles LLM interaction + tool routing

Requirements:
    - langchain, langgraph
    - jpype1           (Python ↔ Java bridge)
    - ctypes (std lib) (Python ↔ C++)
"""

from langgraph import Graph  # pip install langgraph
import jpype
import ctypes
from pathlib import Path

# --- Load Java Planner -------------------------------------------------------

JAR_PATH = Path(__file__).parent / "java" / "planner.jar"
if not jpype.isJVMStarted():
    jpype.startJVM(classpath=[str(JAR_PATH)])

JavaPlanner = jpype.JClass("com.trojan.ai.Planner")

# --- Load C++ Vector Utility -------------------------------------------------

lib_vec = ctypes.cdll.LoadLibrary(str(Path(__file__).parent / "cpp" / "libvector.so"))
lib_vec.cosine_similarity.restype = ctypes.c_double
lib_vec.cosine_similarity.argtypes = (ctypes.POINTER(ctypes.c_double),
                                      ctypes.POINTER(ctypes.c_double),
                                      ctypes.c_int)

def cosine_sim(py_vec1, py_vec2):
    """Wrapper for C++ cosine similarity"""
    length = len(py_vec1)
    array_type = ctypes.c_double * length
    v1 = array_type(*py_vec1)
    v2 = array_type(*py_vec2)
    return lib_vec.cosine_similarity(v1, v2, length)

# --- LangGraph Agent ---------------------------------------------------------

class AgenticAssistant:
    """
    High-level Agent that delegates:
        1. planning  → Java
        2. heavy math → C++
        3. LLM calls  → LangGraph tools
    """

    def __init__(self):
        self.planner = JavaPlanner()

        # Build LangGraph workflow
        self.graph = Graph()
        self.graph.add_node("plan", self.do_plan)
        self.graph.add_node("execute", self.do_execute)
        self.graph.set_entrypoint("plan")

    # --------------------------------------------------------------------- #
    # Node functions
    # --------------------------------------------------------------------- #

    def do_plan(self, user_msg: str) -> dict:
        """Call Java planner to decompose task."""
        steps = self.planner.createPlan(user_msg)
        return {"steps": steps, "idx": 0, "history": []}

    def do_execute(self, state: dict):
        """Execute each step (placeholder — will route tools later)."""
        steps, idx = state["steps"], state["idx"]
        if idx >= len(steps):
            return "DONE"

        current = steps[idx]
        # Very simple routing example
        if current.lower().startswith("vector"):
            result = cosine_sim([1, 0, 1], [0.5, 0, 0.5])
        else:
            result = f"LLM-TODO: {current}"

        state["history"].append(result)
        state["idx"] += 1
        return state

    # --------------------------------------------------------------------- #

    def run(self, prompt: str):
        """Run a full agent cycle."""
        return self.graph.run(prompt)

# ------------------------------------------------------------------------- #
# Quick CLI demo
# ------------------------------------------------------------------------- #
if __name__ == "__main__":
    assistant = AgenticAssistant()
    output = assistant.run("Compare vectors and then draft summary")
    print("Agent Output:", output)
