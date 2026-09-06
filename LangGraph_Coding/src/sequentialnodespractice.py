# Daily task planner
from langgraph.graph import StateGraph, START, END
from typing import TypedDict
import time

STEP_DELAY = 5
CHOICE_DELAY = 8


# Terminal colors. Font size cannot be changed from Python.
CYAN = "\033[36m"
DIM = "\033[2m"
RESET = "\033[0m"


def pause(seconds: int) -> None:
    text = "Moving to the next step..."
    print(f"{DIM}{CYAN}{text}{RESET}", end="", flush=True)
    time.sleep(seconds)
    # Erase using visible length only — color codes are not on screen
    print("\r" + " " * len(text), flush=True)

# Function for adding step delay between nodes
def say(msg: str, delay: int = STEP_DELAY) -> str:
    print(msg)
    pause(delay)
    return msg

# Function for asking a question and getting a response
def ask(msg: str, prompt: str, delay: int = CHOICE_DELAY) -> tuple[str, str]:
    print(msg)
    answer = input(prompt).strip().lower()
    pause(delay)
    return msg, answer


class State(TypedDict):
    name: str
    task: str
    answer: str

# Node 1
def goodmorning(state: State) -> State:
    msg = say("Good morning " + state["name"] + ", how are you? ⸜(｡˃ ᵕ ˂ )⸝♡")
    return {"task": msg}

# Node 2
def breakfast(state: State) -> State:
    msg, answer = ask("Are you having breakfast today?", "Type yes or no: ")
    return {
        "task": msg,
        "answer": answer,
    }

# Node 3
def after_breakfast(state: State):
    if state.get("answer", "").strip().lower() == "yes":
        return "coffee"
    return "studying"  # skip coffee

# Node 4
def coffee(state: State) -> State:
    msg = say("Here is your coffee.˗ˏˋ☕ˎˊ")
    return {"task": msg}

# Node 5
def studying(state: State) -> State:
    msg, answer = ask("What are you studying today?🤔💭", "Type your answer: ")
    return {
        "task": msg,
        "answer": answer,
    }

# Node 6
def after_studying(state: State):
    if state.get("answer", "").strip().lower() == "ai":
        return "studyai"
    return "studyfullstack"  # skip studyai

# Node 7
def studyai(state: State) -> State:
    msg = say("Let's study AI.📚💻✍🏼📓")
    return {"task": msg}

# Node 8
def studyfullstack(state: State) -> State:
    msg = say("Let's study any topic of fullstack.👩🏻‍💻📓✍🏻💡")
    return {"task": msg}

# Node 9
def lunch(state: State) -> State:
    msg = say("Let's have lunch. 🍽")
    return {"task": msg}

# Node 10
def evening(state: State) -> State:
    msg = say("Let's watch something funny and have popcorns.🌆🌙✨🪐🕯️🍿")
    return {"task": msg}

# Node 11
def dinner(state: State) -> State:
    msg = say("Enjoy your dinner.😋🍽️")
    return {"task": msg}

# Node 12
def sleep(state: State) -> State:
    msg = say("It's time to sleep.ᶻ 𝗓 𐰁 .ᐟ")
    return {"task": msg}

# Build the graph
graph = StateGraph(State)

graph.add_node("goodmorning", goodmorning)
graph.add_node("breakfast", breakfast)
graph.add_node("coffee", coffee)
graph.add_node("studying", studying)
graph.add_node("studyai", studyai)
graph.add_node("studyfullstack", studyfullstack)
graph.add_node("lunch", lunch)
graph.add_node("evening", evening)
graph.add_node("dinner", dinner)
graph.add_node("sleep", sleep)

# Add the edges
graph.add_edge(START, "goodmorning")
graph.add_edge("goodmorning", "breakfast")

graph.add_conditional_edges(
    "breakfast",          # from this node
    after_breakfast,      # decide next hop
    {
        "coffee": "coffee",
        "studying": "studying",
    },
)
graph.add_edge("coffee", "studying")

graph.add_conditional_edges(
    "studying",          # from this node
    after_studying,      # decide next hop
    {
        "studyai": "studyai",
        "studyfullstack": "studyfullstack",
    },
)
graph.add_edge("studyai", "lunch")
graph.add_edge("studyfullstack", "lunch")

graph.add_edge("lunch", "evening")
graph.add_edge("evening", "dinner")
graph.add_edge("dinner", "sleep")
graph.add_edge("sleep", END)

# Run the graph
app = graph.compile()

# Run the graph
result = app.invoke({
    "name": "Nishtha", "task": "", "answer": "yes"
})

print(result)
