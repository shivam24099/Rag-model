from fastapi import FastAPI, HTTPException, UploadFile, File
import Rag
from pydantic import BaseModel
import sqlite_storage

class Question(BaseModel):
    question: str
    history: list = []

class Messages(BaseModel):
    role: str
    content: str

app = FastAPI()

# request for generate an answer
@app.post("/ask")
def ask_question(question: Question):
    answer = Rag.generate_answer(question.question, question.history)

    return answer
# request a chat id
@app.post("/chats")
def get_chat():
    chat_id = sqlite_storage.create_chat()

    return {"chatid": chat_id}

 # saving the messages
@app.post("/chats/{chat_id}/message")
def save_message(chat_id: int, message: Messages):
    
    sqlite_storage.save_message(chat_id, message.role, message.content)

    return {"status" : "saved"}

# loading previous chats
@app.get("/chats/{chat_id}")
def load_chat(chat_id: int):

    if not sqlite_storage.chat_exists(chat_id):

        raise HTTPException(
            status_code=404,
            detail="chat not found"
        )
    chats = sqlite_storage.load_chat(chat_id)

    return chats

@app.delete("/chats/{chat_id}")
def delete_chat_messages(chat_id):
    if not sqlite_storage.chat_exists(chat_id):

        raise HTTPException(
            status_code=404,
            detail="chat not found"
        )

    sqlite_storage.delete_chat(chat_id)
    return {"status" : "deleted"}

# for uploading thee pdf
@app.post("/ingest")
def upload(file: UploadFile = File(...)):
    
    if file.content_type != "application/pdf":
        HTTPException(
            status_code=400,
            detail="only pdf files are allowed"
        )

    file.file.seek(0)
    text = Rag.read_pdf(file.file)

    words = text.split()
    chunks = Rag.divide_chunk(words)
    embedded_text = Rag.embedd_text(chunks)

    Rag.store_chromadb(embedded_text, chunks, file.filename)

    return {"status" : "pdf uploaded"}