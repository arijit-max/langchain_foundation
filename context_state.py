from langchain.agents import AgentState
from langchain.tools import tool, ToolRuntime
from langgraph.types import Command
from langchain.messages import ToolMessage
from langchain.chat_models import init_chat_model
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.messages import HumanMessage
from langgraph.checkpoint.memory import InMemorySaver

class CustomState(AgentState):
    fav_colour: str

import os

load_dotenv()

# Create the model
model = ChatOpenAI(
    model="mimo-v2.5-pro",
    api_key=os.getenv("OPENCODE_API_KEY"),
    base_url="https://opencode.ai/zen/go/v1"
)

@tool
def update_fav_colour(fav_colour:str, runtime: ToolRuntime) -> Command:
    """ 
        Update user's favourite colour after they reveal it
    """
    return Command[tuple[()]](
        update = {
            "fav_colour": fav_colour,
            "messages":[
                ToolMessage("Successfully updated favourite colour",tool_call_id = runtime.tool_call_id)
            ]
        }
    )

agent = create_agent(
    model = model,
    tools=[update_fav_colour],
    checkpointer=InMemorySaver(),
    state_schema=CustomState
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


