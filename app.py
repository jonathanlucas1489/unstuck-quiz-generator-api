from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.pdf_reader import extract_text_from_pdf
from app.openai_client import generate_questions
import tempfile

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/generate-questions")
async def generate_questions_from_pdf(file: UploadFile = File(...)):
    print('starting generate_questions_from_pdf')
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name

    text = extract_text_from_pdf(tmp_path)
    
    print(f'text {text}')

    if not text.strip():
        raise HTTPException(status_code=400, detail="The PDF appears to be empty.")

    try:
        questions = generate_questions(text)

        return {"questions": questions}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5001)