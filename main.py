import Rag
from sqlite_storage import save_message, load_chat

# text = Rag.read_pdf("ml notes.pdf")

# words = text.split()
# chunks = Rag.divide_chunk(words)

# embeddings = Rag.embedd_text(chunks)

# Rag.store_chromadb(embeddings, chunks, "ml notes")
Rag.ask_question()

# for msg in history:
#     save_message(1, msg["role"], msg["content"])






