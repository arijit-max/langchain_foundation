from langchain.chat_models import init_chat_model
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.messages import HumanMessage
from pprint import pprint
from langchain.tools import tool
from langgraph.checkpoint.memory import InMemorySaver
import os

load_dotenv()

# Create the model
model = ChatOpenAI(
    model="mimo-v2.5-pro",
    api_key=os.getenv("OPENCODE_API_KEY"),
    base_url="https://opencode.ai/zen/go/v1"
)

agent = create_agent(
    model = model,
    checkpointer=InMemorySaver()
)
question = HumanMessage(content = "What is my favourite colour?")
config = {
    "configurable":{
        "thread_id":"1"
    }
}
response = agent.invoke(
    {
        "messages":[question]
    },
    config,
)
print(response['messages'][-1].content)

# ===================================================================================
# Testing block

# question = HumanMessage(content = "What is my favourite colour?")
# response = agent.invoke(
#     {
#         "messages":[question]
#     },
#     config,
# )
# print(response['messages'][-1].content)

# ===================================================================================

