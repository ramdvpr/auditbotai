"""
Chat service handling LLM interactions.
"""

import streamlit as st
from typing import List, Dict, Generator, Any
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

from config.settings import Settings
from agents.base_agent import BaseAgent


class ChatService:
    """
    Service class for handling chat interactions with the LLM.
    Manages message conversion and streaming responses.
    """

    def __init__(self):
        """Initialize the chat service with LangChain ChatOpenAI."""
        self._validate_api_key()
        self.llm = self._initialize_llm()

    def _validate_api_key(self) -> None:
        """Validate that OpenAI API key is configured."""
        if "OPENAI_API_KEY" not in st.secrets:
            st.error(
                "OpenAI API Key not found. Please set `OPENAI_API_KEY` in `.streamlit/secrets.toml`."
            )
            st.stop()

    def _initialize_llm(self) -> ChatOpenAI:
        """Initialize and return the LangChain ChatOpenAI instance."""
        try:
            return ChatOpenAI(
                model=Settings.OPENAI_MODEL,
                api_key=st.secrets["OPENAI_API_KEY"],
                streaming=True,
            )
        except Exception as e:
            st.error(f"Error initializing LangChain: {e}")
            st.stop()

    def _convert_messages(
        self,
        system_prompt: str,
        chat_history: List[Dict[str, str]],
    ) -> List:
        """
        Convert session state messages to LangChain message objects.

        Args:
            system_prompt: The system prompt for the agent
            chat_history: List of message dicts with 'role' and 'content'

        Returns:
            List of LangChain message objects
        """
        messages = [SystemMessage(content=system_prompt)]

        for msg in chat_history:
            if msg["role"] == "user":
                messages.append(HumanMessage(content=msg["content"]))
            elif msg["role"] == "assistant":
                messages.append(AIMessage(content=msg["content"]))

        return messages

    def stream_response(
        self,
        agent: BaseAgent,
        chat_history: List[Dict[str, str]],
    ) -> Generator[str, None, None]:
        """
        Stream a response from the LLM.

        Args:
            agent: The current agent providing the system prompt
            chat_history: The chat history including the new user message

        Yields:
            Chunks of the response content
        """
        system_prompt = agent.get_system_prompt()
        messages = self._convert_messages(system_prompt, chat_history)

        try:
            stream = self.llm.stream(messages)
            for chunk in stream:
                if hasattr(chunk, "content"):
                    yield chunk.content
        except ValueError as e:
            st.error(f"Configuration error: {e}")
            yield "I encountered a configuration error. Please check your API settings."
        except Exception as e:
            st.error(f"Error generating response: {e}")
            yield "I encountered an error while processing your request. Please try again."
