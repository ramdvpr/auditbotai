"""
SAP License Report Agent implementation.
"""

from typing import List
from agents.base_agent import BaseAgent


class LicenseReportAgent(BaseAgent):
    """
    Agent specialized for SAP License Summary reports.
    Provides insights on license types, costs, and utilization.
    """

    @property
    def name(self) -> str:
        return "SAP License Report Agent"

    @property
    def icon(self) -> str:
        return "📊"

    @property
    def description(self) -> str:
        return "Your intelligent assistant for SAP License Summaries."

    @property
    def placeholder(self) -> str:
        return "Ask about your SAP License Summary..."

    @property
    def suggested_messages(self) -> List[str]:
        return [
            "How many SAP license types are there?",
            "How much is the license purchased cost?",
            "What is the total unused license cost?",
        ]

    @property
    def data_context(self) -> str:
        """SAP License Summary data. Currency: USD ($)."""
        return """
The following data represents SAP License Summary information for a customer.
Currency: USD ($).

headers = ['License Type', 'License Description / Name', 'Purchased License', 'License Unit Cost', 'Purchased License Cost', 'Recommended License Count', 'Recommended License Cost', 'Multiple Logons Count', 'Multiple Logons Cost', 'Net Cost', 'Additional License Count', 'Additional License Cost', 'Unused License Count', 'Unused License Cost', 'AI Note']

rows = [
    ['CA', 'SAP Application Developer', 30, 5000, 150000, 4, 20000, 2, 200, 20200, 0, 0, 26, 130000, 'Record Level'],
    ['CB', 'SAP Application Professional', 300, 3500, 1050000, 2, 7000, 5, 500, 7500, 0, 0, 298, 1043000, 'Record Level'],
    ['CC', 'SAP Application Limited Professional', 70, 2000, 140000, 25, 50000, 8, 800, 50800, 0, 0, 45, 90000, 'Record Level'],
    ['CE', 'SAP Application ESS User', 250, 250, 62500, 290, 72500, 10, 1000, 73500, 40, 10000, 0, 0, 'Record Level'],
    ['Total', 'NaN', 650, 10750, 1402500, 321, 149500, 25, 2500, 152000, 40, 10000, 369, 1263000, 'Summary Level']
]
"""
