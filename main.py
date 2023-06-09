from fastapi import FastAPI, UploadFile, File
from transformers import pipeline
from paddleocr import PaddleOCR, draw_ocr
from PIL import Image
import os
from pyngrok import ngrok
import numpy as np
from fastapi.middleware.cors import CORSMiddleware

public_url = ngrok.connect(8000).public_url
print(f"Public URL: {public_url}")
app = FastAPI()

model_name = "deepset/roberta-base-squad2"
nlp = pipeline('question-answering', model=model_name, tokenizer=model_name)

def extract_text_from_image(image_path):
    ocr = PaddleOCR(use_angle_cls=True, lang="en")
    image = Image.open(image_path)
    image_array = np.array(image)
    result = ocr.ocr(image_array)
    text = ''
    for res in result:
        for line in res:
            text += line[1][0]
    return text

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow access from any origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/extract-information")
async def extract_information(image: UploadFile = File(...)):
    image_path = f"{image.filename}"
    with open(image_path, "wb") as f:
        f.write(image.file.read())
    text = extract_text_from_image(image_path)

    answers = []
    QA_input4 = {
        'question': 'what is the Name of the shop?',
        'context': text
    }
    answers.append("Store Name: " + nlp(QA_input4)['answer'])

    QA_input1 = {
        'question': 'what is the invoice number in the bill?',
        'context': text
    }
    answers.append("Invoice Number: " + nlp(QA_input1)['answer'])

    QA_input2 = {
        'question': 'what is the date in the bill?',
        'context': text
    }
    answers.append("Date: " + nlp(QA_input2)['answer'])

    QA_input3 = {
        'question': 'what is the final total amount or cash amount in the bill?',
        'context': text
    }
    answers.append("Total Amount: " + nlp(QA_input3)['answer'])

    os.remove(image_path)

    return {"answers": answers}

@app.get("/answers", response_model=dict)
async def get_answers():
    return {"answers": answers}
