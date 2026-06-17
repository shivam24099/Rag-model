from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
import chromadb
import uuid
from ollama import chat
import os

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

model = SentenceTransformer("all-MiniLM-L6-v2")

#notes: pipeline 
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


"""
 for a better working of chat history we try:

        question -> llama creates a suitable prompt -> prompt retrieve from DB -> llama generate an answer -> print on console

        but we need a query writing as working with the above will give relevant answer for the certain number of queries

    
"""

def rewrite_query(question, history):
    prompt = f"""
            rewrite the current question so it is self-contained
            
            conversation:{history}
            
            current question: {question}   

            return only the re written question"""
    
    response = chat(
        model="llama3.2",
        messages=[{
            "role":"user",
            "content":prompt
        }]
    )
    return response["message"]["content"]






def generate_answer(question, history):

    user_messages = [
        msg["content"]
        for msg in history
        if msg["role"] == "user"
    ]

    last_user_questions = (
        user_messages[-3:]
        if user_messages
        else ""
    )
    retrieval_query = f"""
        {last_user_questions}

        {question}
    """

    query = rewrite_query(question, history)
    result = question_retrieval(query)
    print("\nREWRITTEN QUERY:")
    print(query)

    print("\n HISTORY:")
    print(history)

    context = "\n\n".join(result["documents"][0])

    messages = history.copy()

   

    messages.append({
        "role":"user",
        "content" : f"""
        use provided context to answer the question

    context: {context},

    question: {query}

    answer:
    """
    })

    response = chat(
        model="llama3.2",
        messages=messages
            
    )
    print("ANSWER:", response["message"]["content"])

    return response["message"]["content"]


def ask_question():
    history = []

    while True:
        question = input(str("Ask what you want? S to stop"))


        if (question.upper() == "S"):
            print("Ending session")
            break
        
        else: 
            response = generate_answer(question, history)

            history.append({
                "role":"user",
                "content":question
                })
            
            history.append({
                "role":"assistant",
                "content":response
                })            

            print(response)

    clear()
    

# text = read_pdf("ml notes.pdf")
# words = text.split() # this is the actual text

# chunks = divide_chunk(words)
# embeddings = embedd_text(chunks)

# store_chromadb(embeddings, chunks)
















"client = chromadb.Client()" # this only stores in the memory 
# print(embeddings[0][:10])
# print(embeddings[1][:10])
# print(type(embeddings))



