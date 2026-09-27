import os 
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()



llm = ChatOpenAI (
    model=os.getenv("MODEL"),
    temperature=0,
    base_url=os.getenv("BASE_URL"),
    api_key=os.getenv("API_KEY"),
)

