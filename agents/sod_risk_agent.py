"""
SAP SOD Risk Report Agent implementation with LangChain Pandas Agent.
"""

from typing import List, Optional
import pandas as pd
import streamlit as st

from agents.base_agent import BaseAgent


@st.cache_data
def load_sod_risk_data(file_path: str) -> pd.DataFrame:
    """Load and cache the SOD Risk Report Excel file."""
    return pd.read_excel(file_path)


class SODRiskReportAgent(BaseAgent):
    """
    Agent specialized for SAP Segregation of Duties (SOD) Risk Reports.
    Provides insights on risk users, risk types, and risk execution patterns.
    Uses LangChain Pandas Agent for data analysis.
    """

    # Path to the Excel data file
    DATA_FILE_PATH = "documents/AI_SOD_Risk_Report.xlsx"

    def __init__(self):
        """Initialize the agent and load the dataframe."""
        self._dataframe: Optional[pd.DataFrame] = None

    @property
    def name(self) -> str:
        return "SAP SOD Risk Report Agent"

    @property
    def icon(self) -> str:
        return "⚠️"

    @property
    def description(self) -> str:
        return "Your intelligent assistant for SAP SOD Risk Reports."

    @property
    def placeholder(self) -> str:
        return "Ask about your SAP SOD Risk Report..."

    @property
    def suggested_messages(self) -> List[str]:
        return [
            "How many risk users are there?",
            "How many risk users executed risk?",
            "What are the high risk levels breakdown?",
            "Show top 10 risk IDs by count",
        ]

    @property
    def dataframe(self) -> pd.DataFrame:
        """Lazy load and cache the dataframe."""
        if self._dataframe is None:
            self._dataframe = load_sod_risk_data(self.DATA_FILE_PATH)
        return self._dataframe

    @property
    def uses_pandas_agent(self) -> bool:
        """Flag indicating this agent uses Pandas Agent for queries."""
        return True

    @property
    def data_context(self) -> str:
        """
        SAP SOD Risk Report data context with column metadata and sample rows.
        This provides context to the LLM about the data structure.
        """
        return """
The following data represents SAP SOD (Segregation of Duties) Risk Report information from the file 'AI_SOD_Risk_Report.xlsx'.
This dataset contains 7,358 risk records for 791 unique users with 16 columns.

=== COLUMN METADATA ===

| Column Name      | Data Type | Description                                      | Unique Values / Notes                              |
|------------------|-----------|--------------------------------------------------|---------------------------------------------------|
| Sys              | string    | SAP system identifier                            | PRD (all records)                                 |
| Client           | integer   | SAP client number                                | 300 (all records)                                 |
| User ID          | string    | SAP user identifier                              | 791 unique users                                  |
| Risk Type        | string    | Type of risk                                     | 'SOD Risk' (5,622), 'Sensitive Trx Codes Risk' (1,736) |
| Risk Level       | string    | Severity level of the risk                       | 'H' = High (6,701), 'M' = Medium (657)            |
| Bus Module       | string    | Business module code                             | P2P, MM, SD, SU, FI, BS, AS, HR                   |
| Bus Module Desc  | string    | Business module description                      | Materials Mgmt, Procurement, or null              |
| Risk Exec        | string    | Whether risk was executed                        | '@0A@' = Executed, '@08@' = Not Executed          |
| Risk ID          | string    | Unique risk identifier code                      | 71 unique risk IDs (e.g., GRC14C, AUD009)         |
| Risk Name        | string    | Description of the risk                          | 70 unique risk names                              |
| False +          | float     | False positive indicator                         | All values are null/NaN                           |
| Total Risks      | integer   | Total risks for the user                         | 1-62 range                                        |
| Risk Roles       | integer   | Number of roles associated with the risk         | 0-67 range                                        |
| Total TCodes     | integer   | Total transaction codes                          | Various values                                    |
| Exec TCodes      | integer   | Executed transaction codes                       | 0, 1, or 2                                        |
| Risk Count       | integer   | Count for this risk record                       | Always 1                                          |

=== KEY STATISTICS ===

- Total Risk Records: 7,358
- Unique Users with Risks: 791
- SOD Risk Records: 5,622
- Sensitive Trx Codes Risk Records: 1,736
- High Risk Level (H): 6,701 records
- Medium Risk Level (M): 657 records
- Risks Executed: 7 records
- Users Who Executed Risk: 6 users

=== BUSINESS MODULE BREAKDOWN ===

| Bus Module | Code | Count |
|------------|------|-------|
| Procurement | P2P  | 1,612 |
| Materials Management | MM | 1,064 |
| Sales & Distribution | SD | 1,029 |
| Security/User Admin | SU | 990 |
| Finance | FI | 945 |
| Basis/System | BS | 746 |
| Asset Management | AS | 504 |
| Human Resources | HR | 468 |

=== TOP RISK IDs ===

| Risk ID | Risk Name | Count |
|---------|-----------|-------|
| AUD009  | Maintain User Master Record | 790 |
| GRC06B  | Enter/Modify Purchase Order & Goods Receipt | 700 |
| GRC14C  | Maintain Material Master Data & Enter/Modify Purchase Order | 694 |
| GRC13A  | Various | 210 |
| GRC20B  | Various | 102 |

=== SAMPLE DATA (First 5 rows) ===

| User ID   | Risk Type | Risk Level | Bus Module | Risk ID | Risk Name | Risk Exec |
|-----------|-----------|------------|------------|---------|-----------|-----------|
| 1702SEA01 | SOD Risk  | H          | MM         | GRC14C  | Maintain Material Master Data & Enter/Modify Purchase Order | Executed |
| 1702SEA01 | SOD Risk  | H          | P2P        | GRC06B  | Enter/Modify Purchase Order & Goods Receipt | Not Executed |
| 1702SEA01 | Sensitive Trx Codes Risk | H | SU | AUD009 | Maintain User Master Record | Not Executed |
| 1702SEA02 | SOD Risk  | H          | MM         | GRC14C  | Maintain Material Master Data & Enter/Modify Purchase Order | Not Executed |
| 1702SEA02 | SOD Risk  | H          | P2P        | GRC06B  | Enter/Modify Purchase Order & Goods Receipt | Executed |

=== IMPORTANT CODE MAPPINGS ===

- Risk Exec: '@0A@' means EXECUTED, '@08@' means NOT EXECUTED
- Risk Level: 'H' = High, 'M' = Medium
"""

    def get_system_prompt(self) -> str:
        """Generate system prompt with data context for Pandas Agent."""
        return f"""
You are "Audit Bot AI", a specialized chatbot for the brand "Audit Bots" (https://www.auditbots.com).
Your purpose is to help users access and understand SAP SOD (Segregation of Duties) Risk Reports, including information about risk types, risk levels, business modules, and risk execution status.

You have access to a pandas DataFrame named 'df' containing SAP SOD risk data. Use Python code to analyze and query this data.

{self.data_context}

INSTRUCTIONS:
1.  **Strict Scope**: ONLY answer questions related to the SAP SOD Risk Report data or the "Audit Bot" brand.
2.  **Refusal**: If a user asks about general topics (e.g., "What is the capital of France?", "Write a poem"), politely refuse and state that you are specialized for Audit Bot SAP data.
3.  **Use the DataFrame**: For any data queries, use the pandas DataFrame 'df' to compute accurate answers.
4.  **Accuracy**: Use the data provided exactly. Do not hallucinate numbers.
5.  **Tone**: Professional, helpful, and concise.
6.  **Format**: Format numbers with commas (e.g., 7,358) for readability. Use tables when showing multiple records.

OUTPUT FORMATTING - VERY IMPORTANT:
- **NEVER show "NaN" or "nan" in your responses**. Replace all NaN/null values with user-friendly text:
  - For text columns: Use "-" instead of NaN
  - For numeric columns: Use "0" or "-" as appropriate
- When displaying tables, always replace NaN values with "-" for better readability
- Use `df.fillna('-')` or similar when preparing data for display
- Convert Risk Exec codes to readable format: '@0A@' → 'Executed', '@08@' → 'Not Executed'

IMPORTANT NOTES:
- When checking for "executed risks", look for 'Risk Exec' column with value '@0A@'
- When checking for "not executed risks", look for 'Risk Exec' column with value '@08@'
- Risk types are: 'SOD Risk' and 'Sensitive Trx Codes Risk'
- Risk levels are: 'H' = High, 'M' = Medium
- To count unique users with risk, use df['User ID'].nunique()
- To count users who executed risk, filter by Risk Exec == '@0A@' then count unique User IDs
"""
