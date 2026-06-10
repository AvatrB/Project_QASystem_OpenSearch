from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# Impor Otak Llama-3.3-70B yang sudah kita rakit
from agent_brain import agent_executor

# 1. Inisiasi Saraf Pusat
app = FastAPI(title="NEXUS Medis API", version="1.0")

# 2. Buka Gerbang Lintas Domain (CORS) agar Frontend React bisa menembus masuk
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Dalam produksi, ini harus diganti dengan localhost:5173 (Vite)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. Skema Data Masukan dari Chatroom
class ChatRequest(BaseModel):
    message: str

# 4. Rute Komunikasi Utama (Endpoint)
@app.post("/chat")
async def chat_endpoint(req: ChatRequest):
    print(f"\n[INCOMING MESSAGE] User: {req.message}")
    
    try:
        # Menyerahkan pesan dari React ke Otak NEXUS
        hasil = agent_executor.invoke({"input": req.message})
        print(f"[OUTGOING MESSAGE] NEXUS: {hasil['output']}")
        
        return {"reply": hasil["output"]}
        
    except Exception as e:
        print(f"[FATAL ERROR] {str(e)}")
        return {"reply": f"Maaf, terjadi gangguan pada sistem saraf NEXUS: {str(e)}"}

# Rute pengecekan status server
@app.get("/health")
async def health_check():
    return {"status": "NEXUS Backend Online"}

if __name__ == "__main__":
    print("[INFO] Mengaktifkan Server Uvicorn...")
    uvicorn.run(app, host="127.0.0.1", port=8000)