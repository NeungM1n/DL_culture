from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import torch
from torchvision import transforms
from PIL import Image
import io
from model import get_model
import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

app = FastAPI()

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure Gemini
API_KEY = os.getenv("VITE_API_KEY")
if API_KEY:
    genai.configure(api_key=API_KEY)
else:
    print("Warning: VITE_API_KEY not found in .env")

# Load Model and Classes
MODEL_PATH = 'culture_model.pth'
CLASS_NAMES_PATH = 'class_names.txt'
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

model = None
class_names = []

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

class ChatRequest(BaseModel):
    message: str
    context: str

@app.post("/chat")
async def chat(request: ChatRequest):
    if not API_KEY:
        raise HTTPException(status_code=500, detail="API Key not configured")
    
    try:
        # Use gemini-2.0-flash (Working with billing)
        model = genai.GenerativeModel('gemini-2.0-flash')
        
        prompt = f"""
        당신은 한국 문화재 전문가 AI입니다.
        현재 사용자가 보고 있는 문화재는 '{request.context}'입니다.
        
        사용자의 질문: {request.message}
        
        이 문화재에 대한 정확하고 친절한 설명을 제공해주세요.
        만약 질문이 문화재와 관련이 없다면, 정중하게 문화재 관련 질문을 유도해주세요.
        """
        
        response = model.generate_content(prompt)
        return {"reply": response.text}
    except Exception as e:
        print(f"Chat Error: {e}")
        return {"reply": f"죄송합니다. 오류가 발생했습니다.\n({str(e)})"}

@app.get("/")
def read_root():
    return {"message": "CultureFinder Backend is running"}
