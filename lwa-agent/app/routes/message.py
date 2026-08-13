from flask import request, Response
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError
from langchain_core.messages import HumanMessage, AIMessage
import json

from app.schema.message import MessageSchema
from app.routes import api
from app.llms.groq import GroqLLM
from app.graphs.builder import GraphBuilder
from flask import current_app


blp = Blueprint(
    "messages",
    __name__,
    url_prefix="/messages",
    description="Message operations"
)

@blp.route("/")


class Message(MethodView):

    def get (self):
        return {"message": f"Welcome to RAG POC message", "status": 200}

    
    @blp.arguments(MessageSchema)
    def post(self, message_data):
        llm = GroqLLM().get_llm()
        graph_builder = GraphBuilder(llm)
        graph = graph_builder.setup_graph()

        def stream_events():
            tool_counter = 0

            for event in graph.stream({"messages": [HumanMessage(content=message_data["content"])]}):
                node_name = list(event.keys())[0]
                state = event[node_name]

                # Tool call detection
                if node_name == "agent":
                    messages = state.get("messages", [])
                    if messages:
                        last_msg = messages[-1]
                        if hasattr(last_msg, "tool_calls") and last_msg.tool_calls:
                            for tool_call in last_msg.tool_calls:
                                tool_counter += 1
                                yield f"data: {json.dumps({'type': 'tool_call', 'id': f't{tool_counter}', 'name': tool_call['name'], 'status': 'running'})}\n\n"

                # Content/message detection
                if node_name in ["retrieve_tool", "rewrite", "generate"]:
                    messages = state.get("messages", [])
                    if messages:
                        last_msg = messages[-1]
                        content = last_msg.content if hasattr(last_msg, "content") else str(last_msg)

                        if isinstance(content, str) and content.strip():
                            # Split content into chunks for streaming effect
                            chunks = content.split(". ")
                            for chunk in chunks:
                                if chunk.strip():
                                    yield f"data: {json.dumps({'type': 'content', 'text': chunk + '. '})}\n\n"

                        # Mark tool as done
                        if node_name == "retrieve_tool":
                            yield f"data: {json.dumps({'type': 'tool_call', 'id': f't{tool_counter}', 'status': 'done'})}\n\n"

            # Final done event
            yield f"data: {json.dumps({'type': 'done'})}\n\n"

        return Response(stream_events(), mimetype="text/event-stream", headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no"
        })

    def delete(self):
        pass
