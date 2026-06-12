import streamlit as st
from ollama import chat

prompt = st.chat_input("Ask a question")

if "messages" not in st.session_state:
    st.session_state.messages = []



if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})

    response = chat(
        model='llama3.2',
        messages=st.session_state.messages
            
    )
    

    answer = response["message"]["content"]
    
    st.session_state.messages.append(
        {"role":"assistant","content":answer})
    
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
          st.write(msg["content"])
    
    
