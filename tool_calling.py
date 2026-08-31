from langchain.chat_models import init_chat_model
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.messages import HumanMessage
from pprint import pprint
from langchain.tools import tool
import os

load_dotenv()

# Create the model
model = ChatOpenAI(
    model="mimo-v2.5-pro",
    api_key=os.getenv("OPENCODE_API_KEY"),
    base_url="https://opencode.ai/zen/go/v1"
)

@tool("square_root")
def tool1(x:float) -> float:
    """
    Calculates square root of a number
    """
    return x ** 0.5

prompt = """
    You are an arithmetic wizard who can perform square and square-root of any number
"""

agent = create_agent(
    model = model,
    system_prompt=prompt,
    tools = [tool1]
)

question = HumanMessage(content = "What is the square root of 469?")
response = agent.invoke(
    {
        "messages":[question]
    }
)
print(response['messages'][-1].content)
