import React from 'react';

const ResultPage = ({ result, image, onReset, onChat, onSelectAlternative, language, t }) => {
    // Local language state removed, using global prop 'language'

    const getLocalizedContent = (dataObj) => {
        // Handle both old schema (string/object-desc only) and new schema (object with name/desc)
        if (typeof dataObj === 'object' && dataObj !== null) {
            const content = dataObj[language] || dataObj['ko'];
            if (content) {
                if (typeof content === 'object') {
                    // New Schema: { name: "...", description: "..." }
                    return content;
                } else {
                    // Old Schema: { ko: "desc string" } -> Name is missing, use default key from result
                    return { name: result.name, description: content };
                }
            }
        }
        // Fallback or string
        return { name: result.name, description: typeof dataObj === 'string' ? dataObj : t.no_description };
    };

    const currentContent = getLocalizedContent(result.description);

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
                    {t.result_match} {result.matchPercentage}%
                </div>
            </div>

            <h2 style={{ fontSize: '1.8rem', marginBottom: '0.5rem', color: 'var(--primary-color)' }}>
                {currentContent.name}
            </h2>

            {/* Language buttons removed here as they are now global in App.jsx */}

            <p style={{ marginBottom: '1.5rem', lineHeight: '1.6', color: '#eee' }}>
                {currentContent.description}
            </p>

            <div style={{ display: 'flex', gap: '10px', marginBottom: '1.5rem' }}>
                <button className="btn-primary" style={{ flex: 1 }} onClick={onChat}>
                    {t.result_chat_btn}
                </button>
                <button className="btn-secondary" onClick={onReset}>
                    {t.result_reset_btn}
                </button>
            </div>

            {result.alternatives && result.alternatives.length > 0 && (
                <div style={{ borderTop: '1px solid var(--glass-border)', paddingTop: '1rem' }}>
                    <p style={{ fontSize: '0.9rem', color: 'var(--text-secondary)', marginBottom: '0.5rem' }}>
                        {t.result_alt_title}
                    </p>
                    <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px' }}>
                        {result.alternatives.map((alt, index) => {
                            const altContent = getLocalizedContent(alt.description);
                            // Fallback if description is missing locally but name is classification result(Korean)
                            const displayName = altContent.name || alt.name;

                            return (
                                <span
                                    key={index}
                                    style={{
                                        background: 'rgba(255,255,255,0.1)',
                                        padding: '6px 12px',
                                        borderRadius: '20px',
                                        fontSize: '0.85rem',
                                        cursor: 'pointer',
                                        display: 'flex',
                                        alignItems: 'center',
                                        gap: '6px'
                                    }}
                                    onClick={() => onSelectAlternative && onSelectAlternative(alt)}
                                >
                                    <span>{displayName}</span>
                                    <span style={{ opacity: 0.7, fontSize: '0.75rem' }}>{alt.confidence}%</span>
                                </span>
                            );
                        })}
                    </div>
                </div>
            )}
        </div>
    );
};

export default ResultPage;
