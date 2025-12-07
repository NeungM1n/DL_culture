import os
import json
import google.generativeai as genai
from dotenv import load_dotenv
import time
from tqdm import tqdm

# Load environment variables
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

# Configure Gemini
API_KEY = os.getenv("VITE_API_KEY")
if not API_KEY:
    print("Error: VITE_API_KEY not found in .env")
    exit(1)

genai.configure(api_key=API_KEY)
# Updated model name based on available models (Confirmed 2.0 Flash exists)
model = genai.GenerativeModel('gemini-2.0-flash')

def generate_descriptions():
    # Load landmarks
    if not os.path.exists('landmarks.txt'):
        print("Error: landmarks.txt not found.")
        return

    with open('landmarks.txt', 'r', encoding='utf-8') as f:
        landmarks = [line.strip() for line in f if line.strip()]

    print(f"Loaded {len(landmarks)} landmarks.")

    # Load existing descriptions
    descriptions = {}
    if os.path.exists('descriptions.json'):
        with open('descriptions.json', 'r', encoding='utf-8') as f:
            descriptions = json.load(f)
    
    print(f"Loaded {len(descriptions)} existing descriptions.")

    # Filter out already processed
    to_process = [name for name in landmarks if name not in descriptions]
    print(f"Remaining to process: {len(to_process)}")

    # Batch processing to save time/calls
    batch_size = 20
    
    for i in range(0, len(to_process), batch_size):
        batch = to_process[i:i+batch_size]
        print(f"Processing batch {i//batch_size + 1}/{len(to_process)//batch_size + 1}...")
        
        prompt = "다음 문화재들에 대해 1~2문장으로 핵심만 요약해서 설명해줘. JSON 형식으로 반환해. 키는 문화재 이름, 값은 설명.\n\n"
        prompt += "\n".join(batch)
        
        try:
            response = model.generate_content(prompt)
            text = response.text.replace("```json", "").replace("```", "").strip()
            
            try:
                batch_results = json.loads(text)
                descriptions.update(batch_results)
                
                # Save progress immediately
                with open('descriptions.json', 'w', encoding='utf-8') as f:
                    json.dump(descriptions, f, ensure_ascii=False, indent=4)
                    
            except json.JSONDecodeError:
                print(f"JSON Error in batch {i}. Skipping...")
                print(text)
                
            time.sleep(1) # Rate limit prevention
            
        except Exception as e:
            print(f"API Error: {e}")
            time.sleep(5)

    print("Description generation complete!")

if __name__ == "__main__":
    generate_descriptions()
