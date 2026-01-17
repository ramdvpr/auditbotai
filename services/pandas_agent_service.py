"""
Pandas Agent service for data analysis using LangChain.
"""

import streamlit as st
from typing import Generator
import pandas as pd
from langchain_openai import ChatOpenAI
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent

from config.settings import Settings
from agents.base_agent import BaseAgent


class PandasAgentService:
    """
    Service for handling queries using LangChain Pandas DataFrame Agent.
    Provides more accurate data analysis capabilities.
    """

    def __init__(self, dataframe: pd.DataFrame, agent: BaseAgent):
        """
        Initialize the Pandas Agent service.

        Args:
            dataframe: The pandas DataFrame to query
            agent: The agent instance for system prompt configuration
        """
        self._validate_api_key()
        self.dataframe = dataframe
        self.agent = agent
        self.pandas_agent = self._create_agent()

    def _validate_api_key(self) -> None:
        """Validate that OpenAI API key is configured."""
        if "OPENAI_API_KEY" not in st.secrets:
            st.error(
                "OpenAI API Key not found. Please set `OPENAI_API_KEY` in `.streamlit/secrets.toml`."
            )
            st.stop()

    def _create_agent(self):
        """Create and return the LangChain Pandas DataFrame Agent."""
        try:
            llm = ChatOpenAI(
                model=Settings.OPENAI_MODEL,
                api_key=st.secrets["OPENAI_API_KEY"],
                temperature=0,  # More deterministic for data queries
            )

            # Create the pandas agent with the dataframe
            pandas_agent = create_pandas_dataframe_agent(
                llm=llm,
                df=self.dataframe,
                agent_type="tool-calling",
                verbose=True,
                allow_dangerous_code=True,  # Required for pandas operations
                prefix=self.agent.get_system_prompt(),
            )

            return pandas_agent
        except Exception as e:
            st.error(f"Error creating Pandas Agent: {e}")
            st.stop()

    def invoke(self, query: str) -> str:
        """
        Invoke the pandas agent with a query.

        Args:
            query: The user's question about the data

        Returns:
            The agent's response as a string
        """
        try:
            result = self.pandas_agent.invoke({"input": query})
            return result.get(
                "output", "I couldn't process that query. Please try again."
            )
        except Exception as e:
            return f"I encountered an error while analyzing the data: {str(e)}"

    def stream_response(self, query: str) -> Generator[str, None, None]:
        """
        Stream the response from the pandas agent.
        Note: Pandas agent doesn't support true streaming, so we simulate it.

        Args:
            query: The user's question about the data

        Yields:
            Chunks of the response (simulated streaming)
        """
        # Get the full response first
        response = self.invoke(query)

        # Simulate streaming by yielding chunks
        words = response.split(" ")
        buffer = ""

        for i, word in enumerate(words):
            buffer += word
            if i < len(words) - 1:
                buffer += " "

            # Yield every few words to simulate streaming
            if len(buffer) > 20 or i == len(words) - 1:
                yield buffer
                buffer = ""
