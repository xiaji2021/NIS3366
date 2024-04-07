import React, { useState } from 'react';
import axios from 'axios'; // 使用axios库简化HTTP请求

function ImgUpload(){
    const [uploadImage,setUploadImage] = useState(null);

    const handleImageChange = (e) =>{

        setUploadImage(e.target.files[0])
    }
    const handleUpload = async () => {
        if(uploadImage) {
            const formData = new FormData();

            formData.append('uploadImage', uploadImage,uploadImage.name);

            try {
                const response = await axios.post('/upload-image',formData,{
                    headers: {
                        'Content-Type': 'multipart/form-data'
                    }
                })
                //暂时回应这个
                console.log(response.data)
            } catch (error) {
                console.error(error);
            }

        }
    }
}