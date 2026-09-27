from llm_config import llm
from langchain_core.tools import tool
from langchain.agents import create_agent

@tool
def calculator(expression:str)-> str:
    """Create a simple mathamatical calculator"""
    print(f"🔧 Tool called: calculator | Input: {expression}")
    try:
        return str(eval(expression))
    except Exception as e:
        return "Unable to calculate the expression"
    
@tool
def mock_search(query:str)->str:
    """Search information about a topic"""
    print(f"🔧 Tool called: mock_search | Input: {query}")
    return f"Search result for: {query}"

agent=create_agent(
    model=llm,
    tools=[calculator,mock_search]
)

if __name__ == "__main__":
    query = input("Enter your question: ")
    response = agent.invoke(
        {
            "messages":[
                {"role":"user","content":query}
            ]
        }
    )

    print("\nAnswers")
    print(response["messages"][-1].content)