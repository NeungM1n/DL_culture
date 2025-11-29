import React from 'react';

const ResultPage = ({ result, image, onReset, onChat }) => {
    return (
        <div className="glass-panel animate-fade-in">
            <div style={{ position: 'relative', marginBottom: '1.5rem' }}>
                <img
                    src={image}
                    alt="Uploaded"
                    style={{
                        width: '100%',
                        borderRadius: '12px',
                        maxHeight: '300px',
                        objectFit: 'cover',
                        boxShadow: '0 4px 12px rgba(0,0,0,0.3)'
                    }}
                />
                <div style={{
                    position: 'absolute',
                    bottom: '10px',
                    right: '10px',
                    background: 'rgba(0,0,0,0.7)',
                    padding: '4px 8px',
                    borderRadius: '6px',
                    fontSize: '0.9rem',
                    color: 'var(--primary-color)',
                    fontWeight: 'bold'
                }}>
                    일치율 {result.matchPercentage}%
                </div>
            </div>

            <h2 style={{ fontSize: '1.8rem', marginBottom: '0.5rem', color: 'var(--primary-color)' }}>
                {result.name}
            </h2>

            <p style={{ marginBottom: '1.5rem', lineHeight: '1.6', color: '#eee' }}>
                {result.description}
            </p>

            <div style={{ display: 'flex', gap: '10px', marginBottom: '1.5rem' }}>
                <button className="btn-primary" style={{ flex: 1 }} onClick={onChat}>
                    AI와 대화하기 💬
                </button>
                <button className="btn-secondary" onClick={onReset}>
                    다시 하기
                </button>
            </div>

            {result.alternatives && result.alternatives.length > 0 && (
                <div style={{ borderTop: '1px solid var(--glass-border)', paddingTop: '1rem' }}>
                    <p style={{ fontSize: '0.9rem', color: 'var(--text-secondary)', marginBottom: '0.5rem' }}>
                        이 결과가 아닌가요? 다른 후보:
                    </p>
                    <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px' }}>
                        {result.alternatives.map((alt, index) => (
                            <span
                                key={index}
                                style={{
                                    background: 'rgba(255,255,255,0.1)',
                                    padding: '6px 12px',
                                    borderRadius: '20px',
                                    fontSize: '0.85rem',
                                    cursor: 'pointer'
                                }}
                                onClick={() => alert('이 기능은 아직 구현되지 않았습니다. (대안 선택)')}
                            >
                                {alt}
                            </span>
                        ))}
                    </div>
                </div>
            )}
        </div>
    );
};

export default ResultPage;
