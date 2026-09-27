# Basic LLM Graph

# Import necessary libraries
from dotenv import find_dotenv, load_dotenv
from langgraph.graph import StateGraph, START, END, MessagesState
# Import the ChatOpenAI class from the langchain_openai module
from langchain_openai import ChatOpenAI

# Load OPENAI_API_KEY from the project .env (walks up from this file)
# print(load_dotenv(find_dotenv()))
load_dotenv(find_dotenv())

# Initialize the LLM with the gpt-4o-mini model
llm = ChatOpenAI( model = "gpt-4o-mini")


# call model and get response
def call_model(state: MessagesState):
    response = llm.invoke(
        state["messages"]
    )
    return {
        "messages": [response]
    }


# Create the graph 
graph = StateGraph(MessagesState)

# Add the nodes to the graph
graph.add_node( "model", call_model)


graph.add_edge(START, "model")
graph.add_edge("model", END)

# Compile the graph
app = graph.compile()

# Invoke the graph
result = app.invoke({
    "messages": [
        {
           "role": "user",
           "content": "Tell all workplace rules to follow as a SDE 2 Engineer in bullet points."
        }
    ]
})

# Print the response
print(result["messages"][-1].content)


# User
#  ↓
# MessagesState
#  ↓
# Model Node
#  ↓
# AIMessage
#  ↓
# END