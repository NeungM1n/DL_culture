import os
import json
import time
import google.generativeai as genai

# Setup Gemini API
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    # Try to load from .env if safe
    from dotenv import load_dotenv
    load_dotenv()
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

genai.configure(api_key=GOOGLE_API_KEY)
# Use gemini-2.0-flash as it is free and fast
model = genai.GenerativeModel('gemini-2.0-flash')

def generate_descriptions():
    # Load landmarks
    with open('landmarks.txt', 'r', encoding='utf-8') as f:
        landmarks = [line.strip() for line in f if line.strip()]
    
    print(f"Loaded {len(landmarks)} landmarks.")

    # Load existing descriptions
    descriptions = {}
    if os.path.exists('descriptions.json'):
        with open('descriptions.json', 'r', encoding='utf-8') as f:
            existing_data = json.load(f)
            # Migration logic: Convert old strings or partial objects to new schema
            for key, value in existing_data.items():
                descriptions[key] = {}
                # Check if value is string (Oldest format)
                if isinstance(value, str):
                    descriptions[key]['ko'] = {"name": key, "description": value}
                    continue
                
                # Check if value is object (Intermediate format)
                if isinstance(value, dict):
                    for lang in ['ko', 'en', 'zh']:
                        if lang in value:
                            content = value[lang]
                            if isinstance(content, str):
                                # Convert string desc to object with name
                                name_val = key if lang == 'ko' else "" # Name might be missing for en/zh
                                descriptions[key][lang] = {"name": name_val, "description": content}
                            else:
                                # Already in new format
                                descriptions[key][lang] = content
    
    print(f"Loaded {len(descriptions)} existing descriptions (migrated).")

    # Filter out items that need processing
    # We need to process if:
    # 1. Key is missing
    # 2. Any language (ko, en, zh) is missing
    # 3. Any language has empty name (optional, but good to have)
    to_process = []
    for name in landmarks:
        if name not in descriptions:
            to_process.append(name)
            continue
        
        is_complete = True
        for lang in ['ko', 'en', 'zh']:
            if lang not in descriptions[name]:
                is_complete = False
                break
            # Optional: Check if name is present
            if not descriptions[name][lang].get('name'):
                is_complete = False
                break
        
        if not is_complete:
            to_process.append(name)

    print(f"Remaining to process: {len(to_process)}")

    # Batch processing
    batch_size = 5 # Small batch size for complex JSON
    
    for i in range(0, len(to_process), batch_size):
        batch = to_process[i:i+batch_size]
        print(f"Processing batch {i//batch_size + 1}/{len(to_process)//batch_size + 1}...")
        print(f"Items: {batch}")
        
        prompt = "다음 문화재들에 대해 한국어(ko), 영어(en), 중국어(zh)로 각각 '이름'과 '설명'을 작성해줘. \n"
        prompt += "반드시 올바른 JSON 형식으로 반환해. \n"
        prompt += "키는 문화재의 한국어 이름이고, 값은 'ko', 'en', 'zh' 각각에 대해 'name'(해당 언어 표기 이름)과 'description'(1~2문장 요약)을 가진 객체여야 해.\n"
        prompt += "예시: {\"숭례문\": {\"ko\": {\"name\": \"숭례문\", \"description\": \"...\"}, \"en\": {\"name\": \"Sungnyemun Gate\", \"description\": \"...\"}, \"zh\": {\"name\": \"崇礼门\", \"description\": \"...\"}}}\n"
        prompt += "주의: 응답은 오직 JSON만 포함해야 해.\n\n"
        prompt += "\n".join(batch)
        
        try:
            response = model.generate_content(prompt)
            text = response.text.replace("```json", "").replace("```", "").strip()
            
            try:
                batch_results = json.loads(text)
                # Merge results carefully
                for k, v in batch_results.items():
                    # Ensure v has the correct structure structure
                    descriptions[k] = v
                
                # Save immediately
                with open('descriptions.json', 'w', encoding='utf-8') as f:
                    json.dump(descriptions, f, ensure_ascii=False, indent=2)
                    
            except json.JSONDecodeError:
                print(f"JSON Decode Error in batch {i}. Text: {text[:100]}...")
                
        except Exception as e:
            print(f"Error processing batch {i}: {e}")
            time.sleep(5)
            
        time.sleep(1)

if __name__ == "__main__":
    generate_descriptions()
