import streamlit as st
import Rag

st.title("AI Assistant", text_alignment="center")
st.header("Hii! I am you ai assistant\n", text_alignment="center")
st.header("ask me what you want", text_alignment="center")

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




if "messages" not in st.session_state:
    st.session_state.messages = Rag.load_json()
# showing old messages immediately


for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

question = st.chat_input("Ask your question")

if question:

    with st.chat_message("user"):
        st.write(question)

    st.session_state.messages.append({
        "role":"user",
        "content":question
    })

    with st.spinner("Processing answer"):
        answer = Rag.generate_answer(question, st.session_state.messages)

        with st.chat_message("assistant"):
            st.write(answer)

        st.session_state.messages.append({
            "role":"assistant",
            "content":answer
        })

    Rag.store_json(st.session_state.messages)

if st.button("clear chat"):
    st.session_state.messages = []
