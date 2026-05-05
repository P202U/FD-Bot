import streamlit as st
from rag import FinancialAssistant

st.set_page_config(page_title="FD-Bot", page_icon="💰")

# --- UI Header ---
st.title("💰 FD-Bot: Personal Financial Assistant")
st.info("Running 100% Offline | Gemma 4 E2B")


# --- Initialize Assistant (Cached) ---
@st.cache_resource
def get_assistant():
    return FinancialAssistant()


assistant = get_assistant()

# --- Chat Interface ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input
if prompt := st.chat_input("Ask about your FD rates or Tax..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        full_response = ""

        stream = assistant.ask(prompt, stream=True)

        for chunk in stream:
            full_response += chunk["response"]
            response_placeholder.markdown(full_response + "▌")

        response_placeholder.markdown(full_response)

    st.session_state.messages.append({"role": "assistant", "content": full_response})
