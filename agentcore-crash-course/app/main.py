from langchain_aws import BedrockEmbeddings
import csv
import os
from typing import List
from typing_extensions import TypedDict
from app.ser

from dotenv import load_dotenv

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

    # Extract query from payload
    query = payload.get("prompt", "No prompt found in input")

    # Invoke the graph
    result = agent.invoke({"messages": [("human", query)]})

    print("Result:", result)

    # Return the answer
    return {"result": result['messages'][-1].content}


if __name__ == "__main__":
    app.run(port=8080)
