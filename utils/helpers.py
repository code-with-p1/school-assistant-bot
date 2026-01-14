# utils/helpers.py
import streamlit as st


def load_session_state():
    if "messages" not in st.session_state:
        st.session_state.messages = []