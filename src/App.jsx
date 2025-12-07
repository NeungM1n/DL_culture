import React, { useState } from 'react';
import LandingPage from './components/LandingPage';
import ResultPage from './components/ResultPage';
import ChatInterface from './components/ChatInterface';
import { analyzeImage } from './services/aiService';
import { translations } from './translations';
import './index.css';

function App() {
  const [currentView, setCurrentView] = useState('landing'); // landing, loading, result, chat
  const [analysisResult, setAnalysisResult] = useState(null);
  const [selectedImage, setSelectedImage] = useState(null);
  const [language, setLanguage] = useState('ko'); // Global language state

  const t = translations[language]; // Translation helper

  const handleImageUpload = async (file) => {
    setSelectedImage(URL.createObjectURL(file));
    setCurrentView('loading');

    try {
      const result = await analyzeImage(file);
      setAnalysisResult(result);
      setCurrentView('result');
    } catch (error) {
      console.error(error);
      alert(t.error_analysis + error.message);
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
    <div className="app-container" style={{ width: '100%', maxWidth: '800px', padding: '20px', position: 'relative' }}>
      {/* Language Switcher */}
      <div style={{ position: 'absolute', top: '20px', right: '20px', zIndex: 100, display: 'flex', gap: '5px' }}>
        {['ko', 'en', 'zh'].map(lang => (
          <button
            key={lang}
            onClick={() => setLanguage(lang)}
            style={{
              background: language === lang ? 'var(--primary-color)' : 'rgba(255,255,255,0.2)',
              color: language === lang ? '#000' : '#fff',
              border: 'none',
              padding: '5px 10px',
              borderRadius: '15px',
              cursor: 'pointer',
              fontWeight: language === lang ? 'bold' : 'normal',
              fontSize: '0.8rem',
              backdropFilter: 'blur(5px)'
            }}
          >
            {lang === 'ko' ? 'KR' : lang === 'en' ? 'EN' : 'CN'}
          </button>
        ))}
      </div>

      {currentView === 'landing' && (
        <LandingPage onUpload={handleImageUpload} t={t} />
      )}

      {currentView === 'loading' && (
        <div className="glass-panel animate-fade-in" style={{ textAlign: 'center' }}>
          <div className="loader" style={{ fontSize: '2rem', marginBottom: '1rem' }}>🔍</div>
          <h2>{t.analyzing_title}</h2>
          <p>{t.analyzing_desc}</p>
        </div>
      )}

      {currentView === 'result' && analysisResult && (
        <ResultPage
          result={analysisResult}
          image={selectedImage}
          onReset={handleReset}
          onChat={() => setCurrentView('chat')}
          onSelectAlternative={handleSelectAlternative}
          language={language}
          t={t}
        />
      )}

      {currentView === 'chat' && (
        <ChatInterface
          context={analysisResult}
          onBack={() => setCurrentView('result')}
          language={language}
          t={t}
        />
      )}
    </div>
  );
}

export default App;
