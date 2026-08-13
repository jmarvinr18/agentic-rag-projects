import os
import io
import base64
import mimetypes
from app.services.Prompt import PromptTemplate
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.messages import HumanMessage
from flask import current_app
from app.models import Message
from app.database import db
from langchain_classic.chains import create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_classic.chains import create_history_aware_retriever
from app.services.VectorStore.pgvector import PGVectorService

from pdf2image import convert_from_path
from dotenv import load_dotenv
from langchain_classic.retrievers import EnsembleRetriever
from langchain_community.retrievers import BM25Retriever
from langchain_aws.retrievers import AmazonKnowledgeBasesRetriever
import boto3
from botocore.client import Config

load_dotenv()

class AIMessageService:

    def __init__(self, model):
        self.model = model


        bedrock_config = Config(
            connect_timeout=120,
            read_timeout=120,
            retries={"max_attempts": 3}
        )        
        # bedrock-agent-runtime is what the retriever uses to call your KB
        bedrock_agent_client = boto3.client(
            "bedrock-agent-runtime",
            region_name="ap-southeast-1",
            config=bedrock_config
        )
        # --- Retriever pointing directly at your Bedrock Knowledge Base ---
        self.aws_bedrock_retriever = AmazonKnowledgeBasesRetriever(
            knowledge_base_id="KJRW6GFIPJ",        # from AWS Bedrock console
            client=bedrock_agent_client,           # explicit client
            retrieval_config={
                "vectorSearchConfiguration": {
                    "numberOfResults": 5,
                    "overrideSearchType": "SEMANTIC"   # or HYBRID
                }
            },
        )

        self.rag_chain = self._build_chain()
        self.with_history = self._init_runnable_message_history()


    def _build_chain(self):
        qa_system_prompt = PromptTemplate().getQASystemPrompt()
        contextualize_prompt = PromptTemplate().getContextualizePrompt()
        history_aware_retriever = create_history_aware_retriever(self.model, 
                                                                 self.aws_bedrock_retriever, 
                                                                 contextualize_prompt)
        question_answer_chain = create_stuff_documents_chain(self.model, qa_system_prompt)
        return create_retrieval_chain(history_aware_retriever, question_answer_chain)


    def getSessionHistory(self, conversation_id: str="") -> BaseChatMessageHistory:

        history = InMemoryChatMessageHistory()
        messages = (Message.query.filter_by(conversation_id=conversation_id)
                                  .order_by(Message.created_at)
                                  .all())
        for m in messages:
            if m.role == "user":
                history.add_message(message=HumanMessage(content=m.content))

        return history
    
    def _init_runnable_message_history(self):
        return RunnableWithMessageHistory(self.rag_chain,
                                    self.getSessionHistory,
                                    input_messages_key="input",
                                    history_messages_key="chat_history",
                                    output_messages_key="answer",  
                                    )        

    def ask(self, conversation_id, human_message):

        config = {"configurable": {"session_id": conversation_id}}

        # Step 1: retrieve relevant docs
        docs = self.retrieve_relevant_docs(human_message)

        # Step 2: guardrail
        if not docs:
            return {
                "answer": "No relevant information found in the knowledge base.",
                "sources": []
            }
        
        # Step 3: normal RAG execution
        response = self.with_history.invoke(
            {"input": human_message},
            config=config
        )

        return {
            "answer": response["answer"],
            "sources": [doc.metadata for doc in docs]
        }

