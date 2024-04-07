import React, { useState } from 'react';
import './Entity.css';
import axios from "axios";

const Entity = () => {
    // 用于保存上传图片的状态
    const [text, setText] = useState('');
    const [image, setImage] = useState(null);
    const [watermarkImage, setWatermarkImage] = useState(null);
    //这里得到的是一个链接


    // 处理图片上传的函数
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
    // const handleText = (e) => {
    //     setText(e.target.value);
    // }


    // 处理拖放上传的函数
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

    // 处理表单提交的函数
    const handleSubmit = async (e)=> {
        e.preventDefault();
        if (!image || !text) {
            alert('Please upload an image and enter watermark text.');
            return;
        }
        const formData = new FormData();
        formData.append('image', dataURLtoBlob(image));
        formData.append('text', text);
        try {
            const response =  await axios.post('/entity-gen',formData,{
                headers: {
                    'Content-Type': 'multipart/form-data'
                }
            })
            setWatermarkImage(response.data.image_path);
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

    return (
        <div className='container'>
            <div className='left'>
                <h1 className="title3">实体抽取</h1>
                <div className="image-container"
                     onDrop={handleDrop}
                     onDragOver={(e) => e.preventDefault()}
                >
                    {image ? (
                        <img src={image} alt="Uploaded" className="image"/>
                    ) : (
                        <p className="upload-text">将图片拖拽放入此处&点击此处选择图片文件</p>
                    )}
                </div>
                <form className="form" onSubmit={handleSubmit}>
                    <input type="file" onChange={handleImageUpload} accept="image/*"/>

                    <br/>
                    <button type="submit" className="generate-button">运行</button>
                </form>
            </div>


            <div className='right'>
                <h1 className="title3">实体抽取结果</h1>
                <div className="image-container"
                     onDrop={handleDrop}
                     onDragOver={(e) => e.preventDefault()}
                >
                    {watermarkImage ? (
                        <img src={watermarkImage} alt="Uploaded" className="image"/>
                    ) : (
                        <p className="upload-text">结果显示</p>
                    )}
                </div>

            </div>
        </div>
    );
};

export default Entity;
