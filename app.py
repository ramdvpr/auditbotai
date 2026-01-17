"""
Audit Bot AI - Main Application Entry Point

A modular, OOP-based Streamlit chatbot for SAP report analysis.
Supports multiple agent types for different SAP reports.
"""

import streamlit as st
from typing import Dict

# Local imports
from agents import LicenseReportAgent, SODRiskReportAgent, UserReportAgent
from agents.base_agent import BaseAgent
from config.settings import Settings
from ui.styles import Styles
from ui.components import UIComponents
from services.chat_service import ChatService
from services.pandas_agent_service import PandasAgentService


# --- Agent Registry ---
def get_available_agents() -> Dict[str, BaseAgent]:
    """
    Get all available agents.
    Add new agents here as they are created.
    """
    agents = [
        LicenseReportAgent(),
        SODRiskReportAgent(),
        UserReportAgent(),
    ]
    return {agent.name: agent for agent in agents}


# --- Page Configuration ---
st.set_page_config(
    page_title=Settings.APP_TITLE,
    page_icon=Settings.APP_ICON,
    layout="wide",
)

# --- Apply Styles ---
Styles.apply()

# --- Initialize Session State ---
if "messages" not in st.session_state:
    st.session_state.messages = []

if "selected_agent" not in st.session_state:
    st.session_state.selected_agent = Settings.DEFAULT_AGENT

if "pending_message" not in st.session_state:
    st.session_state.pending_message = None

# --- Get Available Agents ---
AGENTS = get_available_agents()


def get_current_agent() -> BaseAgent:
    """Get the currently selected agent instance."""
    return AGENTS[st.session_state.selected_agent]


# --- Render UI ---
# Sidebar with agent selection and suggestions
selected_suggestion = UIComponents.render_sidebar(
    agents=AGENTS,
    current_agent_name=st.session_state.selected_agent,
)

# Handle suggestion click
if selected_suggestion:
    st.session_state.pending_message = selected_suggestion
    st.rerun()

# Main header
current_agent = get_current_agent()
UIComponents.render_header(current_agent)

# Chat history
UIComponents.render_chat_history(st.session_state.messages)

# --- Handle User Input ---
# Always render chat input first
chat_input_prompt = UIComponents.render_chat_input(current_agent.placeholder)

# Check for pending message from sidebar or use chat input
prompt = None
if st.session_state.pending_message:
    prompt = st.session_state.pending_message
    st.session_state.pending_message = None
elif chat_input_prompt:
    prompt = chat_input_prompt

# Process user input
if prompt:
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate and stream response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

        # Show thinking indicator
        UIComponents.render_thinking_indicator(message_placeholder)

        # Check if agent uses Pandas Agent
        if current_agent.uses_pandas_agent:
            # Use Pandas Agent for data analysis
            pandas_service = PandasAgentService(
                dataframe=current_agent.dataframe,
                agent=current_agent,
            )

            for chunk in pandas_service.stream_response(prompt):
                full_response += chunk
                UIComponents.render_streaming_response(
                    message_placeholder, full_response, is_complete=False
                )
        else:
            # Use regular chat service
            chat_service = ChatService()

            for chunk in chat_service.stream_response(
                agent=current_agent,
                chat_history=st.session_state.messages,
            ):
                full_response += chunk
                UIComponents.render_streaming_response(
                    message_placeholder, full_response, is_complete=False
                )

        # Final render without cursor
        UIComponents.render_streaming_response(
            message_placeholder, full_response, is_complete=True
        )

    # Add assistant response to history
    st.session_state.messages.append({"role": "assistant", "content": full_response})

    # Rerun to refresh the UI and show the chat input again
    st.rerun()
