from llm_config import llm
from typing import Literal
from pydantic import BaseModel,Field
from langgraph.graph import StateGraph,START,END
from typing_extensions import TypedDict

class RouterDecision(BaseModel):
    category:Literal["math","coding","research","general"]= Field(
        description="the category that best matches the user query")

router_llm = llm.with_structured_output(RouterDecision)

class RouterState(TypedDict):
    query:str
    category:str
    answer:str

def router(state:RouterState):
    decision=router_llm.invoke(state["query"])
    return {
        "category":decision.category
    }

def math_agent(state:RouterState):
    response = llm.invoke(f"Solve this math question:  {state["query"]}")
    return {
        "answer":response.content
    }

def coding_agent(state:RouterState):
    response=llm.invoke(
        f"Answer this coding question: {state["query"]}"
    )
    return {
        "answer":response.content
    }

def research_agent(state:RouterState):
    response= llm.invoke(
        f"Research on the topic of {state["query"]}"
    )
    return {
        "answer":response.content
    }

def general_agent(state:RouterState):
    response=llm.invoke(
        f"Answer this general question: {state["query"]}"
    )
    return {
        "answer":response.content
    }

def router_query(state:RouterState):
    return state["category"]

graph = StateGraph(RouterState)
graph.add_node("router",router)
graph.add_node("math",math_agent)
graph.add_node("coding",coding_agent)
graph.add_node("research",research_agent)
graph.add_node("general",general_agent)

graph.add_edge(START,"router")
graph.add_conditional_edges(
    "router",
    router_query,
    {
        "math":"math",
        "coding":"coding",
        "research":"research",
        "general":"general"
    }
)

graph.add_edge("math",END)
graph.add_edge("coding",END)
graph.add_edge("research",END)
graph.add_edge("general",END)

agent = graph.compile()

query = input("Enter your question: ")
response = agent.invoke({"query":query})
print("\nSelected Agent")
print(response["category"])
print("\nAnswer")
print(response["answer"])