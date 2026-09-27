from typing import TypedDict

from langgraph.graph import StateGraph, START, END

from llm_config import llm
from tool_agent import calculator, mock_search


class AgentState(TypedDict):
    query: str
    reasoning: str
    action: str
    observation: str
    answer: str


def reason_node(state: AgentState):
    query = state["query"]

    response = llm.invoke(
        f"""
You are a ReAct reasoning agent.

User query: {query}

Decide what action is required.
For any arithmetic or mathematical calculation, you MUST choose calculator.
For requests asking for information or research, choose search.
Only choose direct_answer when neither tool is appropriate.

Choose exactly one:
- calculator
- search
- direct_answer

Return exactly:

Reason: <short reason>
Action: <one action>

"""
    )

    content = response.content

    print("\n🧠 REASON")
    print(content)

    action = "direct_answer"

    for line in content.splitlines():
        if line.startswith("Action:"):
            action = line.split(":", 1)[1].strip()

    return {
        "reasoning": content,
        "action": action
    }


def action_node(state: AgentState):
    action = state["action"]
    query = state["query"]

    print("\n⚡ ACTION")
    print(f"Selected action: {action}")

    if action == "calculator":
        result = calculator.invoke(query)

    elif action == "search":
        result = mock_search.invoke(query)

    else:
        result = "No external tool required."

    print(f"Tool result: {result}")

    return {
        "observation": str(result)
    }


def answer_node(state: AgentState):
    response = llm.invoke(
        f"""
Answer the user's question using the reasoning and observation below.

Question:
{state["query"]}

Reasoning:
{state["reasoning"]}

Observation:
{state["observation"]}

Give a clear final answer.
"""
    )

    print("\n💡 FINAL ANSWER")
    print(response.content)

    return {
        "answer": response.content
    }


graph = StateGraph(AgentState)

graph.add_node("reason", reason_node)
graph.add_node("action", action_node)
graph.add_node("answer", answer_node)

graph.add_edge(START, "reason")
graph.add_edge("reason", "action")
graph.add_edge("action", "answer")
graph.add_edge("answer", END)

app = graph.compile()


if __name__ == "__main__":
    query = input("Enter your question: ")

    initial_state = {
        "query": query,
        "reasoning": "",
        "action": "",
        "observation": "",
        "answer": ""
    }

    result = app.invoke(initial_state)

    print("\nAnswer:")
    print(result["answer"])
    png = app.get_graph().draw_mermaid_png()

    with open("react_graph.png", "wb") as f:
        f.write(png)

    print("Graph saved as react_graph.png")