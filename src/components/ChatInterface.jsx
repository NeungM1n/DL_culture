import React, { useState, useRef, useEffect } from 'react';
import { chatWithAI } from '../services/aiService';

const ChatInterface = ({ context, onBack, language, t }) => {
    const [messages, setMessages] = useState([
        { role: 'assistant', content: t.chat_greeting.replace('{name}', context.name) }
    ]);
    const [input, setInput] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const messagesEndRef = useRef(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    const handleSend = async () => {
        if (!input.trim()) return;

        const userMessage = { role: 'user', content: input };
        setMessages(prev => [...prev, userMessage]);
        setInput('');
        setIsLoading(true);

        try {
            // Pass language to AI service
            const responseContent = await chatWithAI(input, context, messages, language);
            const aiResponse = {
                role: 'assistant',
                content: responseContent
            };
            setMessages(prev => [...prev, aiResponse]);
        } catch (error) {
            console.error(error);
            setMessages(prev => [...prev, { role: 'assistant', content: t.chat_error }]);
        } finally {
            setIsLoading(false);
        }
    };

    const handleKeyPress = (e) => {
        if (e.key === 'Enter') {
            handleSend();
        }
    };

    return (
        <div className="glass-panel animate-fade-in" style={{ height: '600px', display: 'flex', flexDirection: 'column', padding: '0' }}>
            <div style={{
                padding: '1rem',
                borderBottom: '1px solid var(--glass-border)',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'space-between'
            }}>
                <button className="btn-secondary" onClick={onBack} style={{ padding: '5px 10px', fontSize: '0.8rem' }}>
                    ← {t.chat_back}
                </button>
                <span style={{ fontWeight: 'bold', color: 'var(--primary-color)' }}>{t.chat_title}</span>
                <div style={{ width: '40px' }}></div> {/* Spacer */}
            </div>

            <div style={{ flex: 1, overflowY: 'auto', padding: '1rem', display: 'flex', flexDirection: 'column', gap: '1rem' }}>
                {messages.map((msg, index) => (
                    <div
                        key={index}
                        style={{
                            alignSelf: msg.role === 'user' ? 'flex-end' : 'flex-start',
                            maxWidth: '80%',
                            background: msg.role === 'user' ? 'var(--primary-color)' : 'rgba(255,255,255,0.1)',
                            color: msg.role === 'user' ? '#000' : '#fff',
                            padding: '10px 15px',
                            borderRadius: '12px',
                            borderBottomRightRadius: msg.role === 'user' ? '2px' : '12px',
                            borderBottomLeftRadius: msg.role === 'assistant' ? '2px' : '12px',
                        }}
                    >
                        {msg.content}
                    </div>
                ))}
                {isLoading && (
                    <div style={{ alignSelf: 'flex-start', color: '#aaa', fontSize: '0.9rem' }}>
                        {t.chat_loading}
                    </div>
                )}
                <div ref={messagesEndRef} />
            </div>

            <div style={{ padding: '1rem', borderTop: '1px solid var(--glass-border)', display: 'flex', gap: '10px' }}>
                <input
                    type="text"
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    onKeyPress={handleKeyPress}
                    placeholder={t.chat_placeholder}
                    style={{
                        flex: 1,
                        padding: '12px',
                        borderRadius: '8px',
                        border: '1px solid var(--glass-border)',
                        background: 'rgba(0,0,0,0.3)',
                        color: '#fff',
                        outline: 'none'
                    }}
                />
                <button className="btn-primary" onClick={handleSend} disabled={isLoading}>
                    {t.chat_send}
                </button>
            </div>
        </div>
    );
};

export default ChatInterface;
