// Python Backend Service

export const analyzeImage = async (file) => {
    const formData = new FormData();
    formData.append('file', file);

    try {
        const response = await fetch('http://localhost:8000/predict', {
            method: 'POST',
            body: formData,
        });

        if (!response.ok) {
            throw new Error(`Backend Error: ${response.statusText}`);
        }

        const data = await response.json();

        if (data.error) {
            throw new Error(data.error);
        }

        return data;
    } catch (error) {
        console.error("Analysis Error:", error);
        // Fallback for demo if backend is offline
        if (error.message.includes("Failed to fetch")) {
            alert("백엔드 서버가 연결되지 않았습니다. 'backend' 폴더에서 'uvicorn main:app --reload'를 실행해주세요.");
        }
        throw error;
    }
};

export const chatWithAI = async (message, context, history) => {
    // Chat is not yet implemented in Python backend
    return `[시스템] 현재 딥러닝 모델 모드에서는 채팅 기능이 제한됩니다.\n식별된 문화재: ${context.name}`;
};
