import React, { useRef } from 'react';

const LandingPage = ({ onUpload }) => {
    const fileInputRef = useRef(null);

    const handleFileChange = (e) => {
        const file = e.target.files[0];
        if (file) {
            onUpload(file);
        }
    };

    return (
        <div className="glass-panel animate-fade-in" style={{ textAlign: 'center', padding: '3rem 2rem' }}>
            <h1 style={{ fontSize: '2.5rem', marginBottom: '1rem', color: 'var(--primary-color)' }}>
                문화재 찾기
            </h1>
            <p style={{ marginBottom: '2rem', color: 'var(--text-secondary)' }}>
                사진을 찍거나 업로드하여<br />우리 문화재의 이야기를 들어보세요.
            </p>

            <div
                style={{
                    border: '2px dashed var(--glass-border)',
                    borderRadius: '16px',
                    padding: '2rem',
                    marginBottom: '2rem',
                    cursor: 'pointer',
                    transition: 'border-color 0.3s'
                }}
                onClick={() => fileInputRef.current.click()}
                onMouseOver={(e) => e.currentTarget.style.borderColor = 'var(--primary-color)'}
                onMouseOut={(e) => e.currentTarget.style.borderColor = 'var(--glass-border)'}
            >
                <div style={{ fontSize: '3rem', marginBottom: '1rem' }}>📸</div>
                <p>여기를 클릭하여 사진 업로드</p>
            </div>

            <input
                type="file"
                accept="image/*"
                ref={fileInputRef}
                style={{ display: 'none' }}
                onChange={handleFileChange}
            />

            <button
                className="btn-primary"
                onClick={() => fileInputRef.current.click()}
            >
                사진 촬영 / 업로드
            </button>
        </div>
    );
};

export default LandingPage;
