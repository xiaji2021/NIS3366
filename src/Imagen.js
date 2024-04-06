import React, { useState } from 'react';
import axios from 'axios';

function ImageGenerator() {
    const [isLoading, setIsLoading] = useState(false);
    const [prompt, setPrompt] = useState('');
    const [imageUrl, setImageUrl] = useState('');

    const handleGenerateImage = async () => {
        try {
            setIsLoading(true);
            const response = await axios.post('http://localhost:5000/generate-image', { prompt });
            setImageUrl(response.data.image_path); // 返回image_path字段
            setIsLoading(false);
        } catch (error) {
            console.error('Error generating image:', error);

            setIsLoading(false);
        }
    };
    const inputStyle = {
        width: '80%',
        marginBottom: '10px',
        borderRadius: '4px',
        padding: '10px',
        border: 'none',
        backgroundColor: '#333',
        color: 'white',
    };

    const buttonStyle = {
        borderRadius: '4px',
        padding: '10px 20px',
        border: 'none',
        backgroundColor: '#4CAF50',
        color: 'white',
        fontSize: '16px',
        cursor: 'pointer',
        marginTop: '10px',
    };

    return (
        <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '100vh' }}>
            <div style={{ backgroundColor: '#1E1E1E', padding: '20px', borderRadius: '8px', marginRight: '20px',height: '70vh', width: '70vh' }}>
                <h2 style={{ color: '#FFFFFF' }}>Enter Parameters</h2>
                <input
                    type="text"
                    value={prompt}
                    onChange={(e) => setPrompt(e.target.value)}
                    placeholder="Enter a prompt"
                    style={inputStyle}
                />
                <button onClick={handleGenerateImage} style={buttonStyle}>Generate Image</button>
            </div>
            <div style={{ backgroundColor: '#1E1E1E', padding: '20px', borderRadius: '8px', height: '70vh',  width: '70vh',   justifyContent: 'center', alignItems: 'center' }}>
                <h2 style={{ color: '#FFFFFF' }}>Generated Image</h2>
                {imageUrl ? <img src={imageUrl} alt="Generated Visual"
                                 style={{
                                     maxHeight: 'calc(70vh - 40px - 40px)', // 70vh (容器高) 减去 padding-top 和 padding-bottom 和标题区域
                                     maxWidth: 'calc(70vh - 40px)', // 70vh (容器宽) 减去 padding-left 和 padding-right
                                     objectFit: 'contain',
                                     borderRadius: '8px' }} /> : <div
                    style={{
                        width: '70vh',
                        height: '55vh',
                        borderRadius: '8px',
                        backgroundColor: '#333',
                        display: 'flex',
                        justifyContent: 'center',
                        alignItems: 'center',
                        color: '#fff'
                            }}>No image generated</div>}
            </div>
        </div>
    );
}

export default ImageGenerator;
