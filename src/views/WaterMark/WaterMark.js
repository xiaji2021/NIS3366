
import React, { useState } from 'react';
import './WaterMark.css';
import axios from "axios";

const ImageUploader = () => {
  // State for the uploaded image
  const [image, setImage] = useState(null);
  const [text, setText] = useState('');
  
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

  const handleSubmit = async (e)=> {
    e.preventDefault();
    if (!image || !text) {
        alert('Please upload an image.');
        return;
    }
    const formData = new FormData();
    formData.append('image', dataURLtoBlob(image)); 
    formData.append('text', text)

    try {
        const response =  await axios.post('http://47.103.101.128:8888/watermark-gen',formData,{
            headers: {
                'Content-Type': 'multipart/form-data'
            }
        })
        setImage1(response.data.image_path);
        console.log('test')
    } catch (error) {
        console.error(error);
    }


    console.log('Generating watermark...');
    };


  function dataURLtoBlob(dataurl) {
    const arr = dataurl.split(',');
    const mime = arr[0].match(/:(.*?);/)[1];
    const bstr = atob(arr[1]);
    let n = bstr.length;
    const u8arr = new Uint8Array(n);
    while (n--) {
        u8arr[n] = bstr.charCodeAt(n);
    }
    return new Blob([u8arr], { type: mime });
    }






  const [Image1, setImage1] = useState(null);
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
  // const handleSubmit = async (e)=> {
  //   e.preventDefault();
  //   if (!image || !text) {
  //       alert('Please upload an image.');
  //       return;
  //   }
  //   const formData = new FormData();
  //   formData.append('image', dataURLtoBlob(image));
  //   formData.append('text', text)
  
  //   try {
  //       const response =  await axios.post('http://47.103.101.128:8888/watermark-gen',formData,{
  //           headers: {
  //               'Content-Type': 'multipart/form-data'
  //           }
  //       })
  //       setWatermarkImage(response.data.image_path);
  //       console.log('test')
  //   } catch (error) {
  //       console.error(error);
  //   }
  
  const handleDetect1 = async (e) => {
    e.preventDefault();
    
    if(!Image1){
      alert('Please upload an image.')
    }
    
    setResult1(`Detecting with ${method1} method...`);
    const formData = new FormData();
    if (Image1.startsWith('data:')) {
      // 如果是dataURL，转换为Blob对象
      const blob = dataURLtoBlob(Image1);
      formData.append('image', blob);
    } else {
      // 如果是远程链接，需要获取远程图片并转换为Blob
      const response = await fetch(Image1);
      const blob = await response.blob();
      formData.append('image', blob);
    }
    formData.append('method', method1);
    
    
    // 模拟向后端发送请求并获取文本结果
        try {
        const response =  await axios.post('http://47.103.101.128:8888/watermark-attack',formData,{
            headers: {
                'Content-Type': 'multipart/form-data'
            }
        })
        setImage1(response.data.image_path);
        setBackendText(response.data.text_detected);// 注意后端返回的键值
        
    } catch (error) {
        console.error(error);
    }
    
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
          <input type="text" onChange={(e) => setText(e.target.value)} placeholder="在此输入文字" className="text-input" />
        </div>
        <br />
        <button type="submit" className="generate-button1">生成水印</button>
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
          {Image1 ? (
            <img src={Image1} alt="Dropped" className="dropped-image" />
          ) : (
            <p className="upload-text">将图片拖拽放入此处&自动放置左侧的生成图片</p>
          )}
          </div>
          <div class="watermark-info">
    <label for="watermark-text">水印信息为：</label>
    <input type="text" id="watermark-text" value={backendText} readonly />
      </div>
          <div className="method-buttons">
            <button onClick={() => handleMethodChange1('bright')} className='attack'>
              bright
            </button>
            <button onClick={() => handleMethodChange1('shelter')} className='attack'>
            shelter
            </button>
            <button onClick={() => handleMethodChange1('salt')} className='attack'>
            salt
            </button>
            <button onClick={() => handleMethodChange1('rot')} className='attack'>
              rotation
            </button>

          </div>

          <div className="selected-method">{selectedAttack}</div> {/* 显示选择的攻击方式 */}
          <button type="submit" onClick={handleDetect1}  className="detect-button">
            检测水印
          </button>

      <div className="result">{result1}</div>
      
    </div>
    </div>
    </div>
  );
};

export default ImageUploader;
