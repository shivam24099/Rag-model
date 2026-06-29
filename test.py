from speech import listen
import requests

question = listen()

print(question)

response = requests.post("http://127.0.0.1:8000/ask",
                               json={
                                   "question":question,
                                   "history":[]
                               })
answer = response.json()

print(answer["answer"])