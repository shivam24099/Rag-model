import Rag
from sqlite_storage import create_chat, save_message

# text = Rag.read_pdf("ml notes.pdf")

# words = text.split()
# chunks = Rag.divide_chunk(words)

# embeddings = Rag.embedd_text(chunks)

# Rag.store_chromadb(embeddings, chunks, "ml notes")
Rag.ask_question()







