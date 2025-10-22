# LangGraph Quick Reference Cheat Sheet

## Setup

```python
from typing import TypedDict
from langgraph.graph import StateGraph, START, END
```

---

## Define State

```python
class MyState(TypedDict):
    field1: str
    field2: int
    field3: list[str]
```

### With Reducers (for accumulation)
```python
from typing import Annotated
from operator import add

class MyState(TypedDict):
    messages: Annotated[list, add]  # Appends items
    count: int  # Replaces value
```

---

## Create Graph

```python
graph = StateGraph(MyState)
```

---

## Define Nodes (Functions)

```python
def my_node(state: MyState) -> dict:
    """Node that processes state"""
    # Read from state
    value = state["field1"]
    
    # Do work
    result = process(value)
    
    # Return state updates (only changed fields)
    return {"field2": result}
```

### Async Node
```python
async def my_async_node(state: MyState) -> dict:
    result = await async_operation()
    return {"field1": result}
```

---

## Add Nodes to Graph

```python
graph.add_node("node_name", my_node_function)
graph.add_node("another_node", another_function)
```

---

## Add Edges

### Unconditional Edge
```python
# Always go from node_a to node_b
graph.add_edge("node_a", "node_b")
```

### Entry Point
```python
# Start execution here
graph.add_edge(START, "first_node")
```

### Exit Point
```python
# End execution here
graph.add_edge("last_node", END)
```

### Conditional Edge
```python
def routing_function(state: MyState) -> str:
    """Return key to determine next node"""
    if state["condition"]:
        return "option_a"
    return "option_b"

graph.add_conditional_edges(
    "decision_node",
    routing_function,
    {
        "option_a": "node_a",
        "option_b": "node_b",
        "end": END
    }
)
```

---

## Compile Graph

```python
app = graph.compile()
```

### With Checkpointing (for persistence)
```python
from langgraph.checkpoint.memory import MemorySaver

checkpointer = MemorySaver()
app = graph.compile(checkpointer=checkpointer)
```

---

## Execute Graph

### Basic Invoke
```python
initial_state = {
    "field1": "value",
    "field2": 0,
    "field3": []
}

final_state = app.invoke(initial_state)
print(final_state)
```

### With Config (for checkpointing)
```python
config = {"configurable": {"thread_id": "1"}}
result = app.invoke(initial_state, config=config)
```

### Async Invoke
```python
result = await app.ainvoke(initial_state)
```

### Stream Results
```python
for state in app.stream(initial_state):
    print(state)
```

### Stream with Config
```python
config = {"configurable": {"thread_id": "1"}}
for state in app.stream(initial_state, config=config):
    print(state)
```

---

## Common Patterns

### Linear Pipeline
```python
graph.add_edge(START, "step1")
graph.add_edge("step1", "step2")
graph.add_edge("step2", "step3")
graph.add_edge("step3", END)
```

### Conditional Branch
```python
def route(state):
    return "path_a" if state["condition"] else "path_b"

graph.add_edge(START, "decision")
graph.add_conditional_edges(
    "decision",
    route,
    {"path_a": "node_a", "path_b": "node_b"}
)
graph.add_edge("node_a", END)
graph.add_edge("node_b", END)
```

### Loop
```python
def should_continue(state):
    return "continue" if not state["done"] else "finish"

graph.add_edge(START, "process")
graph.add_conditional_edges(
    "process",
    should_continue,
    {
        "continue": "process",  # Loop back
        "finish": END
    }
)
```

---

## Debugging

### Visualize Graph (Mermaid)
```python
app = graph.compile()
print(app.get_graph().draw_mermaid())
```

### Get Graph Info
```python
graph_info = app.get_graph()
print(graph_info.nodes)  # List of nodes
print(graph_info.edges)  # List of edges
```

### Add Logging
```python
def my_node(state):
    print(f"[DEBUG] Entering node with state: {state}")
    result = process(state)
    print(f"[DEBUG] Returning: {result}")
    return result
```

---

## Type Hints Reference

```python
from typing import TypedDict, Literal, Annotated
from operator import add

# Basic state
class State(TypedDict):
    field: str

# With optional fields
class State(TypedDict, total=False):
    required_field: str
    optional_field: int

# With reducers
class State(TypedDict):
    items: Annotated[list, add]

# Routing return type
def route(state) -> Literal["path_a", "path_b"]:
    return "path_a"
```

---

## Error Handling

```python
def safe_node(state: MyState) -> dict:
    try:
        result = risky_operation(state)
        return {"result": result, "error": None}
    except Exception as e:
        return {"result": None, "error": str(e)}
```

---

## Complete Minimal Example

```python
from typing import TypedDict
from langgraph.graph import StateGraph, START, END

# 1. Define state
class State(TypedDict):
    input: str
    output: str

# 2. Define nodes
def process(state: State) -> dict:
    return {"output": state["input"].upper()}

# 3. Build graph
graph = StateGraph(State)
graph.add_node("process", process)
graph.add_edge(START, "process")
graph.add_edge("process", END)

# 4. Compile
app = graph.compile()

# 5. Execute
result = app.invoke({"input": "hello", "output": ""})
print(result)  # {"input": "hello", "output": "HELLO"}
```

---

## Common Mistakes to Avoid

❌ **Forgetting to return state updates**
```python
def bad_node(state):
    result = process(state)
    # Oops! Forgot to return
```

✅ **Always return dict with updates**
```python
def good_node(state):
    result = process(state)
    return {"field": result}
```

---

❌ **Modifying state directly**
```python
def bad_node(state):
    state["field"] = "new_value"  # Don't do this!
    return state
```

✅ **Return new values**
```python
def good_node(state):
    return {"field": "new_value"}
```

---

❌ **Not handling missing keys**
```python
def bad_node(state):
    value = state["maybe_missing"]  # Could crash
```

✅ **Use .get() with defaults**
```python
def good_node(state):
    value = state.get("maybe_missing", "default")
```

---

## Quick Links

- 📚 Concepts: `langgraph_concepts.md`
- 💡 Example: `langgraph_example.py`
- 👥 Team Summary: `team_summary.md`
- 🎨 Visual Guide: `visual_guide.md`
- 🌐 Official Docs: https://langchain-ai.github.io/langgraph/

---

*Keep this cheat sheet handy while building your first graphs!*
