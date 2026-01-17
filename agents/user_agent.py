"""
SAP User Report Agent implementation with LangChain Pandas Agent.
"""

from typing import List, Optional
import pandas as pd
import streamlit as st

from agents.base_agent import BaseAgent


@st.cache_data
def load_user_report_data(file_path: str) -> pd.DataFrame:
    """Load and cache the User Report Excel file."""
    return pd.read_excel(file_path)


class UserReportAgent(BaseAgent):
    """
    Agent specialized for SAP User Reports.
    Provides insights on user types, statuses, and validity periods.
    Uses LangChain Pandas Agent for data analysis.
    """

    # Path to the Excel data file
    DATA_FILE_PATH = "documents/AI_Users_List_Report.xlsx"

    def __init__(self):
        """Initialize the agent and load the dataframe."""
        self._dataframe: Optional[pd.DataFrame] = None

    @property
    def name(self) -> str:
        return "SAP User Report Agent"

    @property
    def icon(self) -> str:
        return "👥"

    @property
    def description(self) -> str:
        return "Your intelligent assistant for SAP User Reports."

    @property
    def placeholder(self) -> str:
        return "Ask about your SAP User Report..."

    @property
    def suggested_messages(self) -> List[str]:
        return [
            "How many total users are there?",
            "How many dialog users are there?",
            "How many locked users are there?",
            "How many users never expire (VALID TO = BLANK)?",
        ]

    @property
    def dataframe(self) -> pd.DataFrame:
        """Lazy load and cache the dataframe."""
        if self._dataframe is None:
            self._dataframe = load_user_report_data(self.DATA_FILE_PATH)
        return self._dataframe

    @property
    def uses_pandas_agent(self) -> bool:
        """Flag indicating this agent uses Pandas Agent for queries."""
        return True

    @property
    def data_context(self) -> str:
        """
        SAP User Report data context with column metadata and sample rows.
        This provides context to the LLM about the data structure.
        """
        return """
The following data represents SAP User Report information from the file 'AI_Users_List_Report.xlsx'.
This dataset contains 1,017 SAP user records with 28 columns.

=== COLUMN METADATA ===

| Column Name              | Data Type  | Description                                           | Unique Values / Notes                     |
|--------------------------|------------|-------------------------------------------------------|-------------------------------------------|
| User Status / User Type  | string     | Type of SAP user                                      | DIALOG USER (915), SERVICE USER (91), SYSTEM USER (11) |
| System                   | string     | SAP system identifier                                 | PRD (all records)                         |
| Client                   | integer    | SAP client number                                     | 300 (all records)                         |
| SAP User ID              | string     | Unique user identifier                                | 1,017 unique values                       |
| Logon                    | string     | Logon status                                          | INACTIVE (all records)                    |
| Active                   | string     | Whether user is active (X = Yes)                      | X or empty/null                           |
| User Locked              | string     | Whether user is locked (X = Yes)                      | X or empty/null (27 locked users)         |
| Expired                  | string     | Whether user is expired (X = Yes)                     | X or empty/null (180 expired users)       |
| Terminated               | float      | Termination status                                    | All values are null/NaN                   |
| Current License          | string     | Current license type code                             | HD, 91, or null                           |
| License Description      | string     | Description of the license                            | SAP S/4HANA Cloud for self-ser, Test, or null |
| Law License              | string     | Law license code                                      | AX, AY, AZ, or null                       |
| Rec License              | string     | Recommended license code                              | AX, AY, AZ, or null                       |
| Last Name                | string     | User's last name                                      | 880 unique values                         |
| First Name               | string     | User's first name                                     | 449 unique values                         |
| User Count               | integer    | Count of users (always 1)                             | 1 (all records)                           |
| Role Count               | integer    | Number of roles assigned                              | 0-68 range                                |
| Trx Count                | integer    | Transaction count                                     | Various values                            |
| Trx Range                | integer    | Transaction range                                     | 0, 1, 16, 17, 125, 126, 141               |
| Trx Star                 | integer    | Star transactions                                     | 0 or 1                                    |
| Trx Wild                 | integer    | Wildcard transactions                                 | 0-27 range                                |
| Trx Exec                 | integer    | Executed transactions                                 | 0, 1, or 2                                |
| Risk Count               | integer    | Number of risks associated                            | 0-17 range (791 users have risk > 0)      |
| Risk Excuted Count       | integer    | Number of risks executed                              | 0 or 1 (only 3 users executed risk)       |
| User Valid From          | datetime   | User validity start date                              | Mostly null                               |
| User Valid To            | object     | User validity end date                                | 843 users have null (never expire)        |
| User Created On          | datetime   | Date when user was created                            | Various dates                             |
| User Last Logon          | datetime   | Last login date                                       | Various dates (106 null values)           |

=== KEY STATISTICS ===

- Total Users: 1,017
- Dialog Users: 915
- Service Users: 91
- System Users: 11
- Locked Users: 27
- Expired Users: 180
- Users Never Expire (VALID TO = BLANK): 843
- Active Users (Active=X): 837
- Users with Risk (Risk Count > 0): 791
- Users Executed Risk: 3

=== SAMPLE DATA (First 5 rows) ===

| User Type   | System | Client | SAP User ID | Active | User Locked | Expired | Current License | Role Count | Risk Count | Risk Excuted Count |
|-------------|--------|--------|-------------|--------|-------------|---------|-----------------|------------|------------|--------------------|
| DIALOG USER | PRD    | 300    | 1702SEA01   | X      | NaN         | NaN     | HD              | 10         | 3          | 1                  |
| DIALOG USER | PRD    | 300    | 1702SEA02   | X      | NaN         | NaN     | HD              | 10         | 3          | 1                  |
| DIALOG USER | PRD    | 300    | 1702SEA03   | X      | NaN         | NaN     | HD              | 10         | 3          | 1                  |
| DIALOG USER | PRD    | 300    | 1702SEA04   | X      | NaN         | NaN     | HD              | 10         | 3          | 0                  |
| DIALOG USER | PRD    | 300    | 1702SEA05   | X      | NaN         | NaN     | HD              | 10         | 3          | 0                  |

=== SAMPLE DATA (System Users) ===

| User Type    | SAP User ID   | Active | Role Count | Risk Count | User Created On |
|--------------|---------------|--------|------------|------------|-----------------|
| SYSTEM USER  | SM_ADMIN_SMP  | X      | 5          | 0          | 2018-11-07      |
| SYSTEM USER  | SM_SMP        | X      | 1          | 0          | 2018-11-07      |
| SYSTEM USER  | TMSADM        | X      | 0          | 0          | 2018-10-16      |
"""

    def get_system_prompt(self) -> str:
        """Generate system prompt with data context for Pandas Agent."""
        return f"""
You are "Audit Bot AI", a specialized chatbot for the brand "Audit Bots" (https://www.auditbots.com).
Your purpose is to help users access and understand SAP User Reports, including information about user types, statuses, validity periods, and risk analysis.

You have access to a pandas DataFrame named 'df' containing SAP user data. Use Python code to analyze and query this data.

{self.data_context}

INSTRUCTIONS:
1.  **Strict Scope**: ONLY answer questions related to the SAP User Report data or the "Audit Bot" brand.
2.  **Refusal**: If a user asks about general topics (e.g., "What is the capital of France?", "Write a poem"), politely refuse and state that you are specialized for Audit Bot SAP data.
3.  **Use the DataFrame**: For any data queries, use the pandas DataFrame 'df' to compute accurate answers.
4.  **Accuracy**: Use the data provided exactly. Do not hallucinate numbers.
5.  **Tone**: Professional, helpful, and concise.
6.  **Format**: Format numbers with commas (e.g., 1,017) for readability. Use tables when showing multiple records.

OUTPUT FORMATTING - VERY IMPORTANT:
- **NEVER show "NaN" or "nan" in your responses**. Replace all NaN/null values with user-friendly text:
  - For boolean/flag columns (Active, User Locked, Expired): Use "-" or "No" instead of NaN
  - For text columns (First Name, Last Name, License): Use "-" instead of NaN
  - For date columns: Use "-" or "Not Set" instead of NaN/NaT
- When displaying tables, always replace NaN values with "-" for better readability
- Use `df.fillna('-')` or similar when preparing data for display

IMPORTANT NOTES:
- When checking for "locked users", look for 'User Locked' column with value 'X'
- When checking for "expired users", look for 'Expired' column with value 'X'  
- When checking for "users that never expire", look for 'User Valid To' column with null/NaN values
- User types are in column 'User Status / User Type' with values: 'DIALOG USER', 'SERVICE USER', 'SYSTEM USER'
- Active users have 'X' in the 'Active' column
"""
