# LangGraph Core Concepts

## Overview
LangGraph is a library built on top of LangChain for building stateful, multi-actor applications with LLMs. It extends the LangChain Expression Language with the ability to coordinate multiple chains (or actors) across multiple steps of computation in a cyclic manner.

## Core Components

### 1. StateGraph
**What is it?**
A StateGraph is the central class in LangGraph that manages application state throughout the execution of a graph. It's a state machine where:
- State is passed between nodes
- Each node can read from and write to the state
- State persists across the entire graph execution
- State is defined using TypedDict or Pydantic models

**Key Features:**
- Centralized state management across all nodes
- Type-safe state definitions
- Automatic state propagation between nodes
- Support for state reducers (how to merge updates)

**How it manages state:**
- State is initialized at the start of graph execution
- Each node receives the current state as input
- Nodes return updates to the state
- Updates are merged into the global state using reducers
- The updated state is passed to the next node(s)

### 2. Nodes
**What are they?**
Nodes are Python functions that represent individual steps or operations in your graph. Each node:
- Takes the current state as input
- Performs some operation (call an LLM, process data, make decisions)
- Returns updates to the state

**Characteristics:**
- Simple Python functions with a specific signature
- Function signature: `def node_name(state: StateType) -> dict`
- Can be synchronous or asynchronous
- Can call LLMs, APIs, or perform any Python operation
- Must return a dictionary with state updates

**Example Node Structure:**
```python
def my_node(state: GraphState) -> dict:
    # Access state
    current_data = state["data"]
    
    # Perform operation
    result = process(current_data)
    
    # Return state update
    return {"data": result, "step": "processed"}
```

### 3. Edges
**What are they?**
Edges define the flow and connections between nodes in the graph. They determine which node executes next.

**Types of Edges:**

#### Unconditional Edges
- Direct connections from one node to another
- Always follow the same path
- Syntax: `graph.add_edge("node_a", "node_b")`
- Node A always leads to Node B

#### Conditional Edges
- Dynamic routing based on state or conditions
- Use a routing function to determine next node
- Syntax: `graph.add_conditional_edges("node_a", routing_function, mapping)`
- The routing function examines state and returns a key
- The mapping dictionary maps keys to node names

**Routing Function Example:**
```python
def route_decision(state: GraphState) -> str:
    if state["should_continue"]:
        return "continue"
    else:
        return "end"

# Mapping
{
    "continue": "next_node",
    "end": END
}
```

#### Special Edges
- **START**: Entry point to the graph
- **END**: Exit point from the graph
- `add_edge(START, "first_node")`: Defines where execution begins
- `add_edge("last_node", END)`: Defines where execution ends

### 4. Compilation and Execution

**Compilation:**
The graph must be compiled before execution:
```python
app = graph.compile()
```

**What compilation does:**
- Validates the graph structure (no orphaned nodes, proper START/END)
- Optimizes the execution plan
- Creates an executable application
- Enables features like checkpointing and streaming

**Execution:**
Once compiled, invoke the graph:
```python
result = app.invoke(initial_state)
```

**Execution Flow:**
1. Initialize state with provided input
2. Start at the START node
3. Execute nodes following edges
4. Update state after each node
5. Continue until reaching END
6. Return final state

**Advanced Execution:**
- **Streaming**: `app.stream(input)` - Stream intermediate results
- **Async**: `await app.ainvoke(input)` - Async execution
- **Checkpointing**: Save/restore state at any point for persistence

## State Management Details

### State Reducers
Control how state updates are merged:
```python
from typing import Annotated
from operator import add

class State(TypedDict):
    messages: Annotated[list, add]  # Appends new messages
    count: int  # Replaces count value
```

### State Types
- **TypedDict**: Simple, type-safe dictionaries
- **Pydantic Models**: Complex validation and schemas
- **Custom Classes**: Advanced state management

## Best Practices

1. **Keep nodes focused**: Each node should do one thing well
2. **Use type hints**: Make state structure clear with TypedDict
3. **Handle errors gracefully**: Add error handling in nodes
4. **Test nodes independently**: Nodes are just functions
5. **Use conditional edges wisely**: Don't overcomplicate routing
6. **Document state structure**: Clear comments on what each field means
7. **Consider state size**: Don't store massive objects in state

## Common Patterns

### Linear Pipeline
```
START -> Node1 -> Node2 -> Node3 -> END
```

### Conditional Branching
```
START -> Node1 -> (condition) -> Node2A or Node2B -> END
```

### Loops/Cycles
```
START -> Node1 -> (condition) -> Node2 -> Node1 (loop) or END
```

### Parallel Processing
```
START -> Node1 -> [Node2A, Node2B, Node2C] -> Aggregate -> END
```

## Advantages of LangGraph

1. **State Management**: Built-in state handling across complex workflows
2. **Flexibility**: Mix LLM calls with traditional code
3. **Cyclical Flows**: Support for loops and iterative processes
4. **Human-in-the-Loop**: Easy to add approval steps
5. **Persistence**: Built-in checkpointing for long-running tasks
6. **Streaming**: Real-time output as graph executes
7. **Debugging**: Clear visualization of graph structure

## When to Use LangGraph

- **Complex LLM workflows** with multiple steps
- **Agent systems** that need to reason and act iteratively
- **Multi-step pipelines** with conditional logic
- **Stateful conversations** that maintain context
- **Human-in-the-loop** applications requiring approval
- **Retry/error handling** with sophisticated logic

## Summary

- **StateGraph**: The container that manages state throughout execution
- **Nodes**: Python functions that process state and return updates
- **Edges**: Connections that define execution flow (conditional or unconditional)
- **Compilation**: Prepares the graph for execution
- **Execution**: Runs the graph from START to END, updating state along the way

LangGraph provides a powerful framework for building complex, stateful applications with LLMs while keeping the code clean, testable, and maintainable.
