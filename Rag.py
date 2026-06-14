from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
import chromadb
import uuid
from ollama import chat

model = SentenceTransformer("all-MiniLM-L6-v2")

#notes: 
"""
            pdf -> text extraction -> chunks creates -> embedding chunks (turing into vectors) -> storing into chromadb
"""

def read_pdf(pdf):
    reader = PdfReader(pdf)

    text = ""

    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text

    return text

def divide_chunk(words, chunk_size=500, overlap=50):
    chunks = []

    # Loop through the list of words, jumping by chunk_size each time
    for i in range(0, len(words), chunk_size - overlap):
        chunk_words = words[i : i + chunk_size]
        chunks.append(' '.join(chunk_words)) 

    return chunks

def embedd_text(chunks):
    
    embeddings = model.encode(chunks) # our embedded text
    return embeddings

def get_collection():
    client = chromadb.PersistentClient("./chroma_db")
    collection = client.get_or_create_collection(
        name= "My_collection",
        embedding_function=None
    )

    return collection

def store_chromadb(embeddings, chunks, pdf_name):

    collection = get_collection()
    ids = [str(uuid.uuid4()) for _ in range(len(chunks))]

    metadatas = [{
        "source": pdf_name,
        "chunk": i
    }
    for i in range(len(chunks))
    ]

    existing = collection.get(
        where= {"source":pdf_name}
    )

    if (existing["ids"]):
        print("Pdf already exist")

    else:
        collection.add(
            ids= ids,
            embeddings=embeddings,
            documents=chunks,
            metadatas=metadatas
        )

    return collection


def question_retrieval(question):
    question_embeddings = model.encode(question)
    collection = get_collection()

    results = collection.query(
        query_embeddings= [question_embeddings],
        n_results= 3
    )

    return results

def generate_answer(question):
    result = question_retrieval(question)

    context = "\n\n".join(result["documents"][0])

    prompt = f"""

    context: {context},

    question: {question},

    answer: 

    """

    response = chat(
        model="llama3.2",
        messages=[
            {
            "role":"user",
            "content":prompt
            }
            
        ]
    )

    return response["message"]["content"]

def ask_question():

    while True:
        question = input(str("Ask what you want? S to stop"))

        if (question == "S"):
            print("Ending session")
            break
        
        else: 
            response = generate_answer(question)
            print(response)
            print("\n\n")


# text = read_pdf("ml notes.pdf")
# words = text.split() # this is the actual text

# chunks = divide_chunk(words)
# embeddings = embedd_text(chunks)

# store_chromadb(embeddings, chunks)
















"client = chromadb.Client()" # this only stores in the memory 
# print(embeddings[0][:10])
# print(embeddings[1][:10])
# print(type(embeddings))



