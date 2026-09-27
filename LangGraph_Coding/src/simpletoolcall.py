# a simple tool calling agent

# Import necessary libraries
from dotenv import find_dotenv, load_dotenv
from langgraph.graph import StateGraph, START, END, MessagesState
from langchain_openai import ChatOpenAI

# Import the tool class from the langchain_core module
from langchain_core.tools import tool
from langgraph.prebuilt import ToolNode

load_dotenv(find_dotenv())

# Each tool's name and docstring is what the model uses to choose.
#The choice is the model comparing your sentence to those descriptions. 
# A clear docstring is what makes the match reliable.
@tool
def multiply(a: int, b: int) -> int:
    """Multiply two numbers together."""
    return a * b

@tool
def add(a: int, b: int) -> int:
    """Add two numbers together."""
    return a + b

# List of tools to use
tools_list = [multiply, add]

# bind_tools only describes the tools. It does not run them.
# attach the tools to the LLM as tools_list
llm = ChatOpenAI(model="gpt-4o-mini").bind_tools(tools_list)


# Define the model function - AGENT NODE
def call_model(state: MessagesState):
    response = llm.invoke(
        state["messages"]
    )
    return {
        "messages": [response]
    }

# Define the should continue function and 
# checks if the model has requested a tool call
def should_continue(state):
    last_message = state["messages"][-1]

    if last_message.tool_calls:
        return "tools"
    else:
        return END

# ToolNode runs whichever tool name the model requested.
tools = ToolNode(tools_list)


# Create the graph
graph = StateGraph(MessagesState)

# Add the nodes to the graph
graph.add_node("agent", call_model)
graph.add_node("tools", tools)

graph.add_edge(START, "agent")

# Add the conditional edges to the graph
graph.add_conditional_edges(
    "agent",
    should_continue,
    {
        "tools": "tools",
        END: END
    }
)

graph.add_edge("tools", "agent")

app = graph.compile()

questions = [
    "What is 12 multiplied by 7?",
    "What is 12 plus 7?",
]

for question in questions:
    result = app.invoke({
        "messages": [
            {
                "role": "user",
                "content": question,
            }
        ]
    })

    print("USER:", question)
    for message in result["messages"]:
        if message.type == "ai" and message.tool_calls:
            call = message.tool_calls[0]
            print("CHOSE:", call["name"], call["args"])
        elif message.type == "tool":
            print("RESULT:", message.content)
    print("ANSWER:", result["messages"][-1].content)
    print()


# User:
# "What is 12 × 7?"
#        ↓
#      Agent
#        ↓
# LLM decides:
# "I need multiply tool"
#        ↓
#     ToolNode
#        ↓
# multiply(12, 7)
#        ↓
# ToolMessage:
# 84
#        ↓
#      Agent
#        ↓
# LLM sees 84
#        ↓
# "84"
#        ↓
#      END