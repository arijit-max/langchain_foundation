from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from langchain.messages import HumanMessage
from dotenv import load_dotenv
import base64
from langchain.tools import tool
from typing import Dict, Any
from tavily import TavilyClient
from langgraph.checkpoint.memory import InMemorySaver
from mcp.server.fastmcp import FastMCP
from requests import get
import asyncio
import os
import sys

load_dotenv()

client = MultiServerMCPClient(
    {
        "local_server":{
            "transport":"stdio",
            "command":sys.executable,
            "args":["-u", "basic_mcp.py"]
        }
    }
)

async def initialize():
    global tools, resources, prompt
    try:
        print("Connecting to MCP server...")
        tools = await client.get_tools()
        print(f"Tools loaded: {len(tools)}")
        resources = await client.get_resources("local_server")
        print(f"Resources loaded: {len(resources)}")
        prompt_data = await client.get_prompt("local_server","prompt")
        prompt = prompt_data[0].content
        print("Prompt loaded")
        return tools, resources, prompt
    except Exception as e:
        print(f"Error during initialization: {e}")
        import traceback
        traceback.print_exc()
        raise

# Initialize tools, resources, and prompt
tools, resources, prompt = asyncio.run(initialize())

model = ChatOpenAI(
    model="mimo-v2.5-pro",
    api_key=os.getenv("OPENCODE_API_KEY"),
    base_url="https://opencode.ai/zen/go/v1"
)

agent = create_agent(
    model = model,
    tools = tools,
    system_prompt=prompt
)

async def main():
    config = {
        "configurable":{
            "thread_id":"1"
        }
    }
    response = await agent.ainvoke(
        {
            "messages":[
                HumanMessage(content = "Tell me about langchain-mcp adapter libraries")
            ]
        },
        config = config
    )
    return response

# Run the agent
response = asyncio.run(main())

# Print the agent's final answer
for message in response["messages"]:
    if message.type == "ai" and message.content:
        print("\nAgent response:")
        print(message.content)



