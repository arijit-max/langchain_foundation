from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from langchain.messages import HumanMessage
from dotenv import load_dotenv
import base64
from langchain.tools import tool
from typing import Dict, Any
from tavily import TavilyClient
from langgraph.checkpoint.memory import InMemorySaver
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

prompt = """
    You are a personal chef. Suggest a list of recipe suggestions and instructions on how to make those recipes
    after user supplies you with the left over ingredients in his house. Using web search tool suggest the recipes
    and also the instructions to make those recipes.
"""

agent = create_agent(
    model = model,
    tools = [web_search],
    system_prompt = prompt,
    checkpointer = InMemorySaver()
)
config = {
    "configurable":{
        "thread_id":"1"
    }
}

question = input("Ask a question?")
response = agent.invoke(
    {
        "messages":[
            HumanMessage(
                content = question
            )
        ]
    },
    config,
)
print(response['messages'][-1].content)


