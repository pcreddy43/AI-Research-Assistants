# Restore controller for import compatibility
def controller(question, session_id):
    state = MultiStepState(question, session_id)
    state = planner_node(state)
    while not state.finished:
        state = executor_node(state)
    result = synthesize_node(state)
    return result
import json

# Example state structure
class MultiStepState:
    def __init__(self, question, session_id):
        self.question = question
        self.session_id = session_id
        self.plan = None
        self.current_step = 0
        self.contexts = {}
        self.finished = False

# Planner node: produces a plan
def planner_node(state: MultiStepState):
    # For demo, always return the same plan
    state.plan = {"steps": ["rag", "web", "llm"]}
    state.current_step = 0
    return state

# Executor node: executes steps in order
def executor_node(state: MultiStepState):
    steps = state.plan["steps"]
    if state.current_step >= len(steps):
        state.finished = True
        return state
    step = steps[state.current_step]
    # Simulate step execution and context storage
    state.contexts[step] = f"Result of {step} for question: {state.question}"
    state.current_step += 1
    return state

# Synthesize node: combines all contexts
def synthesize_node(state: MultiStepState):
    summary = " | ".join([v for k, v in state.contexts.items()])
    return {"summary": summary, "session_id": state.session_id}

# Controller: main graph logic


def streaming_controller(question, session_id):
    state = MultiStepState(question, session_id)
    # Yield planner event
    state = planner_node(state)
    yield {"event": "planner", "data": f"Plan: {state.plan['steps']}"}
    # Yield each executor step
    while not state.finished:
        step = state.plan["steps"][state.current_step]
        state = executor_node(state)
        yield {"event": step, "data": state.contexts[step]}
    # Yield synthesize event
    result = synthesize_node(state)
    yield {"event": "synthesize", "data": result["summary"]}
    yield {"event": "end", "data": "Done"}
