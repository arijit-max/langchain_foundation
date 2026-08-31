from langchain.chat_models import init_chat_model
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.messages import HumanMessage
from pprint import pprint
from langchain.tools import tool
from typing import Dict,Any
from tavily import TavilyClient
import os

load_dotenv()

tavily_client = TavilyClient()

# Create the model
model = ChatOpenAI(
    model="mimo-v2.5-pro",
    api_key=os.getenv("OPENCODE_API_KEY"),
    base_url="https://opencode.ai/zen/go/v1"
)



@tool
def web_search(query:str) -> Dict[str,Any]:
    """
        Search the web for informations
    """
    return tavily_client.search(query)

agent = create_agent(
    model = model,
    tools = [web_search]
)

question = HumanMessage(content = "Who is the Chief Minister of West Bengal (India)?")
response = agent.invoke(
    {
        "messages":[question]
    }
)
print(response['messages'][-1].content)