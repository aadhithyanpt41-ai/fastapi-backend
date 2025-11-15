from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
import requests
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

GEMINI_API_KEY = "AIzaSyAwRIm4-0Mnpe3kAGluWisZrKTT4aX54mY"
MODEL = "gemini-1.5-flash"

@app.get("/models")
def models():
    url = f"https://generativelanguage.googleapis.com/v1beta/models?key={GEMINI_API_KEY}"
    res = requests.get(url)
    return res.json()
@app.post("/chat")
async def chat(message: str = Form(...)):
    MODEL = "models/gemini-flash-latest"
    url = f"https://generativelanguage.googleapis.com/v1beta/{MODEL}:generateContent?key={GEMINI_API_KEY}"

    body = {
        "contents": [
            {"parts": [{"text": message}]}
        ]
    }

    res = requests.post(url, json=body)
    data = res.json()

    print("GEMINI RESPONSE:", data)

    if "error" in data:
        return {"reply": "GEMINI ERROR: " + data["error"]["message"]}

    reply = data["candidates"][0]["content"]["parts"][0]["text"]
    return {"reply": reply}
