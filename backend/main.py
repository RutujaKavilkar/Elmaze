from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
import os
import time

app = FastAPI()

# ✅ Allow React (port 3000)
origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# Request Model
# =========================
class ChatRequest(BaseModel):
    message: str


# =========================
# Dummy PCB Generator
# =========================
def generate_pcb_file(user_input: str) -> str:
    """
    Simulates PCB generation.
    Replace this with your actual PCB generator logic.
    """
    os.makedirs("outputs", exist_ok=True)

    file_path = f"outputs/pcb_{int(time.time())}.txt"

    with open(file_path, "w") as f:
        f.write(f"PCB GENERATED\n\nUser Input:\n{user_input}\n\n")
        f.write("✔ Components placed\n")
        f.write("✔ Routing optimized\n")
        f.write("✔ Signal integrity checked\n")

    return file_path


# =========================
# API Routes
# =========================
@app.get("/")
def read_root():
    return {"message": "FastAPI PCB Backend Running 🚀"}


@app.post("/api/generate")
def generate_pcb(data: ChatRequest):
    """
    Receives message from frontend and generates PCB file
    """
    file_path = generate_pcb_file(data.message)

    return {
        "reply": "✅ PCB generated successfully!",
        "download_url": f"http://localhost:8000/download/{os.path.basename(file_path)}"
    }


@app.get("/download/{filename}")
def download_file(filename: str):
    file_path = os.path.join("outputs", filename)

    if os.path.exists(file_path):
        return FileResponse(
            path=file_path,
            filename=filename,
            media_type='application/octet-stream'
        )

    return {"error": "File not found"}