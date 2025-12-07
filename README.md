# 🏛️ CultureFinder (문화재 찾기) - AI 기반 문화재 식별 서비스

**CultureFinder**는 딥러닝(Deep Learning)과 생성형 AI(LLM)를 결합하여, 사용자가 촬영한 문화재 사진을 분석하고 상세한 설명을 제공하는 웹 애플리케이션입니다.

단순한 이미지 분류를 넘어, **나만의 데이터셋 구축부터 원격 GPU 서버 학습, 그리고 웹 서비스 배포까지** 경험할 수 있는 올인원 프로젝트입니다.

---

## ✨ 주요 기능 (Key Features)

1.  **📸 실시간 촬영 및 분석**
    *   웹 브라우저에서 카메라를 구동하여 즉시 분석하거나, 고화질 사진을 업로드할 수 있습니다.
2.  **🧠 고성능 AI 모델 (ResNet18 + Custom Training)**
    *   **1,500여 개의 주요 문화재(국보, 보물, 사적)**를 식별할 수 있는 커스텀 모델을 탑재했습니다.
    *   데이터 증강(Augmentation)과 전이 학습(Transfer Learning)을 통해 높은 정확도를 확보했습니다.
3.  **🥈 대안 제시 (Top 4 Alternatives)**
    *   AI가 가장 확신하는 정답뿐만 아니라, 2, 3, 4순위 후보도 함께 보여주어 정확도를 보완합니다.
    *   사용자가 "이게 아닌데?" 싶을 때 다른 후보를 선택하여 바로잡을 수 있습니다.
4.  **💬 AI 도슨트 (LLM Chat)**
    *   **Google Gemini 2.0 Flash** 모델이 탑재되어, 식별된 문화재에 대해 궁금한 점을 자유롭게 물어볼 수 있습니다.
    *   문화재의 역사, 특징, 관람 포인트 등을 대화하듯 알려줍니다.
5.  **🎨 Glassmorphism UI**
    *   현대적이고 세련된 글래스모피즘 디자인을 적용하여 몰입감 있는 사용자 경험을 제공합니다.

---

## 🛠️ 기술 스택 (Tech Stack)

### Frontend
*   **React (Vite)**: 빠르고 가벼운 프론트엔드 개발 환경
*   **Vanilla CSS**: Glassmorphism 디자인 시스템 직접 구현 (No Framework)
*   **Axios**: 백엔드 API 통신

### Backend
*   **Python 3.10+**: 핵심 언어
*   **FastAPI**: 고성능 비동기 웹 프레임워크 (API 서버)
*   **Uvicorn**: ASGI 서버
*   **Google Generative AI (Gemini)**: LLM 기반 챗봇 및 설명 생성

### AI / Deep Learning
*   **PyTorch**: 딥러닝 모델 학습 및 추론
*   **Torchvision**: ResNet18 모델 및 이미지 전처리/증강
*   **Pandas**: 데이터셋 메타데이터 처리 (`heritage_list.xls`)
*   **icrawler**: 이미지 데이터 자동 수집

---

## 📂 프로젝트 파일 구조 (File Structure)

### 1. Backend (`/backend`)
*   **`main.py`**: FastAPI 서버의 진입점. 이미지 분석(`/predict`) 및 채팅(`/chat`) API를 제공합니다.
*   **`train.py`**: AI 모델 학습 스크립트.
    *   `--resume`: 중단된 학습 이어하기 기능
    *   `Scheduler`: 학습률 자동 조절 (ReduceLROnPlateau)
    *   `Best Model Saving`: 최고 성능 모델 자동 저장
*   **`model.py`**: ResNet18 모델 정의 및 수정 (Transfer Learning).
*   **`download_images.py`**: `landmarks.txt`에 있는 문화재 목록을 바탕으로 이미지를 자동 수집합니다. (병렬 처리 지원)
*   **`augment_dataset.py`**: 부족한 데이터를 회전/반전/색변환하여 목표 수량까지 자동으로 증강합니다. (Multiprocessing 지원)
*   **`extract_landmarks.py`**: 엑셀 파일(`heritage_list.xls`)에서 주요 문화재(국보, 보물 등) 1,500개를 추출합니다.
*   **`generate_descriptions.py`**: Gemini API를 이용해 1,500개 문화재의 설명을 자동으로 생성하여 `descriptions.json`에 저장합니다.
*   **`evaluate_model.py`**: 학습된 모델의 성능을 정밀 분석(Top-5 정확도, 오답 노트)합니다.

### 2. Frontend (`/src`)
*   **`App.jsx`**: 전체 앱의 상태 관리 (화면 전환, 결과 데이터 유지).
*   **`components/LandingPage.jsx`**: 카메라 촬영 및 파일 업로드 화면.
*   **`components/ResultPage.jsx`**: 분석 결과 표시, 대안 선택, 채팅 진입 화면.
*   **`components/ChatInterface.jsx`**: AI와의 실시간 채팅 화면.
*   **`services/aiService.js`**: 백엔드 API 호출 로직 분리.

---

## 🚀 데이터셋 구축 및 학습 가이드 (Workflow)

이 프로젝트는 **데이터 수집 -> 증강 -> 학습 -> 배포**의 전체 파이프라인을 포함합니다.

### 1. 데이터 준비
```bash
# 1. 문화재 목록 추출
python extract_landmarks.py

# 2. 이미지 다운로드 (서버 권장)
python download_images.py --batch --count 50

# 3. 데이터 증강 (서버 권장)
python augment_dataset.py --target 200
```

### 2. 모델 학습 (Remote Server)
```bash
# 학습 시작 (50 Epoch, Batch 32)
python train.py --epochs 50 --batch 32

# (선택) 학습 중단 시 이어하기
python train.py --epochs 50 --batch 32 --resume
```

### 3. 설명 데이터 생성
```bash
# Gemini가 설명 자동 작성
python generate_descriptions.py
```

---

## 🏃‍♂️ 실행 방법 (How to Run)

학습이 완료된 후, 웹 서비스를 실행하는 방법입니다.

### 1. Backend 실행
```bash
cd backend
# 가상환경 활성화 (선택)
# conda activate dl_pj7 

uvicorn main:app --reload
```
*   서버가 `http://localhost:8000`에서 실행됩니다.

### 2. Frontend 실행
```bash
# 새 터미널에서 실행
npm run dev
```
*   브라우저가 `http://localhost:5173`에서 실행됩니다.

---

## ⚠️ 주의사항 (Troubleshooting)

*   **API Key**: `backend/.env` 파일에 `VITE_API_KEY`가 올바르게 설정되어 있어야 채팅 및 설명 생성이 가능합니다.
*   **Model File**: `backend/culture_model.pth` 파일이 없으면 서버가 시작되지 않습니다. (학습 후 다운로드 필요)
*   **CORS**: 프론트엔드와 백엔드의 포트가 다르므로 `main.py`의 CORS 설정이 중요합니다. (현재 모든 오리진 허용됨)

---

**Developed by [Your Name]**
*Powered by Google Gemini & PyTorch*
