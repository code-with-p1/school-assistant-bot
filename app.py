# app.py
import streamlit as st
from rag.chain import get_rag_chain
from utils.helpers import load_session_state

st.set_page_config(
    page_title="School Assistant Bot",
    page_icon="🏫",
    layout="wide"
)

st.title("🏫 School Assistant Bot")
st.caption("Ask anything about your school!")

# Load chain (cached)
chain = get_rag_chain()

# Chat history
load_session_state()

# Display messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input
if prompt := st.chat_input("Ask me anything about school..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = chain.invoke(prompt)
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
            except Exception as e:
                error = f"Sorry, something went wrong: {str(e)}"
                st.error(error)
                st.session_state.messages.append({"role": "assistant", "content": error})

# Sidebar controls
with st.sidebar:
    st.markdown("### Controls")
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()