import streamlit as st
import os
from src.langgraph.ui.config import Config
from dotenv import load_dotenv
load_dotenv()

class LoadStreamlitUI:
    def __init__(self):
        self.config = Config()
        self.user_controls={}

    def load_streamlit_ui(self):
        st.set_page_config(page_title=f"AI {self.config.get_page_title()}", layout="wide")
        st.header(f"AI {self.config.get_page_title()}")

        with st.sidebar:
            # Get options from config
            llm_options = self.config.get_llm_options()
            usecase_options = self.config.get_usecase_options()

            # LLM selection
            self.user_controls["selected_llm"] = st.selectbox("Select LLM", llm_options)

            if self.user_controls["selected_llm"] == "Groq":
                # Model selection
                model_options = self.config.get_groq_model_options()
                self.user_controls["selected_groq_model"] = st.selectbox("Select Model", model_options)
                self.user_controls["GROQ_API_KEY"] = st.session_state["GROQ_API_KEY"] = st.text_input("API Key", type="password")

                # Validate API Key
                if not self.user_controls["GROQ_API_KEY"]:
                    st.warning(" Please enter your GROQ API key to proceed. Don't have?")

            if self.user_controls["selected_llm"] == "Claude":
                # Model selection
                model_options = self.config.get_claude_model_options()
                self.user_controls["selected_claude_model"] = st.selectbox("Select Model", model_options)
                self.user_controls["CLAUDE_API_KEY"] = st.session_state["CLAUDE_API_KEY"] = st.text_input("API Key", type="password")

                # Validate API Key
                if not self.user_controls["CLAUDE_API_KEY"]:
                    st.warning(" Please enter your CLAUDE API key to proceed. Don't have?")

            ## Use case selection
            self.user_controls["selected_usecase"] = st.selectbox("Select Use Case", usecase_options)


            if self.user_controls["selected_usecase"] == "Chatbot with Tool":
                # tavily_api_key = st.text_input("TAVILY API KEY", type="password")
                tavily_api_key = os.getenv("TAVILY_API_KEY")
                st.session_state["TAVILY_API_KEY"] = tavily_api_key
                self.user_controls["TAVILY_API_KEY"] = tavily_api_key
                os.environ["TAVILY_API_KEY"] = tavily_api_key

                if not self.user_controls["TAVILY_API_KEY"]:
                    st.warning("Please enter your TAVILY_API_KEY key to proceed.")

        return self.user_controls

