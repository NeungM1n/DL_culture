# 🏛️ CultureFinder (문화재 찾기) - AI 기반 문화재 식별 서비스

**CultureFinder**는 딥러닝(Deep Learning) 기술을 활용하여 사용자가 촬영한 문화재 사진을 분석하고, 해당 문화재의 이름과 상세 정보를 실시간으로 제공하는 웹 애플리케이션입니다.

단순한 이미지 검색을 넘어, **나만의 데이터셋을 구축하고 직접 AI 모델을 학습**시킬 수 있는 교육적이고 실용적인 프로젝트입니다.

---

## ✨ 주요 기능 (Key Features)

1.  **📸 실시간 카메라 촬영 및 분석**
    *   웹 브라우저에서 직접 카메라를 구동하여 문화재를 촬영합니다.
    *   촬영된 이미지는 즉시 서버로 전송되어 AI 분석을 거칩니다.
2.  **📂 이미지 업로드 지원**
    *   PC나 모바일에 저장된 고화질 문화재 사진을 업로드하여 분석할 수 있습니다.
3.  **🧠 고성능 AI 모델 (ResNet18)**
    *   수백만 장의 이미지로 사전 학습된(Pre-trained) **ResNet18** 모델을 사용하여, 적은 데이터로도 높은 정확도를 보여줍니다.
4.  **📝 풍부한 문화재 설명**
    *   단순히 이름만 알려주는 것이 아니라, 해당 문화재의 역사적 배경과 설명을 함께 제공합니다.
5.  **🎨 Glassmorphism UI 디자인**
    *   최신 디자인 트렌드인 글래스모피즘(유리 같은 질감)을 적용하여 심미적으로 우수한 사용자 경험을 제공합니다.

---

## 🛠️ 기술 스택 및 도구 (Tech Stack & Tools)

이 프로젝트는 최신 웹 기술과 검증된 AI 프레임워크를 사용하여 구축되었습니다.

### 🖥️ Frontend (프론트엔드)
*   **React (v18+)**: 컴포넌트 기반의 UI 라이브러리로, 재사용 가능한 UI 요소를 만들기 위해 사용했습니다.
*   **Vite**: 기존 Webpack보다 월등히 빠른 빌드 속도와 개발 서버 구동을 위해 채택했습니다.
*   **JavaScript (ES6+)**: 최신 자바스크립트 문법(Async/Await 등)을 사용하여 비동기 통신을 구현했습니다.
*   **Vanilla CSS**: 외부 UI 라이브러리(Bootstrap 등) 없이 순수 CSS 변수(`var(--primary-color)`)와 Flexbox/Grid를 사용하여 커스텀 디자인을 구현했습니다.
*   **HTML5 Media Devices API**: 별도의 플러그인 없이 브라우저에서 카메라에 접근하기 위해 `navigator.mediaDevices`를 사용했습니다.

### 🔙 Backend (백엔드)
*   **Python (v3.10+)**: AI 라이브러리와의 호환성이 가장 뛰어난 언어로 백엔드를 구축했습니다.
*   **FastAPI**: Flask보다 빠르고 자동 문서화(Swagger UI)를 지원하는 최신 웹 프레임워크입니다. 비동기 처리(`async def`)를 통해 다수의 요청을 효율적으로 처리합니다.
*   **Uvicorn**: FastAPI를 실행하기 위한 고성능 ASGI(Asynchronous Server Gateway Interface) 서버입니다.

### 🧠 AI & Deep Learning (인공지능)
*   **PyTorch**: 페이스북(Meta)에서 개발한 딥러닝 프레임워크로, 직관적인 코드 작성이 가능하여 채택했습니다.
*   **Torchvision**: 이미지 변환(Resize, Normalize) 및 사전 학습된 모델(ResNet18)을 불러오기 위해 사용했습니다.
*   **Transfer Learning (전이 학습)**: ImageNet 데이터셋으로 미리 학습된 모델의 지식을 빌려와, 적은 수의 문화재 사진으로도 빠르게 학습시키는 기법을 적용했습니다.

---

## 📂 프로젝트 파일 구조 및 상세 설명 (File Descriptions)

각 파일이 어떤 역할을 하는지 상세하게 설명합니다.

### 1. Backend (`/backend`) - AI 및 서버 로직
*   **`main.py` (핵심)**: FastAPI 서버의 진입점입니다.
    *   프론트엔드에서 보내온 이미지를 받아서(`POST /predict`), 모델에 넣고 결과를 돌려주는 API가 정의되어 있습니다.
    *   CORS(Cross-Origin Resource Sharing) 설정을 통해 프론트엔드와의 통신을 허용합니다.
*   **`model.py`**: AI 모델의 설계도입니다.
    *   `get_model(num_classes)` 함수가 정의되어 있으며, 여기서 ResNet18 모델을 불러오고 마지막 출력층을 우리가 원하는 문화재 개수만큼 수정합니다.
*   **`train.py`**: AI를 학습시키는 선생님 역할을 하는 스크립트입니다.
    *   `dataset` 폴더의 이미지를 읽어와서 모델을 학습(Training)시킵니다.
    *   학습이 끝나면 `culture_model.pth`(두뇌)와 `class_names.txt`(정답지)를 생성합니다.
*   **`check_dataset.py`**: 데이터가 잘 준비되었는지 검사하는 도구입니다.
    *   폴더별로 이미지가 10장 이상 있는지, 설명(`descriptions.json`)은 있는지 확인해 줍니다.
*   **`download_images.py`**: 이미지 수집 도우미입니다.
    *   구글 이미지 검색을 크롤링하여 원하는 검색어의 이미지를 자동으로 다운로드해 줍니다.
*   **`descriptions.json`**: 문화재 설명 데이터베이스입니다.
    *   AI가 "경복궁"이라고 판단했을 때, 사용자에게 보여줄 상세 설명 텍스트가 저장되어 있습니다.

### 2. Frontend (`/src`) - 사용자 화면
*   **`App.jsx`**: 웹사이트의 전체 레이아웃을 담당하는 메인 컴포넌트입니다.
*   **`components/LandingPage.jsx`**: 사용자가 처음 마주하는 화면입니다.
    *   파일 업로드 버튼, 카메라 켜기 버튼, 그리고 카메라 모달(Modal) UI가 구현되어 있습니다.
    *   카메라 촬영 로직(`startCamera`, `captureImage`)이 포함되어 있습니다.
*   **`services/aiService.js`**: 백엔드와 통신하는 우체부 역할을 합니다.
    *   `analyzeImage` 함수가 이미지를 백엔드 API(`http://localhost:8000/predict`)로 전송하고 결과를 받아옵니다.
*   **`index.css`**: 웹사이트의 모든 디자인(색상, 폰트, 애니메이션, 글래스모피즘 효과)이 정의된 스타일 시트입니다.

---

## 🚀 전체 실행 가이드 (Step-by-Step Guide)

### 1단계: 데이터 수집 (Data Collection)
AI가 공부할 교과서(사진)를 만드는 단계입니다.

1.  `backend` 폴더에서 터미널을 엽니다.
2.  이미지 다운로드 도구를 실행합니다.
    ```bash
    python download_images.py
    ```
3.  원하는 문화재 이름(영어)과 장수를 입력합니다. (예: `gyeongbokgung`, `20`)
4.  최소 2개 이상의 문화재를 수집하는 것을 권장합니다. (비교 대조를 위해)

### 2단계: AI 모델 학습 (Training)
수집한 데이터를 바탕으로 AI를 학습시키는 단계입니다.

1.  학습 스크립트를 실행합니다.
    ```bash
    python train.py
    ```
2.  화면에 `Epoch 1/10...`과 같이 학습 진행 상황이 표시됩니다.
3.  학습이 완료되면 `Training complete` 메시지가 뜨고, `culture_model.pth` 파일이 생성됩니다.

### 3단계: 서비스 실행 (Run)
이제 학습된 AI를 탑재한 서버와 화면을 켤 차례입니다. **터미널 2개**가 필요합니다.

**터미널 1: 백엔드 서버 (Backend)**
```bash
cd backend
uvicorn main:app --reload
```
*   성공 시: `Application startup complete` 메시지 출력

**터미널 2: 프론트엔드 화면 (Frontend)**
```bash
# 프로젝트 최상위 폴더에서
npm run dev
```
*   성공 시: `Local: http://localhost:5173/` 메시지 출력

### 4단계: 사용하기
1.  브라우저 주소창에 `http://localhost:5173`을 입력합니다.
2.  **"카메라 켜기"** 버튼을 누르고 문화재를 비춰보거나, 사진을 업로드합니다.
3.  AI가 분석한 결과와 설명을 확인합니다! 🎉

---

## 📝 라이선스 및 참고사항
이 프로젝트는 포트폴리오 및 학습용으로 제작되었습니다. 상업적 목적으로 사용할 경우 이미지 저작권 등에 유의하시기 바랍니다.
