# LangGraph Visual Guide

## Graph Structure Visualization

This document provides visual representations of how LangGraph graphs work.

---

## Basic Graph Flow (From Example)

```
                    START
                      |
                      v
              +---------------+
              |    Greet      |  <-- Node: greeting_node()
              | (welcomes     |      Updates: messages
              |  user)        |
              +---------------+
                      |
                      | (unconditional edge)
                      v
              +---------------+
              |   Analyze     |  <-- Node: sentiment_analysis_node()
              | (sentiment    |      Updates: sentiment, continue_chat
              |  detection)   |
              +---------------+
                      |
                      | (conditional edge)
                      v
                 [Decision]
                  /      \
       continue /        \ end
               /          \
              v            v
      +----------+    +-----------+
      | Respond  |    | Farewell  |  <-- Nodes
      | (reply)  |    | (goodbye) |
      +----------+    +-----------+
              |            |
              v            v
                    END
```

---

## State Flow Through Nodes

```
Input State → Node 1 → Updated State → Node 2 → Updated State → Node 3 → Final State
                ↓                        ↓                        ↓
         (reads state)              (reads state)          (reads state)
         (returns updates)          (returns updates)      (returns updates)
                ↓                        ↓                        ↓
         (state merged)             (state merged)         (state merged)
```

**Example from our chatbot:**

```
{                         greeting_node()               {
  messages: [],      →    returns                  →     messages: ["Hello..."],
  user_input: "hi",       { messages: [...] }            user_input: "hi",
  sentiment: "",                                         sentiment: "",
  continue_chat: true                                    continue_chat: true
}                                                      }
                                                            ↓
                         sentiment_analysis_node()      {
                         returns                   →     messages: ["Hello..."],
                         { sentiment: "neutral",         user_input: "hi",
                           continue_chat: true }         sentiment: "neutral",
                                                         continue_chat: true
                                                       }
```

---

## Edge Types Comparison

### Unconditional Edge
```
+--------+  always  +--------+
| Node A |--------->| Node B |
+--------+          +--------+
```

**Code:**
```python
graph.add_edge("node_a", "node_b")
```

**Use Case:** Sequential steps that always happen in order

---

### Conditional Edge
```
                +------------+
                | Routing    |
                | Function   |
                +------------+
                      |
         +------------+------------+
         |                         |
    returns "path_a"          returns "path_b"
         |                         |
         v                         v
   +--------+                 +--------+
   | Node A |                 | Node B |
   +--------+                 +--------+
```

**Code:**
```python
def routing_function(state):
    if state["condition"]:
        return "path_a"
    else:
        return "path_b"

graph.add_conditional_edges(
    "decision_node",
    routing_function,
    {
        "path_a": "node_a",
        "path_b": "node_b"
    }
)
```

**Use Case:** Decision points where the next step depends on state

---

## Common Patterns

### 1. Linear Pipeline
```
START → Node1 → Node2 → Node3 → END
```
Simple sequential processing, each node does one thing.

---

### 2. Decision Tree
```
          START
            |
            v
        +-------+
        | Check |
        +-------+
           / \
     yes  /   \  no
         /     \
        v       v
   +-----+   +-----+
   | Yes |   | No  |
   +-----+   +-----+
        \     /
         \   /
          \ /
           v
          END
```
Branch based on conditions, reconverge at the end.

---

### 3. Loop Pattern
```
    START
      |
      v
   +------+
   | Init |
   +------+
      |
      v
   +------+  <--+
   |Process|     |
   +------+      |
      |          |
      v          |
  [Done?] -------+ (no)
      |
    (yes)
      |
      v
     END
```
Iterative processing until a condition is met.

---

### 4. Parallel Fan-out/Fan-in
```
           START
             |
             v
         +-------+
         | Split |
         +-------+
          /  |  \
         /   |   \
        v    v    v
     +--+ +--+ +--+
     |A1| |A2| |A3|
     +--+ +--+ +--+
        \   |   /
         \  |  /
          v v v
        +-------+
        | Merge |
        +-------+
             |
             v
            END
```
Process multiple branches in parallel, then combine results.

---

## State Management Patterns

### 1. State Accumulation (using Annotated)
```python
from typing import Annotated
from operator import add

class State(TypedDict):
    items: Annotated[list, add]  # Appends to list
    count: int  # Replaces value
```

**How it works:**
- `items` with `add` reducer: Each node's items are appended
- `count` without reducer: Latest value replaces previous

### 2. State Replacement (default)
```python
class State(TypedDict):
    current_value: str  # Latest update wins
    timestamp: float    # Latest update wins
```

---

## Real-World Example Structure

### Customer Support Agent
```
                      START
                        |
                        v
                +----------------+
                | Classify Query |
                +----------------+
                        |
                 [Route by Type]
                   /    |    \
        technical /     |     \ billing
                 /      |      \
                v       v       v
         +------+  +-----+  +-------+
         |Tech  |  |Sales|  |Billing|
         |Agent |  |Agent|  |Agent  |
         +------+  +-----+  +-------+
                \     |     /
                 \    |    /
                  v   v   v
              +---------------+
              | Format Reply  |
              +---------------+
                      |
                      v
                     END
```

---

## Debugging Tips

### Visualize Your Graph
```python
# After compiling
app = graph.compile()

# Get mermaid diagram
print(app.get_graph().draw_mermaid())
```

### Add Logging to Nodes
```python
def my_node(state):
    print(f"[Node] Current state: {state}")
    result = process(state)
    print(f"[Node] Returning: {result}")
    return result
```

### Test Nodes Independently
```python
# Nodes are just functions!
def test_my_node():
    test_state = {"input": "test"}
    result = my_node(test_state)
    assert result["output"] == "expected"
```

---

## Best Practices Illustrated

### ✅ Good: Focused Nodes
```
START → Parse → Validate → Transform → Format → END
        (one job each)
```

### ❌ Bad: Monolithic Node
```
START → DoEverything → END
        (parsing, validation, transformation, formatting all in one)
```

---

### ✅ Good: Clear State Structure
```python
class State(TypedDict):
    input: str          # Clear purpose
    validated: bool     # Clear purpose
    result: dict        # Clear purpose
```

### ❌ Bad: Unclear State
```python
class State(TypedDict):
    data: Any          # What is this?
    temp: Any          # Temporary what?
    x: str             # What does x mean?
```

---

## Next Steps

1. Study the visual patterns above
2. Map your use case to a pattern
3. Sketch your graph on paper first
4. Implement nodes one at a time
5. Test each node independently
6. Connect with edges
7. Test the full graph

---

*Visual guide created to complement the LangGraph learning materials*
