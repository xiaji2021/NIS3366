import React, { useState } from 'react';
import './WaterMark.css';
const WaterMark = () => {

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
  return (
    <div className='container'>
      <div className='left'>
        <h1 className="title3">水印生成</h1>
        <div
          className="image-container"
          onDrop={handleDrop}
          onDragOver={(e) => e.preventDefault()}
        >
        {image ? (
          <img src={image} alt="Uploaded" className="image" />
        ) : (
          <p className="upload-text">将图片拖拽放入此处&点击此处选择图片文件</p>
        )}
        </div>
        <form className="form" onSubmit={handleSubmit}>
        <input type="file" onChange={handleImageUpload} accept="image/*" />
        <br />
        <input type="text" placeholder="Enter watermark text" className="text-input" />
        <br />
        <button type="submit" className="generate-button">Generate</button>
      </form>
      </div>
    </div>
      
  );
};

export default WaterMark;
