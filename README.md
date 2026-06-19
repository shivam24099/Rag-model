# Conversational RAG Chatbot

A Retrieval-Augmented Generation (RAG) chatbot that allows users to upload PDFs and ask questions about their content.

## Features

* PDF Upload
* Text Extraction using PyPDF
* Chunking with Overlap
* Sentence Transformer Embeddings
* ChromaDB Vector Storage
* Conversational Memory
* Query Rewriting
* Source Citations
* Streamlit Chat Interface
* JSON Chat Persistence

## Tech Stack

* Python
* Streamlit
* Ollama (Llama 3.2)
* ChromaDB
* Sentence Transformers
* PyPDF

## Project Architecture

PDF → Text Extraction → Chunking → Embeddings → ChromaDB

User Question → Query Rewriting → Retrieval → Llama 3.2 → Answer

## Installation

```bash
git clone <repo-url>

pip install -r requirements.txt

streamlit run app.py
```

## Future Improvements

* SQLite Chat Storage
* Multiple Conversations
* FastAPI Backend
* Voice Interface
* Streaming Responses
* Better Retrieval and Reranking

```
```

