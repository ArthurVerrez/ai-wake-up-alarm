import streamlit as st
from config import CURRENT_VERSION, APP_NAME


def header():
    """Displays the application header."""
    st.markdown(
        f"<h1>{APP_NAME} <small>v{CURRENT_VERSION}</small></h1>",
        unsafe_allow_html=True,
    )

    st.markdown(
        """Craft your perfect gentle wake-up experience! ✨
        """
    )

    st.divider()
