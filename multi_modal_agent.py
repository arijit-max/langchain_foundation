from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from langchain.messages import HumanMessage
from dotenv import load_dotenv
import base64
import os

load_dotenv()

# Create the model
model = ChatOpenAI(
    model="deepseek-v4-flash-vision-exp",
    api_key=os.getenv("OPENCODE_API_KEY"),
    base_url="https://opencode.ai/zen/go/v1"
)

# Read image from local filesystem
with open("moon.png", "rb") as f:
    img_bytes = f.read()

# Convert image bytes → Base64 string
img_b64 = base64.b64encode(img_bytes).decode("utf-8")

# Create agent
agent = create_agent(
    model=model
)

# Create multimodal message
multi_modal_question = HumanMessage(
    content=[
        {
            "type": "text",
            "text": "Tell me about this capital"
        },
        {
            "type": "image_url",
            "image_url": {
                "url": f"data:image/png;base64,{img_b64}"
            }
        }
    ]
)

# Invoke agent
response = agent.invoke(
    {
        "messages": [multi_modal_question]
    }
)

print(response["messages"][-1].content)