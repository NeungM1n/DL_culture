import React, { useState } from 'react';
import LandingPage from './components/LandingPage';
import ResultPage from './components/ResultPage';
import ChatInterface from './components/ChatInterface';
import { analyzeImage } from './services/aiService';
import './index.css';

function App() {
  const [currentView, setCurrentView] = useState('landing'); // landing, loading, result, chat
  const [analysisResult, setAnalysisResult] = useState(null);
  const [selectedImage, setSelectedImage] = useState(null);

  const handleImageUpload = async (file) => {
    setSelectedImage(URL.createObjectURL(file));
    setCurrentView('loading');

    try {
      const result = await analyzeImage(file);
      setAnalysisResult(result);
      setCurrentView('result');
    } catch (error) {
      console.error(error);
      alert("분석 중 오류가 발생했습니다: " + error.message);
      setCurrentView('landing');
    }
  };

  const handleReset = () => {
    setCurrentView('landing');
    setAnalysisResult(null);
    setSelectedImage(null);
  };

  const handleSelectAlternative = (alternative) => {
    setAnalysisResult(prev => ({
      ...prev,
      name: alternative.name,
      description: alternative.description,
      matchPercentage: alternative.confidence
    }));
  };

  return (
    <div className="app-container" style={{ width: '100%', maxWidth: '600px', padding: '20px' }}>
      {currentView === 'landing' && (
        <LandingPage onUpload={handleImageUpload} />
      )}

      {currentView === 'loading' && (
        <div className="glass-panel animate-fade-in" style={{ textAlign: 'center' }}>
          <div className="loader" style={{ fontSize: '2rem', marginBottom: '1rem' }}>🔍</div>
          <h2>문화재를 분석하고 있습니다...</h2>
          <p>잠시만 기다려주세요.</p>
        </div>
      )}

      {currentView === 'result' && analysisResult && (
        <ResultPage
          result={analysisResult}
          image={selectedImage}
          onReset={handleReset}
          onChat={() => setCurrentView('chat')}
          onSelectAlternative={handleSelectAlternative}
        />
      )}

      {currentView === 'chat' && (
        <ChatInterface
          context={analysisResult}
          onBack={() => setCurrentView('result')}
        />
      )}
    </div>
  );
}

export default App;
