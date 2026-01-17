"""
CSS styles for the Audit Bot AI application.
"""

import streamlit as st


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
    
    /* Hide Toolbar */
    .stToolbarActions {
        visibility: hidden;
    }
    
    /* Hide Streamlit Branding Elements */
    /* Hide "Deploy" badge */
    [class*="_viewerBadge_"] {
        display: none !important;
    }
    
    /* Hide App Creator Avatar */
    [class*="_profileContainer_"] {
        display: none !important;
    }
    </style>
    
    <script>
    // Function to remove Streamlit branding elements
    function removeStreamlitBranding() {
        // Remove viewer badge (Deploy button)
        const viewerBadges = document.querySelectorAll('[class*="_viewerBadge_"]');
        viewerBadges.forEach(badge => {
            if (badge && badge.parentElement) {
                badge.parentElement.removeChild(badge);
            }
        });
        
        // Remove profile container (App Creator Avatar)
        const profileContainers = document.querySelectorAll('[class*="_profileContainer_"]');
        profileContainers.forEach(container => {
            if (container && container.parentElement) {
                container.parentElement.removeChild(container);
            }
        });
    }
    
    // Run immediately
    removeStreamlitBranding();
    
    // Run after a short delay to catch dynamically loaded elements
    setTimeout(removeStreamlitBranding, 500);
    setTimeout(removeStreamlitBranding, 1000);
    setTimeout(removeStreamlitBranding, 2000);
    setTimeout(removeStreamlitBranding, 4000);
    
    // Use MutationObserver to catch elements added later
    const observer = new MutationObserver(function(mutations) {
        removeStreamlitBranding();
    });
    
    // Start observing the document with the configured parameters
    observer.observe(document.body, {
        childList: true,
        subtree: true
    });
    </script>
"""

    @classmethod
    def apply(cls) -> None:
        """Apply all CSS styles to the Streamlit app."""
        st.markdown(cls.get_main_css(), unsafe_allow_html=True)
