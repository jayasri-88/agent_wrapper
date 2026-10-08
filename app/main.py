from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from app.agent import create_chat

app=FastAPI(title="StudyMate Agent")
sessions={}

class ChatRequest(BaseModel):
    session_id:str
    message:str

@app.post("/chat")
def chat(req: ChatRequest):
    if req.session_id not in sessions:
        sessions[req.session_id]=create_chat()
    try:
        response=sessions[req.session_id].send_message(req.message)
        return {"reply": response.text or "(no response)"}
    except Exception as e:
        # Most common: rate limit (429) on the free tier
        return {"reply": f"Sorry, something went wrong: {e}"}
@app.get("/heath")
def health():
    return {"status":"ok"}
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def read_root():
    return FileResponse("static/index.html")
