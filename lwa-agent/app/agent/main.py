from langchain_aws import BedrockEmbeddings
import csv
import os
from typing import List
from typing_extensions import TypedDict

from langchain_core.documents import Document
from langchain_core.tools import tool
from langchain_text_splitters import RecursiveCharacterTextSplitter

# from langchain_huggingface import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from langchain_community.vectorstores import FAISS
from langchain.agents import create_agent
from dotenv import load_dotenv
from app.llms.groq import GroqLLM
from app.llms.bedrock import BedrockLLM
from app.graphs.builder import GraphBuilder

# Import AgentCore runtime
from bedrock_agentcore.runtime import BedrockAgentCoreApp
# Create the AgentCore app instance
app = BedrockAgentCoreApp()

_ = load_dotenv()



# AgentCore Entrypoint
@app.entrypoint
def agent_invocation(payload, context):
    """Handler for agent invocation in AgentCore runtime"""
    print("Received payload:", payload)
    print("Context:", context)

    llm = BedrockLLM().get_llm()
    graph_builder = GraphBuilder(llm)
    graph = graph_builder.setup_graph()
    
    # Extract query from payload
    query = payload.get("prompt", "No prompt found in input")

    # Invoke the graph
    result = graph.invoke({"messages": [("human", query)]})

    print("Result:", result)

    # Return the answer
    return {
        "result": result["messages"][-1].content,
        "messages": [m.model_dump(mode="json") for m in result["messages"]],
    }


if __name__ == "__main__":
    app.run(port=8080)
