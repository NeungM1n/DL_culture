from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import torch
from torchvision import transforms
from PIL import Image
import io
from model import get_model
import os

app = FastAPI()

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load Model and Classes
MODEL_PATH = 'culture_model.pth'
CLASS_NAMES_PATH = 'class_names.txt'
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

model = None
class_names = []

import json

# Load Descriptions
DESCRIPTIONS_PATH = 'descriptions.json'
DESCRIPTIONS = {}

def load_descriptions():
    global DESCRIPTIONS
    if os.path.exists(DESCRIPTIONS_PATH):
        with open(DESCRIPTIONS_PATH, 'r', encoding='utf-8') as f:
            DESCRIPTIONS = json.load(f)
    else:
        print("descriptions.json not found. Using empty descriptions.")

load_descriptions()

def load_artifacts():
    global model, class_names
    if os.path.exists(CLASS_NAMES_PATH):
        with open(CLASS_NAMES_PATH, 'r', encoding='utf-8') as f:
            class_names = [line.strip() for line in f.readlines()]
        
        model = get_model(len(class_names))
        if os.path.exists(MODEL_PATH):
            model.load_state_dict(torch.load(MODEL_PATH, map_location=device))
            model.to(device)
            model.eval()
            print("Model loaded successfully.")
        else:
            print("Model file not found. Please train the model first.")
    else:
        print("Class names file not found. Please train the model first.")

# Load on startup
load_artifacts()

def transform_image(image_bytes):
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])
    image = Image.open(io.BytesIO(image_bytes)).convert('RGB')
    return transform(image).unsqueeze(0)

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    if model is None:
        return {"error": "Model not loaded. Please train the model first."}
    
    image_bytes = await file.read()
    tensor = transform_image(image_bytes).to(device)
    
    with torch.no_grad():
        outputs = model(tensor)
        probabilities = torch.nn.functional.softmax(outputs, dim=1)
        confidence, predicted = torch.max(probabilities, 1)
        
    class_name = class_names[predicted.item()]
    confidence_score = int(confidence.item() * 100)
    
    # Get top 3 alternatives
    top3_prob, top3_idx = torch.topk(probabilities, min(3, len(class_names)))
    alternatives = [class_names[idx.item()] for idx in top3_idx[0] if idx.item() != predicted.item()]
    
    description = DESCRIPTIONS.get(class_name, "설명이 준비되지 않은 문화재입니다.")
    
    return {
        "name": class_name,
        "description": description,
        "matchPercentage": confidence_score,
        "alternatives": alternatives
    }

@app.get("/")
def read_root():
    return {"message": "CultureFinder Backend is running"}
