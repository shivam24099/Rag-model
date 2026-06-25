import streamlit as st
import Rag
from sqlite_storage import save_message, load_chat, create_chat, get_all_chats, delete_chat
import requests

st.title("AI Assistant", text_alignment="center")
st.header("Hii! I am your ai assistant\n", text_alignment="center")
st.header("ask me what you want", text_alignment="center")

if "chat_id" not in st.session_state:
    st.session_state.chat_id = None
with st.sidebar:
    #getting the file to upload in the rag
    uploaded_file = st.file_uploader("Add the file", type="pdf")

    # uploading the file using all the functions 
    if uploaded_file:
        st.write(uploaded_file.name)

        if st.button("Click to upload"):
            with st.spinner("uploading file..."):
                text = Rag.read_pdf(uploaded_file)
                words = text.split()
                chunks = Rag.divide_chunk(words)
                embeddings = Rag.embedd_text(chunks)
                Rag.store_chromadb(embeddings, chunks, uploaded_file.name)

                st.success("pdf uploaded successfully")

    if st.button("new chat"):
        response = requests.post("http://127.0.0.1:8000/chat")
        st.session_state.chat_id = response.json()["chat_id"]

        st.session_state.messages = []

    st.write("Select chat:")
    chat_id = st.selectbox(
        "chat",
        get_all_chats()
    )

    if st.button("Load Chat"):
        hist = load_chat(chat_id)
        st.session_state.messages = hist
        st.rerun()

    if st.button("delete chat"):
        delete_chat(chat_id)

        st.session_state.chat_id = None
        st.session_state.messages = []

        st.rerun()




if "messages" not in st.session_state:
    # st.session_state.messages = Rag.load_json()
# showing old messages immediately
    st.session_state.messages = []



for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

question = st.chat_input("Ask your question")

if question:
    if st.session_state.chat_id is None:
        # st.session_state.chat_id = create_chat()

        response = requests.post("http://127.0.0.1:8000/chat")

        st.session_state.chat_id = response.json()["chat_id"]


    with st.chat_message("user"):
        st.write(question)

    st.session_state.messages.append({
        "role":"user",
        "content":question
    })


    save_message(st.session_state.chat_id, "user", question)


    with st.spinner("Processing answer"):
        
        # answer = Rag.generate_answer(question, st.session_state.messages)

        response = requests.post("http://127.0.0.1:8000/ask",
                               json={
                                   "question":question,
                                   "history":st.session_state.messages
                               })
        answer = response.json()
        
    

        save_message(st.session_state.chat_id, "assistant", answer["answer"])

        with st.chat_message("assistant"):
            st.write(answer["answer"])

        st.session_state.messages.append({
            "role":"assistant",
            "content":answer["answer"]
        })

    Rag.store_json(st.session_state.messages) 

    with st.expander("source"):
        source = {source["source"]
                for source in answer["sources"]}
        st.write(source)

# if st.button("clear chat"):
#     st.session_state.messages = []
#     Rag.store_json([])
#     st.rerun()

    

