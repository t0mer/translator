from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import MarianTokenizer, MarianMTModel
import torch
import uvicorn
from loguru import logger

app = FastAPI(title="Hebrew ↔ English Translator")

class TranslationRequest(BaseModel):
    text: str

# Auto-detect device (GPU if available)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Load model and tokenizer
model_name = "Helsinki-NLP/opus-mt-tc-big-he-en"
tokenizer = MarianTokenizer.from_pretrained(model_name)
model = MarianMTModel.from_pretrained(model_name).to(device)
model.eval()

@app.post("/translate")
def translate(req: TranslationRequest):
    try:
        inputs = tokenizer(req.text, return_tensors="pt", padding=True).to(device)
        with torch.no_grad():
            translated = model.generate(**inputs)
        output = tokenizer.decode(translated[0], skip_special_tokens=True)
        return {"translated_text": output}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    logger.info("Starting the service")
    uvicorn.run(app, host="0.0.0.0", port=7020)