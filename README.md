# 🏛️ CultureFinder (문화재 찾기) - AI 기반 문화재 식별 및 가이드 서비스

**딥러닝(Deep Learning)**과 **생성형 AI(LLM)**를 결합하여, 사용자가 촬영한 문화재 사진을 분석하고 3개 국어(한국어, 영어, 중국어)로 상세한 설명을 제공하는 인공지능 웹 애플리케이션입니다.

> **프로젝트 개요**
> 본 프로젝트는 단순한 이미지 분류 모델 구현을 넘어, **데이터셋 구축(수집/증강)부터 모델 학습(PyTorch), 백엔드 API 서버(FastAPI), 그리고 최종 웹 서비스 배포(React)**까지의 전 과정을 아우르는 올인원 딥러닝 프로젝트입니다.

---

## ✨ 주요 기능 (Key Features)

### 1. 📸 실시간 문화재 식별 (Real-time Identification)
*   **카메라/업로드 지원**: 모바일/PC 카메라로 즉시 촬영하거나 고화질 사진을 업로드하여 분석할 수 있습니다.
*   **Top-K 예측**: AI가 가장 확신하는 1순위 결과뿐만 아니라, **2~4순위 후보**도 함께 제시하여 정답 가능성을 보완합니다.

### 2. 🌍 다국어 도슨트 (Multi-language Support)
*   **글로벌 가이드**: 외국인 관광객을 위해 **한국어(KO), 영어(EN), 중국어(ZH)** 3개 국어로 설명을 제공합니다.
*   **자동 생성**: Google Gemini 2.0 Flash 모델을 활용하여 1,500여 개 문화재에 대한 고품질 설명을 자동으로 생성 및 DB화했습니다.

### 3. 🧠 고성능 커스텀 AI 모델
*   **방대한 클래스**: 국보, 보물, 사적 등 총 **1,500개 클래스**를 구분할 수 있는 ResNet18 기반 커스텀 모델입니다.
*   **전이 학습(Transfer Learning)**: ImageNet 사전 학습 가중치를 활용하고, 커스텀 데이터셋으로 Fine-tuning하여 높은 정확도를 확보했습니다.

### 4. 💬 AI 챗봇 (Interactive AI Chat)
*   **심층 질의응답**: 식별된 문화재에 대해 더 궁금한 점이 있다면 AI 챗봇에게 바로 물어볼 수 있습니다.
*   **맥락 인식**: 현재 보고 있는 문화재가 무엇인지 AI가 인지하고 있어, 자연스러운 대화가 가능합니다.

### 5. 🎨 몰입형 UI (Glassmorphism Design)
*   현대적이고 세련된 **글래스모피즘(Glassmorphism)** 디자인 시스템을 적용하여, 앱 사용 경험을 극대화했습니다.

---

## 🛠️ 기술 스택 (Tech Stack)

| 구분 | 기술 스택 | 설명 |
| :--- | :--- | :--- |
| **Frontend** | **React (Vite)** | 빠르고 가벼운 SPA 프레임워크 |
| | **Vanilla CSS** | 커스텀 디자인 시스템 직접 구현 |
| | **Axios** | 비동기 백엔드 API 통신 |
| **Backend** | **Python 3.10+** | 핵심 프로그래밍 언어 |
| | **FastAPI** | 고성능 API 서버 프레임워크 |
| | **Google Gemini** | 설명 데이터 생성 및 챗봇 구현 |
| **Deep Learning** | **PyTorch** | 모델 설계, 학습 및 추론 |
| | **Torchvision** | 이미지 전처리 및 ResNet 모델 로드 |
| | **icrawler** | 이미지 데이터 자동 수집 |

---

## 📂 프로젝트 구조 (File Structure)

### `/backend` (핵심 로직 및 AI)
*   **`model.py`**: ResNet18 모델 아키텍처 정의 (Class 수: 1,500).
*   **`train.py`**: 모델 학습을 위한 메인 스크립트.
    *   *Features*: Resume 학습, Learning Rate Scheduling, Best Model 저장.
*   **`main.py`**: FastAPI 서버. 이미지 분석(`POST /predict`) 및 채팅(`POST /chat`) API 제공.
*   **`generate_descriptions.py`**: **[NEW]** Gemini API를 활용한 다국어 설명 데이터 생성 스크립트.
*   **`descriptions.json`**: 생성된 문화재 설명 데이터 (3개 국어 포함).
*   **`extract_landmarks.py`**: 원시 데이터(`heritage_list.xls`)에서 학습 대상 추출.
*   **`download_images.py` / `augment_dataset.py`**: 데이터 수집 및 증강 파이프라인.

### `/src` (사용자 인터페이스)
*   **`App.jsx`**: 앱의 메인 라우팅 및 상태 관리.
*   **`components/`**: `LandingPage`(입력), `ResultPage`(결과), `ChatInterface`(채팅) 등 화면 구성 요소.
*   **`services/`**: API 통신 로직 모듈화.

---

## 🚀 프로젝트 실행 가이드 (How to Run)

본 프로젝트를 로컬 환경에서 실행하기 위한 단계별 가이드입니다.

### 1. 환경 설정 (Prerequisites)
*   Python 3.10 이상 설치
*   Node.js 및 npm 설치
*   Google Gemini API Key 발급

### 2. 백엔드 설정 및 실행
```bash
# 1. 백엔드 폴더로 이동
cd backend

# 2. 필수 라이브러리 설치
pip install -r requirements.txt

# 3. 환경 변수 설정 (.env 파일 생성)
# VITE_API_KEY=your_google_api_key_here

# 4. 서버 실행
uvicorn main:app --reload
```
*   서버 정상 작동 시: `http://localhost:8000` 접속 가능

### 3. 프론트엔드 설정 및 실행
```bash
# 새 터미널 창을 열고 루트 경로에서 실행
# 1. 의존성 설치
npm install

# 2. 개발 서버 실행
npm run dev
```
*   브라우저에서 `http://localhost:5173` 접속하여 서비스 이용

---

## 📊 데이터셋 및 학습 파이프라인 (Data Pipeline)

본 프로젝트는 데이터의 양과 질을 확보하기 위해 체계적인 파이프라인을 구축했습니다.

1.  **목록 추출**: 문화재청 데이터를 기반으로 학습 가치가 높은 1,500종 선정.
2.  **자동 수집**: 검색 엔진(Bing, Google) 크롤링을 통해 클래스당 초기 이미지 확보.
3.  **데이터 정제**: 손상된 이미지 제거 및 형식 통일 (RGB, Resize).
4.  **데이터 증강**: 회전(Rotation), 반전(Flip), 색상 변환(Color Jitter) 등을 통해 데이터 다양성 확보 (강건한 모델 학습).
5.  **다국어 데이터 생성**: LLM을 활용하여 정제된 텍스트 데이터 베이스 구축.

---

## 🎓 결론 및 기대 효과

이 프로젝트는 최신 AI 기술을 활용하여 **'문화재'라는 전통적인 소재를 현대적인 서비스로 재해석**했습니다.
특히 다국어 지원을 통해 내국인뿐만 아니라 외국인 관광객들에게도 우리 문화유산의 가치를 효과적으로 전달할 수 있는 가능성을 제시합니다.

---

**Project Members**
*   [팀원 이름 1] - 모델 설계 및 학습, 데이터셋 구축
*   [팀원 이름 2] - 백엔드 API 개발, 프롬프트 엔지니어링
*   [팀원 이름 3] - 프론트엔드 UI/UX 개발, 서비스 연동
