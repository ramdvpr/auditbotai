"""
Base Agent class that defines the interface for all SAP report agents.
"""

from abc import ABC, abstractmethod
from typing import List


class BaseAgent(ABC):
    """
    Abstract base class for all SAP report agents.
    Each agent must implement the abstract methods to provide
    agent-specific configuration and data.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """Display name of the agent shown in the UI."""
        pass

    @property
    @abstractmethod
    def icon(self) -> str:
        """Emoji icon representing the agent."""
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        """Short description shown in the UI header."""
        pass

    @property
    @abstractmethod
    def placeholder(self) -> str:
        """Placeholder text for the chat input field."""
        pass

    @property
    @abstractmethod
    def suggested_messages(self) -> List[str]:
        """List of suggested questions shown in the sidebar."""
        pass

    @property
    @abstractmethod
    def data_context(self) -> str:
        """The data context embedded in the system prompt."""
        pass

    @property
    def uses_pandas_agent(self) -> bool:
        """Whether this agent uses Pandas Agent for queries. Override in subclass."""
        return False

    @property
    def base_instructions(self) -> str:
        """Common instructions for all agents."""
        return """
INSTRUCTIONS:
1.  **Strict Scope**: ONLY answer questions related to the provided data or the "Audit Bot" brand.
2.  **Refusal**: If a user asks about general topics (e.g., "What is the capital of France?", "Write a poem"), politely refuse and state that you are specialized for Audit Bot SAP data.
3.  **Accuracy**: Use the data provided exactly. Do not hallucinate numbers. If the data is 'NaN' or missing, state that.
4.  **Tone**: Professional, helpful, and concise.
5.  **Format**: Format numbers with commas (e.g., $1,402,500) for readability.
"""

    def get_system_prompt(self) -> str:
        """
        Generate the complete system prompt for this agent.
        Combines the agent-specific context with base instructions.
        """
        return f"""
You are "Audit Bot AI", a specialized chatbot for the brand "Audit Bots" (https://www.auditbots.com/).
{self.description}

DATA CONTEXT:
{self.data_context}

{self.base_instructions}
"""

    def to_dict(self) -> dict:
        """Convert agent configuration to dictionary for session state."""
        return {
            "name": self.name,
            "icon": self.icon,
            "description": self.description,
            "placeholder": self.placeholder,
            "suggested_messages": self.suggested_messages,
        }
