import React, { useState } from 'react';
import './WaterMark.css';
const ImageUploader = () => {
  // State for the uploaded image
  const [image, setImage] = useState(null);
  // Function to handle file upload
  const handleImageUpload = (e) => {
    const file = e.target.files[0];
    const reader = new FileReader();
    reader.onload = () => {
      if (reader.readyState === 2) {
        setImage(reader.result);
      }
    };
    reader.readAsDataURL(file);
  };
  // Function to handle drag and drop
  // eslint-disable-next-line
  const handleDrop = (e) => {
    e.preventDefault();
    const file = e.dataTransfer.files[0];
    const reader = new FileReader();

    reader.onload = () => {
      if (reader.readyState === 2) {
        setImage(reader.result);
      }
    };
    reader.readAsDataURL(file);
  };
  // Function to handle form submission
  const handleSubmit = (e) => {
    e.preventDefault();
    // Implement watermark generation logic here
    console.log('Generating watermark...');
  };






  const [image1, setImage1] = useState(null);
  const [method1, setMethod1] = useState('');
  const [result1, setResult1] = useState('');
  const [selectedAttack, setSelectedAttack] = useState('');
  const [backendText, setBackendText] = useState('');

  const handleDrop1 = (e) => {
    e.preventDefault();
    const file = e.dataTransfer.files[0];
    const reader = new FileReader();
    reader.onload = () => {
      setImage1(reader.result);
    };
    reader.readAsDataURL(file);
  };

  const handleMethodChange1 = (selectedMethod) => {
    setMethod1(selectedMethod);
    setSelectedAttack(`已选择方式: ${selectedMethod}`); // 更新选择的攻击方式
    setResult1(''); // 清空之前的结果
  };

  const handleDetect1 = async () => {
    // 这里可以根据选择的方法和图片进行处理
    setResult1(`Detecting with ${method1} method...`);
    
    // 模拟向后端发送请求并获取文本结果
    const response = await fetch('your-backend-endpoint');
    const data = await response.text();
    setBackendText(data);
  };

  const handleDragOver1 = (e) => {
    e.preventDefault();
  };











  return (
    <div className='container'>
      <div className='left'>
        <h1 className="title3">水印生成/Watermark Generation</h1>
        <div
          className="image-container"
          onDrop={handleDrop}
          onDragOver={(e) => e.preventDefault()}
        >
        {image ? (
          <img src={image} alt="Uploaded" className="image" />
        ) : (
          <p className="upload-text">将图片拖拽放入此处&点击下方选择图片文件</p>
        )}
        </div>
        <form className="form" onSubmit={handleSubmit}>
        <label className="custom-file-upload">
          点击此处上传图片
          <input type="file" onChange={handleImageUpload} accept="image/*" />
        </label> 
        <div className='line4'>
          水印输入：
          <input type="text" placeholder="在此输入文字" className="text-input" />
        </div>
        <br />
        <button type="submit" className="generate-button">生成水印</button>
      </form>
      </div>







      <div className='right'>
        <div className="App">
          <h1 className='title3'>水印检测/Watermark Detection</h1>
          <div
            className="drop-zone"
            onDrop={handleDrop1}
            onDragOver={handleDragOver1}
          >
          {image1 ? (
            <img src={image1} alt="Dropped" className="dropped-image" />
          ) : (
            <p className="upload-text">将图片拖拽放入此处&自动放置左侧的生成图片</p>
          )}
          </div>
          <div className="method-buttons">
            <button onClick={() => handleMethodChange1('Method 1')} className='attack'>
              方式1
            </button>
            <button onClick={() => handleMethodChange1('Method 2')} className='attack'>
              方式2
            </button>
            <button onClick={() => handleMethodChange1('Method 3')} className='attack'>
              方式3
            </button>
            <button onClick={() => handleMethodChange1('Method 4')} className='attack'>
              方式4
            </button>
          </div>
          <div className="selected-method">{selectedAttack}</div> {/* 显示选择的攻击方式 */}
          <button onClick={handleDetect1} className="detect-button">
            检测水印
          </button>
      <div className="result">{result1}</div>
      <div>{backendText}</div> {/* 显示后端载入的文本结果 */}
    </div>
    </div>
    </div>
  );
};

export default ImageUploader;
