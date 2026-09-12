# Increment counter until 10

from langgraph.graph import StateGraph, START, END
from typing import TypedDict
import time
class State(TypedDict):
    counter: int
    message: str

# Create Nodes
def increment(state: State) -> State:
    next_count = state["counter"] + 1
    message = f"Count is: {next_count}"
    # print message
    time.sleep(1)
    print(message)
    return {
        "counter": next_count,
        "message": message,
    }
# conditional node
def condition(state: State) -> State:
    if int(state["counter"]) < 10:
        return "continue"
    return "done"


# Build the graph
graph = StateGraph(State)

# Add nodes
graph.add_node("increment", increment)
graph.add_node("condition", condition)

# Add Edges
graph.add_edge(START, "increment")
graph.add_conditional_edges(
    "increment",
    condition,
    {
        "continue": "increment",
        "done": END
    }
)

# Lets create app
app = graph.compile()


# Run the app
result = app.invoke({
    "counter": 0,
    "message": "",
})

#print(result)