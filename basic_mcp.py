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
import os
import sys

load_dotenv()

mcp = FastMCP[Any]("mcp_server")

try:
    tavily_client = TavilyClient()
except Exception as e:
    print(f"Warning: Could not initialize Tavily client: {e}", file=sys.stderr)
    tavily_client = None

# Create the model
try:
    model = ChatOpenAI(
        model="mimo-v2.5-pro",
        api_key=os.getenv("OPENCODE_API_KEY"),
        base_url="https://opencode.ai/zen/go/v1"
    )
except Exception as e:
    print(f"Warning: Could not initialize model: {e}", file=sys.stderr)
    model = None

@mcp.tool()
def web_search(query:str) -> Dict[str,Any]:
    """
        Search the web for informations
    """
    if tavily_client is None:
        return {"error": "Tavily client not initialized"}
    return tavily_client.search(query)

@mcp. resource("github://langchain-ai/langchain-mcp-adapters/blob/main/README.md")
def github_file():
    """Resource for accessing langchain-ai/langchain-mcp-adapters/README.md file
    """

    url =f"https://raw.githubusercontent.com/langchain-ai/langchain-mcp-adapters/blob/main/README.md"
    try:
        resp = get(url)
        return resp. text
    except Exception as e:
        return f"Error: {str(e)}"

@mcp.prompt()
def prompt():
    """Analyze data from a langchain-ai repo file with comprehensive insights"""
    return """
    You are a helpful assistant that answers user questions about LangChain, LangGraph and LangSmith.

    You can use the following tools/resources to answer user questions:
    - search_web: Search the web for information
    - github_file: Access the langchain-ai repo files

    If the user asks a question that is not related to LangChain, LangGraph or LangSmith, you should say "I'm sorry, I

    You may try multiple tool and resource calls to answer the user's question.

    You may also ask clarifying questions to the user to better understand their question."""

if __name__== "__main__":
    try:
        mcp.run(transport="stdio")
    except Exception as e:
        print(f"Error running MCP server: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc(file=sys.stderr)
        sys.exit(1)
   

