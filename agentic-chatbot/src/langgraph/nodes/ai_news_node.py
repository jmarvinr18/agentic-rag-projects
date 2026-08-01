from src.langgraph.state.state import State
from tavily import TavilyClient
from langchain_core.prompts import ChatPromptTemplate
import streamlit as st

class AINewsNode:

    def __init__(self,model):
        """
        Initialize the AINewsNode with API keys for Tavily and
        """
        self.tavily=TavilyClient()
        self.llm=model

        # This is used to capture various steps in this file so that later can be use for steps shown
        self.state = {}

    def fetch_news(self, state: dict)->dict:
        """
        Fetch AI News based on the specified frequency.

        Args:
            state (dict): The state dictionary containing 'frequency'

        Returns:
            dict: Updated state with 'news_data' key containing fetched news.
        """


        frequency = st.session_state.timeframe.lower()

        query = state["messages"][0].content.lower()

        print(f"FREQUENCY: {frequency.lower()}")

        print(f"MESSAGE INSIDE STATE: {state["messages"][0].content.lower()}")

       
        # self.state["messages"]
        
        time_range_map = {"daily": "d", "weekly": "w", "monthly": "m", "yearly": "y"}

        print(f"TIME_RANGE: {time_range_map[frequency]}")

        days_map = {"daily": 1, "weekly": 7, "monthly": 30, "yearly": 366}

        response = self.tavily.search(
            query=query,
            topic="news",
            time_range=time_range_map[frequency],
            include_answer="advanced",
            max_results=15,
            days=days_map[frequency]
        )

        state["news_data"] = response.get("results", [])
        self.state["news_data"] = state["news_data"]

        return state

    def summarize_news(self, state: dict)->dict:
        """
        Summarize the fetched news using an LLM.

        Args:
            state (dict): The state dictionary containing 'news_data'.

        Returns:
            dict: Updated state with 'summary' key containing the summarized news.
        """

        news_items = self.state["news_data"]

        prompt_template = ChatPromptTemplate.from_messages([
            ("system", """Summarize AI news articles into markdown format. For each item include:
                - Date in **YYYY-MM-DD** format in IST timezone
                - Concise 5 sentences summary from latest news
                - Sort news by date wise (latest first)
                - Source URL as link
                Use format:
                ### [Date]
                - [5 Sentences Summary - URL]"""),
                ("user", "Articles:\n{articles}")
        ])

        articles_str = "\n\n".join([
            f"Content: {item.get("content", "")}\nURL: {item.get("url", "")}\nDate: {item.get("published_date", "")}"
            for item in news_items
        ])

        response = self.llm.invoke(prompt_template.format(articles=articles_str))

        state["summary"] = response.content
        self.state["summary"] = state["summary"]

        return self.state

    def save_results(self, state):
        frequency = st.session_state.timeframe.lower()
        summary = self.state["summary"]
        filename = f"./AINews/{frequency}_summary.md"

        with open(filename,"w") as f:
            f.write(f"# {frequency.capitalize()} AI News Summary\n\n")
            f.write(summary)
        self.state["filename"] = filename

        return self.state





