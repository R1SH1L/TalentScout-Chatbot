"""TalentScout AI Hiring Assistant - Main Application Entry Point

A Streamlit-based chatbot for conducting technical interviews.
Collects candidate information and conducts AI-powered technical interviews.
"""

import streamlit as st
import sys
from pathlib import Path

# Add project root to Python path for module imports
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

try:
    from config import Config
    from core.chatbot_logic import run_chatbot
except ImportError as e:
    st.error(f"Import error: {e}")
    st.error("Please ensure all required files are in place.")
    st.stop()


def main() -> None:
    """Main application entry point with error handling."""
    try:
        # Validate configuration before starting
        Config.validate_config()
        
        # Configure Streamlit page settings
        st.set_page_config(
            page_title=Config.APP_TITLE,
            page_icon=Config.APP_ICON,
            layout="centered",
            initial_sidebar_state="collapsed"
        )
        
        # Display main title and subtitle
        st.title(f"{Config.APP_ICON} {Config.APP_TITLE}")
        st.markdown("*Streamlined AI-powered technical interviews for modern hiring*")
        
        run_chatbot()
        
    except ValueError as e:
        st.error(f"Configuration Error: {e}")
        st.info("Please check your .env file and ensure all required variables are set.")
    except Exception as e:
        st.error(f"Application Error: {e}")
        st.info("Please contact support if this issue persists.")


if __name__ == "__main__":
    main()
