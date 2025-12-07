import React, { useRef, useState } from 'react';

const LandingPage = ({ onUpload, t }) => {
    const fileInputRef = useRef(null);
    const videoRef = useRef(null);
    const canvasRef = useRef(null);
    const [isCameraOpen, setIsCameraOpen] = useState(false);

    const handleFileChange = (e) => {
        const file = e.target.files[0];
        if (file) {
            onUpload(file);
        }
    };

    const startCamera = async () => {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ video: true });
            setIsCameraOpen(true);
            // Wait for modal to render
            setTimeout(() => {
                if (videoRef.current) {
                    videoRef.current.srcObject = stream;
                }
            }, 100);
        } catch (err) {
            console.error("Error accessing camera:", err);
            alert("Camera access denied.");
        }
    };

    const stopCamera = () => {
        if (videoRef.current && videoRef.current.srcObject) {
            const tracks = videoRef.current.srcObject.getTracks();
            tracks.forEach(track => track.stop());
            videoRef.current.srcObject = null;
        }
        setIsCameraOpen(false);
    };

    const captureImage = () => {
        if (videoRef.current && canvasRef.current) {
            const video = videoRef.current;
            const canvas = canvasRef.current;

            // Set canvas size to match video
            canvas.width = video.videoWidth;
            canvas.height = video.videoHeight;

            // Draw video frame to canvas
            const context = canvas.getContext('2d');
            context.drawImage(video, 0, 0, canvas.width, canvas.height);

            // Convert to file
            canvas.toBlob((blob) => {
                const file = new File([blob], "camera_capture.jpg", { type: "image/jpeg" });
                onUpload(file);
                stopCamera();
            }, 'image/jpeg');
        }
    };

    return (
        <div className="glass-panel animate-fade-in" style={{ textAlign: 'center', padding: '3rem 2rem' }}>
            <h1 style={{ fontSize: '2.5rem', marginBottom: '1rem', color: 'var(--primary-color)' }}>
                {t.app_title}
            </h1>
            <p style={{ marginBottom: '2rem', color: 'var(--text-secondary)', lineHeight: '1.6' }}>
                {t.upload_title}<br />{t.upload_desc}
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
                <p>{t.upload_btn}</p>
            </div>

            <input
                type="file"
                accept="image/*"
                ref={fileInputRef}
                style={{ display: 'none' }}
                onChange={handleFileChange}
            />

            <div style={{ display: 'flex', gap: '1rem', justifyContent: 'center' }}>
                <button
                    className="btn-primary"
                    onClick={() => fileInputRef.current.click()}
                >
                    {t.upload_btn}
                </button>
                <button
                    className="btn-secondary"
                    onClick={startCamera}
                >
                    {t.camera_btn}
                </button>
            </div>

            {/* Camera Modal */}
            {isCameraOpen && (
                <div className="camera-modal-overlay">
                    <div className="camera-modal-content">
                        <button className="btn-close" onClick={stopCamera}>&times;</button>
                        <video ref={videoRef} autoPlay playsInline className="camera-video"></video>
                        <canvas ref={canvasRef} style={{ display: 'none' }}></canvas>
                        <div className="camera-controls">
                            <button className="btn-capture" onClick={captureImage}></button>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
};

export default LandingPage;
