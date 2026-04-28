from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

print("🔥 MAIN FILE LOADED")

app = FastAPI()

# ✅ CORS MUST BE IMMEDIATELY AFTER APP CREATION
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---- imports AFTER middleware ----
from app.engine import AutocompleteEngine
from app.schemas import InputRequest, SelectRequest
from data.training_data import sentences

engine = AutocompleteEngine()
engine.train(sentences)


@app.get("/")
def home():
    return {"message": "API running"}


@app.post("/input")
def process(req: InputRequest):
    print("🔥 /input HIT:", req)
    return engine.process_input(req.text, req.char)


@app.post("/select")
def select(req: SelectRequest):
    print("🔥 /select HIT:", req)
    return engine.select(req.text, req.word)
