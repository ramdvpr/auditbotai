import streamlit as st
from openai import OpenAI

# --- Page Configuration ---
st.set_page_config(
    page_title="Audit Bot AI",
    page_icon="🤖",
    layout="centered",
)

# --- Custom CSS for Premium UI ---
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* Main Container */
    .stApp {
        background-color: #0E1117; /* Dark background */
        color: #FAFAFA;
    }

    /* Header Styling */
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        background: -webkit-linear-gradient(45deg, #4F46E5, #9333EA);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        text-align: center;
        color: #A1A1AA;
        font-size: 1rem;
        margin-bottom: 2rem;
    }

    /* Chat Message Styling */
    .stChatMessage {
        background-color: rgba(255, 255, 255, 0.05);
        border-radius: 12px;
        padding: 10px;
        margin-bottom: 10px;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* User Message Override */
    div[data-testid="stChatMessage"]:nth-child(even) {
        background-color: rgba(79, 70, 229, 0.1); /* Indigo tint for user */
        border-color: rgba(79, 70, 229, 0.2);
    }

    /* Input Field */
    .stTextInput input {
        border-radius: 20px;
        background-color: rgba(255,255,255,0.05);
        color: white;
        border: 1px solid rgba(255,255,255,0.1);
    }
    .stTextInput input:focus {
        border-color: #4F46E5;
        box-shadow: 0 0 0 1px #4F46E5;
    }
    
    /* Hide Streamlit Elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    .stToolbarActions {
        visibility: hidden;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# --- Header ---
st.markdown('<div class="main-header">Audit Bot AI</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="sub-header">Your intelligent assistant for SAP License Summaries. Powered by Audit Bot.</div>',
    unsafe_allow_html=True,
)

# --- Data Embedding ---
# This data describes the SAP License Summary as provided
# Currency: USD
license_data = """
headers = ['License Type', 'License Description / Name', 'Purchased License', 'License Unit Cost', 'Purchased License Cost', 'Recommended License Count', 'Recommended License Cost', 'Multiple Logons Count', 'Multiple Logons Cost', 'Net Cost', 'Additional License Count', 'Additional License Cost', 'Unused License Count', 'Unused License Cost', 'AI Note']

rows = [
    ['CA', 'SAP Application Developer', 30, 5000, 150000, 4, 20000, 2, 200, 20200, 0, 0, 26, 130000, 'Record Level'],
    ['CB', 'SAP Application Professional', 300, 3500, 1050000, 2, 7000, 5, 500, 7500, 0, 0, 298, 1043000, 'Record Level'],
    ['CC', 'SAP Application Limited Professional', 70, 2000, 140000, 25, 50000, 8, 800, 50800, 0, 0, 45, 90000, 'Record Level'],
    ['CE', 'SAP Application ESS User', 250, 250, 62500, 290, 72500, 10, 1000, 73500, 40, 10000, 0, 0, 'Record Level'],
    ['Total', 'NaN', 650, 10750, 1402500, 321, 149500, 25, 2500, 152000, 40, 10000, 369, 1263000, 'Summary Level']
]
"""

# --- OpenAI Configuration ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# System Prompt
system_prompt = f"""
You are "Audit Bot AI", a specialized chatbot for the brand "Audit Bots" (https://www.auditbots.com/).
Your purpose is to help users access and understand custom SAP report data, specifically the License Summary data provided below.

DATA CONTEXT:
The following data represents SAP License Summary information for a customer.
Currency: USD ($).

{license_data}

INSTRUCTIONS:
1.  **Strict Scope**: specific ONLY answer questions related to the provided data or the "Audit Bot" brand.
2.  **Refusal**: If a user asks about general topics (e.g., "What is the capital of France?", "Write a poem"), politely refuse and state that you are specialized for Audit Bot SAP license data.
3.  **Accuracy**: Use the data provided exactly. Do not hallucinate numbers. If the data is 'NaN' or missing, state that.
4.  **Tone**: Professional, helpful, and concise.
5.  **Format**: Format numbers with commas (e.g., $1,402,500) for readability.
"""

# --- Chat Logic ---

# Initialize OpenAI Client
# Expects OPENAI_API_KEY in .streamlit/secrets.toml
try:
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
except Exception:
    st.error(
        "OpenAI API Key not found. Please set `OPENAI_API_KEY` in `.streamlit/secrets.toml`."
    )
    st.stop()

# Display Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input
if prompt := st.chat_input("Ask about your SAP License Summary..."):
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate Response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

        # Prepare messages for API
        api_messages = [{"role": "system", "content": system_prompt}] + [
            {"role": m["role"], "content": m["content"]}
            for m in st.session_state.messages
        ]

        try:
            stream = client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=api_messages,
                stream=True,
            )

            for chunk in stream:
                if chunk.choices[0].delta.content is not None:
                    full_response += chunk.choices[0].delta.content
                    message_placeholder.markdown(full_response + "▌")

            message_placeholder.markdown(full_response)
        except Exception as e:
            st.error(f"Error generating response: {e}")
            full_response = "I encountered an error while processing your request. Please check your API configuration."

    # Add assistant response to history
    st.session_state.messages.append({"role": "assistant", "content": full_response})
