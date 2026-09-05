# agent.py
from bedrock_agentcore.runtime import BedrockAgentCoreApp

from app.graphs.builder import GraphBuilder   # your existing graph
from app.llms.bedrock import BedrockLLM
from app.config import load_secrets
load_secrets()
app = BedrockAgentCoreApp()



llm = BedrockLLM().get_llm()

graph = GraphBuilder(llm).setup_graph()

@app.entrypoint
async def invoke(payload, context):

    result = await graph.ainvoke(
        {"messages": [{"role": "user", "content": payload["prompt"]}]},
        config={"configurable": {"thread_id": context.session_id}},
    )
    return {"result": result["messages"][-1].content}

if __name__ == "__main__":
    app.run()