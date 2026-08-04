import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

class GroqLLM:
    def __init__(self):
        load_dotenv()

    def get_llm(self, model_name="llama3-70b-8192"):

        try:
            os.environ["GROQ_API_KEY"] = groq_api_key = os.getenv("GROQ_API_KEY")
            llm = ChatGroq(api_key=groq_api_key, model="llama-3.1-8b-instant")
            return llm
        except Exception as e:
            raise ValueError("Error occurred with exception: {e}")

        