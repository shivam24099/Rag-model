import Rag

# text = Rag.read_pdf("PS.pdf")

# words = text.split()
# chunks = Rag.divide_chunk(words)

# embeddings = Rag.embedd_text(chunks)

# Rag.store_chromadb(embeddings, chunks)
question = input(str("Ask what you want?"))

response = Rag.generate_answer(question)

print(response["message"]["content"])



