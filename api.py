from fastapi import FastAPI, HTTPException
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

@app.post("/chat")
def get_chat():
    chat_id = sqlite_storage.create_chat()

    return {"chat_id": chat_id}

@app.post("/chat/{chat_id}/message")
def save_message(chat_id: int, message: Messages):
    
    sqlite_storage.save_message(chat_id, message.role, message.content)

    return {"status" : "saved"}

@app.get("/load-chat/{chat_id}")
def load_chat(chat_id: int):

    if not sqlite_storage.chat_exists(chat_id):

        raise HTTPException(
            status_code=404,
            detail="chat not found"
        )
    chats = sqlite_storage.load_chat(chat_id)

    return chats

@app.delete("/delete-chat/{chat_id}")
def delete_chat_messages(chat_id):
    if not sqlite_storage.chat_exists(chat_id):

        raise HTTPException(
            status_code=404,
            detail="chat not found"
        )

    sqlite_storage.delete_chat(chat_id)
    return {"status" : "deleted"}