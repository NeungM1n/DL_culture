import os
import json

def check_data():
    dataset_dir = 'dataset'
    json_path = 'descriptions.json'
    
    print("🔍 데이터셋 점검을 시작합니다...\n")

    if not os.path.exists(dataset_dir):
        print(f"❌ '{dataset_dir}' 폴더가 없습니다. 'backend' 폴더 안에 'dataset' 폴더를 만들어주세요!")
        return

    folders = [f for f in os.listdir(dataset_dir) if os.path.isdir(os.path.join(dataset_dir, f))]
    
    if not folders:
        print(f"⚠️ '{dataset_dir}' 폴더 안에 문화재 이름으로 된 폴더가 하나도 없습니다.")
        print("   예: backend/dataset/gyeongbokgung/")
        return

    print(f"✅ 총 {len(folders)}개의 문화재 클래스를 발견했습니다:\n")
    
    # Load JSON to check descriptions
    descriptions = {}
    if os.path.exists(json_path):
        with open(json_path, 'r', encoding='utf-8') as f:
            try:
                descriptions = json.load(f)
            except:
                print("⚠️ descriptions.json 파일 형식이 잘못되었습니다.")
    
    all_good = True
    
    for folder in folders:
        path = os.path.join(dataset_dir, folder)
        images = [f for f in os.listdir(path) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp'))]
        count = len(images)
        
        status = "✅ 충분함" if count >= 10 else "⚠️ 부족함 (10장 이상 권장)"
        desc_status = "✅ 설명 있음" if folder in descriptions else "❌ 설명 없음"
        
        print(f"  📂 [{folder}]")
        print(f"     - 이미지: {count}장 -> {status}")
        print(f"     - 설  명: {desc_status}")
        
        if count < 10 or folder not in descriptions:
            all_good = False
        print("")

    if all_good:
        print("🎉 모든 준비가 완료되었습니다! 'python train.py'를 실행해서 학습을 시작하세요.")
    else:
        print("💡 위에서 '부족함'이나 '설명 없음'으로 표시된 부분을 채워주세요.")

if __name__ == "__main__":
    check_data()
