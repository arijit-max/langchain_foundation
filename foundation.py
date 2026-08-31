from langchain.chat_models import init_chat_model
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import os

load_dotenv()

llm = ChatOpenAI(
    model="mimo-v2.5-pro",
    api_key=os.getenv("OPENCODE_API_KEY"),
    base_url="https://opencode.ai/zen/go/v1"
)

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an AI engineering tutor."),
    ("human", "Explain {topic} with a simple example.")
])

chain = prompt | llm

response = chain.invoke({
    "topic": "Reciprocal Rank Fusion in RAG"
})

print(response.content)


