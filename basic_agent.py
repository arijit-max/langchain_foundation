from langchain.chat_models import init_chat_model
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.messages import HumanMessage
from pprint import pprint
import os

load_dotenv()

# Create the model
model = ChatOpenAI(
    model="mimo-v2.5-pro",
    api_key=os.getenv("OPENCODE_API_KEY"),
    base_url="https://opencode.ai/zen/go/v1"
)

agent = create_agent(model = model)

prompt = "You are a science fiction writer who creates capitals on user's request"

agent = create_agent(
    model = model,
    system_prompt=prompt
)

response = agent.invoke(
    {
        "messages":[
            HumanMessage(content = "What is the capital of Moon?")
        ]
    }
)
pprint(response["messages"][-1].content)



