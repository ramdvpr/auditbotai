"""
Reusable UI components for the Audit Bot AI application.
"""

import streamlit as st
from typing import Dict, List, Optional
from agents.base_agent import BaseAgent
from config.settings import Settings


class UIComponents:
    """Factory class for creating UI components."""

    @staticmethod
    def render_header(agent: BaseAgent) -> None:
        """Render the main header with agent-specific description."""
        st.markdown(
            f'<div class="main-header">{Settings.APP_TITLE}</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            f'<div class="sub-header">{agent.description} Powered by {Settings.BRAND_NAME}.</div>',
            unsafe_allow_html=True,
        )

    @staticmethod
    def render_sidebar(
        agents: Dict[str, BaseAgent],
        current_agent_name: str,
    ) -> Optional[str]:
        """
        Render the sidebar with agent selection and suggested messages.

        Args:
            agents: Dictionary mapping agent names to agent instances
            current_agent_name: Name of the currently selected agent

        Returns:
            Selected suggestion message if any button was clicked, None otherwise
        """
        selected_suggestion = None
        current_agent = agents[current_agent_name]

        with st.sidebar:
            st.markdown("### 🤖 Agent Selection")

            # Agent dropdown
            selected_agent_name = st.selectbox(
                "Choose Agent",
                options=list(agents.keys()),
                index=list(agents.keys()).index(current_agent_name),
                key="agent_selector",
            )

            # Handle agent change
            if selected_agent_name != current_agent_name:
                st.session_state.selected_agent = selected_agent_name
                st.session_state.messages = []
                st.rerun()

            st.markdown("---")

            # Suggested Messages Section
            st.markdown(f"### {current_agent.icon} Suggested Questions")
            st.caption("Click to start a conversation:")

            for i, suggestion in enumerate(current_agent.suggested_messages):
                if st.button(
                    f"💬 {suggestion}",
                    key=f"suggestion_{i}",
                    use_container_width=True,
                ):
                    selected_suggestion = suggestion

            st.markdown("---")
            st.caption(f"Powered by [{Settings.BRAND_NAME}]({Settings.BRAND_URL})")

        return selected_suggestion

    @staticmethod
    def render_chat_history(messages: List[Dict[str, str]]) -> None:
        """Render the chat message history."""
        for message in messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    @staticmethod
    def render_chat_input(placeholder: str) -> Optional[str]:
        """Render the chat input field and return user input."""
        return st.chat_input(placeholder)

    @staticmethod
    def render_thinking_indicator(placeholder) -> None:
        """Show a thinking indicator in the given placeholder."""
        placeholder.markdown("_Thinking..._")

    @staticmethod
    def render_streaming_response(
        placeholder, content: str, is_complete: bool = False
    ) -> None:
        """
        Render streaming response content.

        Args:
            placeholder: Streamlit placeholder to render into
            content: Current accumulated content
            is_complete: Whether streaming is complete
        """
        if is_complete:
            placeholder.markdown(content)
        else:
            placeholder.markdown(content + "▌")
