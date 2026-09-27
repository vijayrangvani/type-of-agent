from llm_config import llm

def simple_agent(query):
    response = llm.invoke(query)
    return response.content

query = input("Enter your question: ")
result = simple_agent(query)
print("\nAnswer: ")
print(result)