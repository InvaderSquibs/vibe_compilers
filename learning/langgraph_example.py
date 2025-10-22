#!/usr/bin/env python3
"""
LangGraph Quickstart Example
=============================

This example demonstrates the core concepts of LangGraph:
1. StateGraph - managing state across the workflow
2. Nodes - Python functions that process state
3. Edges - connecting nodes (conditional and unconditional)
4. Compilation and execution

This is a simple chatbot that:
- Greets the user
- Processes their message
- Decides whether to continue or end based on sentiment
- Says goodbye if ending
"""

from typing import TypedDict, Literal
from langgraph.graph import StateGraph, START, END


# Step 1: Define the State
# -------------------------
# State is shared across all nodes in the graph
class ChatState(TypedDict):
    """
    The state structure for our chat application.
    
    Each node can read from and write to these fields.
    """
    messages: list[str]  # Conversation history
    user_input: str  # Current user message
    sentiment: str  # Detected sentiment (positive, negative, neutral)
    continue_chat: bool  # Whether to continue the conversation


# Step 2: Define Nodes
# ---------------------
# Nodes are Python functions that take state and return state updates

def greeting_node(state: ChatState) -> dict:
    """
    First node: Greets the user and initializes the conversation.
    
    This demonstrates:
    - Reading from state (user_input)
    - Updating state (messages)
    """
    print("\n🤖 [Greeting Node] Welcoming user...")
    
    greeting = f"Hello! You said: '{state['user_input']}'"
    messages = state.get("messages", [])
    messages.append(greeting)
    
    return {"messages": messages}


def sentiment_analysis_node(state: ChatState) -> dict:
    """
    Second node: Analyzes the sentiment of user input.
    
    This demonstrates:
    - Processing state data
    - Making decisions based on content
    - Updating multiple state fields
    """
    print("🤖 [Sentiment Node] Analyzing sentiment...")
    
    user_input = state["user_input"].lower()
    
    # Simple sentiment analysis (in real app, use an LLM or sentiment model)
    if any(word in user_input for word in ["bye", "goodbye", "exit", "quit"]):
        sentiment = "farewell"
        continue_chat = False
    elif any(word in user_input for word in ["happy", "great", "awesome", "love"]):
        sentiment = "positive"
        continue_chat = True
    elif any(word in user_input for word in ["sad", "bad", "hate", "angry"]):
        sentiment = "negative"
        continue_chat = True
    else:
        sentiment = "neutral"
        continue_chat = True
    
    print(f"   Detected sentiment: {sentiment}")
    
    return {
        "sentiment": sentiment,
        "continue_chat": continue_chat
    }


def response_node(state: ChatState) -> dict:
    """
    Third node: Generates an appropriate response based on sentiment.
    
    This demonstrates:
    - Using state to make contextual decisions
    - Adding to conversation history
    """
    print("🤖 [Response Node] Generating response...")
    
    sentiment = state["sentiment"]
    messages = state["messages"]
    
    # Generate response based on sentiment
    if sentiment == "positive":
        response = "That's wonderful! I'm glad you're feeling good! 😊"
    elif sentiment == "negative":
        response = "I'm sorry to hear that. I hope things get better! 💙"
    elif sentiment == "neutral":
        response = "I see. Tell me more about that."
    else:
        response = "Thanks for chatting! It was nice talking to you."
    
    messages.append(response)
    
    return {"messages": messages}


def farewell_node(state: ChatState) -> dict:
    """
    Final node: Says goodbye to the user.
    
    This demonstrates:
    - Terminal node that ends the conversation
    - Cleaning up or finalizing state
    """
    print("🤖 [Farewell Node] Saying goodbye...")
    
    messages = state["messages"]
    messages.append("Goodbye! Have a great day! 👋")
    
    return {"messages": messages}


# Step 3: Define Routing Logic
# -----------------------------
# Conditional edges use routing functions to decide the next node

def should_continue(state: ChatState) -> Literal["continue", "end"]:
    """
    Routing function for conditional edges.
    
    This determines whether to continue chatting or end the conversation.
    Returns a string key that maps to the next node.
    """
    if state["continue_chat"]:
        return "continue"
    else:
        return "end"


# Step 4: Build the Graph
# ------------------------

def create_chat_graph() -> StateGraph:
    """
    Creates and returns the compiled chat graph.
    
    This demonstrates:
    - Creating a StateGraph
    - Adding nodes
    - Adding edges (unconditional and conditional)
    - Compiling the graph
    """
    # Initialize the graph with our state type
    graph = StateGraph(ChatState)
    
    # Add nodes to the graph
    # Each node is a function that processes state
    graph.add_node("greet", greeting_node)
    graph.add_node("analyze", sentiment_analysis_node)
    graph.add_node("respond", response_node)
    graph.add_node("farewell", farewell_node)
    
    # Add edges to define the flow
    # Unconditional edges: Always go from A -> B
    graph.add_edge(START, "greet")  # Start with greeting
    graph.add_edge("greet", "analyze")  # Greeting -> Analysis
    
    # Conditional edge: Route based on sentiment analysis
    # The should_continue function returns "continue" or "end"
    # This determines whether we respond or say farewell
    graph.add_conditional_edges(
        "analyze",  # From this node
        should_continue,  # Use this function to decide
        {
            "continue": "respond",  # If "continue", go to respond node
            "end": "farewell"  # If "end", go to farewell node
        }
    )
    
    # More unconditional edges
    graph.add_edge("respond", END)  # Response leads to end
    graph.add_edge("farewell", END)  # Farewell leads to end
    
    # Compile the graph
    # This validates the structure and prepares it for execution
    return graph.compile()


# Step 5: Execute the Graph
# --------------------------

def run_example(user_message: str):
    """
    Runs the chat graph with a user message.
    
    This demonstrates:
    - Compiling a graph
    - Invoking with initial state
    - Accessing the final state
    """
    print("\n" + "="*60)
    print(f"User message: '{user_message}'")
    print("="*60)
    
    # Create the compiled graph
    app = create_chat_graph()
    
    # Initial state
    initial_state = {
        "messages": [],
        "user_input": user_message,
        "sentiment": "",
        "continue_chat": True
    }
    
    # Execute the graph
    # The graph will run from START to END, updating state along the way
    final_state = app.invoke(initial_state)
    
    # Display results
    print("\n" + "-"*60)
    print("Final Conversation:")
    print("-"*60)
    for msg in final_state["messages"]:
        print(f"  {msg}")
    print("\n" + "="*60)
    
    return final_state


# Main execution
if __name__ == "__main__":
    print("""
╔══════════════════════════════════════════════════════════╗
║          LangGraph Quickstart Example                    ║
║                                                          ║
║  This example demonstrates:                              ║
║  • StateGraph for managing state                         ║
║  • Nodes as Python functions                             ║
║  • Unconditional and conditional edges                   ║
║  • Graph compilation and execution                       ║
╚══════════════════════════════════════════════════════════╝
    """)
    
    # Example 1: Positive message (will continue)
    print("\n📝 Example 1: Positive Message")
    run_example("Hello! I'm having a great day!")
    
    # Example 2: Negative message (will continue)
    print("\n📝 Example 2: Negative Message")
    run_example("I'm feeling a bit sad today")
    
    # Example 3: Farewell message (will end)
    print("\n📝 Example 3: Farewell Message")
    run_example("Thanks for your help, goodbye!")
    
    print("\n✅ All examples completed successfully!")
    print("\nKey Takeaways:")
    print("  1. StateGraph manages shared state across all nodes")
    print("  2. Nodes are simple Python functions that update state")
    print("  3. Unconditional edges always follow the same path")
    print("  4. Conditional edges use routing functions to decide flow")
    print("  5. Compile the graph before execution")
    print("  6. Invoke executes the graph from START to END")
