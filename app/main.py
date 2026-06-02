from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import tempfile, os

print("🚀 AI Autocomplete Keyboard — Server Starting")
IS_PRODUCTION = os.getenv("RENDER", "false") == "true"
app = FastAPI(title="AI Keyboard API", version="2.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from app.engine import AutocompleteEngine
from app.schemas import InputRequest, SelectRequest
from data.training_data import sentences

engine = AutocompleteEngine()
engine.train(sentences)
print(f"✅ Trained on {len(sentences)} sentences")


@app.get("/")
def home():
    return {"message": "AI Keyboard API running", "version": "2.0"}


@app.post("/input")
def process(req: InputRequest):
    print(f"📥 INPUT: '{req.text}' + '{req.char}'")
    result = engine.process_input(req.text, req.char)
    print(f"💡 SUGGESTIONS: {result['suggestions']}")
    return result


@app.post("/select")
def select(req: SelectRequest):
    print(f"✅ SELECT: '{req.word}' in '{req.text}'")
    return engine.select(req.text, req.word)


@app.post("/voice")
async def voice(audio: UploadFile = File(...)):
    """
    Transcribes audio using OpenAI Whisper (Disabled in Production due to RAM limits).
    """
    # 🚀 FOR PRODUCTION: Cut it off immediately to save RAM
    if IS_PRODUCTION:
        return {
            "text": "", 
            "error": "Voice features are running in local-only mode due to cloud server RAM limitations."
        }

    # 💻 FOR LOCALHOST: Keep your existing working logic
    try:
        import whisper
        with tempfile.NamedTemporaryFile(suffix=".webm", delete=False) as tmp:
            tmp.write(await audio.read())
            tmp_path = tmp.name
        
        # Using "tiny" locally is faster and lighter than "base"
        model = whisper.load_model("tiny") 
        result = model.transcribe(tmp_path)
        os.unlink(tmp_path)
        
        return {"text": result["text"].strip()}
        
    except ImportError:
        return {"text": "", "error": "Whisper not installed locally. Run: pip install openai-whisper"}
    except Exception as e:
        return {"text": "", "error": str(e)}
