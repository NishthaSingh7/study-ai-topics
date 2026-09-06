from langgraph.graph import StateGraph, START, END
from typing import TypedDict

# state is the data the graph shares between nodes
# key: type
# {"message": "Nishtha"}
class State(TypedDict):
    message: str

# node is a function that receives the current state and returns the new state
# {"message": "Hello Nishtha"}
def hello(state: State):
    return {
        "message": "Hello " + state["message"]
    }
''' 
LangGraph merges that back into state. 
The old "Nishtha" is replaced by "Hello Nishtha".
'''

# Build the graph
graph = StateGraph(State)  # this graph uses the State shape.

graph.add_node("hello", hello) # register the function under the name "hello".

graph.add_edge(START, "hello") # first hop is into that node
graph.add_edge("hello", END)  # after it runs, stop

# Flow:  START  →  hello  →  END

# Compile and run the graph
app = graph.compile()

# invoke the graph with the initial state
result = app.invoke({
    "message": "Nishtha"
})

print(result)

'''
Execution:
    Start with {"message": "Nishtha"}.
    hello runs → {"message": "Hello Nishtha"}.
Graph ends.
'''