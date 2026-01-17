"""
CSS styles for the Audit Bot AI application.
"""

import streamlit as st
import streamlit.components.v1 as components


class Styles:
    """Manages all CSS styles for the application."""

    @staticmethod
    def get_main_css() -> str:
        """Return the main CSS styles for the application."""
        return """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* Main Container */
    .stApp {
        background-color: #0E1117;
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
        background-color: rgba(79, 70, 229, 0.1);
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
    
    /* Suggested Message Button Styling */
    .suggested-btn {
        background: linear-gradient(135deg, rgba(79, 70, 229, 0.2), rgba(147, 51, 234, 0.2));
        border: 1px solid rgba(79, 70, 229, 0.3);
        border-radius: 10px;
        padding: 0.75rem 1rem;
        color: #E5E7EB;
        font-size: 0.875rem;
        cursor: pointer;
        transition: all 0.2s ease;
        text-align: left;
        width: 100%;
        margin-bottom: 0.5rem;
    }
    
    .suggested-btn:hover {
        background: linear-gradient(135deg, rgba(79, 70, 229, 0.4), rgba(147, 51, 234, 0.4));
        border-color: rgba(79, 70, 229, 0.5);
        transform: translateX(4px);
    }
    
    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #161B22;
    }
    
    section[data-testid="stSidebar"] .stSelectbox label {
        color: #A1A1AA;
    }
    
    /* Remove Streamlit branding */
    .stToolbarActions {
        visibility: hidden;
    }
    </style>
"""

    @staticmethod
    def inject_branding_removal_script() -> None:
        """Inject JavaScript to remove Streamlit branding elements using components.html()."""
        components.html(
            """
            <script>
            // Function to remove Streamlit branding elements
            function removeStreamlitBranding() {
                // Remove header
                document.querySelectorAll(".stToolbarActions").forEach(el => el.remove());
                
                // Remove footer streamlit icon
                // var link = document.querySelector('a[href="https://streamlit.io/cloud"]');
                // if (link) {
                    // link.remove();
                // }
                
                // Remove footer streamlit user profile
                // var link = document.querySelector('a[href^="https://share.streamlit.io/user/ramdvpr"]');
                // var twoLevelsUp = link?.parentElement?.parentElement;
                // if (twoLevelsUp) {
                    // twoLevelsUp.remove();
                // }
            }
            
            // Run immediately
            removeStreamlitBranding();
            
            // Run after delays to catch dynamically loaded elements
            setTimeout(removeStreamlitBranding, 100);
            setTimeout(removeStreamlitBranding, 500);
            setTimeout(removeStreamlitBranding, 1000);
            setTimeout(removeStreamlitBranding, 2000);
            setTimeout(removeStreamlitBranding, 5000);
            
            // Use MutationObserver to catch elements added later
            const parentDoc = window.parent.document;
            const observer = new MutationObserver(function(mutations) {
                removeStreamlitBranding();
            });
            
            // Start observing the parent document
            observer.observe(parentDoc.body, {
                childList: true,
                subtree: true
            });
            </script>
            """,
            height=0,
        )

    @classmethod
    def apply(cls) -> None:
        """Apply all CSS styles and JavaScript to the Streamlit app."""
        st.markdown(cls.get_main_css(), unsafe_allow_html=True)
        cls.inject_branding_removal_script()
