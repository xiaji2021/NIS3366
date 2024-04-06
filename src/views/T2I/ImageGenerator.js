import React, { useState } from 'react';
import './ImageGenerator.css'
import image0 from './1.png'
import axios from 'axios';
function App() {
    const [text, setText] = useState('');//输入文本
    const [style, setStyle] = useState('default');//风格选择
    const [seed, setSeed] = useState('');//输入种子
    const [generatedImage, setGeneratedImage] = useState(null);//存储生成图片
    const [imageCount, setImageCount] = useState(1); // 新增图片数量
    const [imageSize, setImageSize] = useState('medium'); // 新增图片尺寸
    const [imageUrl, setImageUrl] = useState('');
    const [isLoading, setIsLoading] = useState(false);

    const handleGenerateClick = async () => {
        try {
            setIsLoading(true);
            const response = await axios.post('http://<ip>:<port>/generate-image', {text});
            setImageUrl(response.data.image_path); //后端需要返回image_path
            setIsLoading(false);
        }
        catch (error)  {
            console.error('Error generating image:', error);
            setIsLoading(false);
        }
        };

  return (
    <div style={{ display: 'flex', justifyContent: 'center', height: '100vh' }}>
      <div style={{
        display:'flex',
        width: '100%',
        height: 'auto',
        justifyContent: 'space-between',
        padding:'2%',
        background: 'linear-gradient(to bottom left, rgb(255, 238, 255), rgb(221, 255, 238))'
      }}>
        <div style={{width:'30%', marginRight: '20px' }}>
          <h1 className='title'>文字转图片/Text to Image</h1>
          <h2 className='line2'>创意描述</h2>
          <textarea
            value={text}
            onChange={(e) => setText(e.target.value)}
            placeholder="在此输入内容，自动生成图片"
            style={{
              width: '90%',
              height: '130px',
              backgroundColor: 'rgb(255, 255, 255)',
              fontSize: '20px',
              borderRadius:'10px',
              marginTop:'10px',
              padding:'15px',
              display:'block',
              marginBottom:'20px',
            }}
          />
          <div className='line1'>风格选择</div>
          <select 
            value={style} 
            onChange={(e) => setStyle(e.target.value)} 
            style={{
              width: '30%',
              marginTop: '0px',
              fontSize: '20px',
              padding:'8px',
              backgroundColor:'rgb(255,255,255)',
              borderRadius:'7px',
              marginLeft:'20px',
              fontSize:'16px',
            }}
          >
            <option value="default">默认风格</option>
            <option value="style2">风格1</option>
            <option value="style3">风格2</option>
            <option value="style4">风格3</option>
            <option value="style5">风格4</option>
            <option value="style6">风格5</option>
            <option value="style7">风格6</option>
            <option value="style7">风格7</option>
            <option value="style7">风格8</option>
            <option value="style7">风格9</option>
            <option value="style7">风格10</option>
            <option value="style7">风格11</option>
          </select>
          <div className="grid-container">
            <div className="grid-item"><img src={image0} alt="style0"/><h3 className='style'>默认风格</h3></div>
            <div className="grid-item"><img src={image0}  alt="style1" /><h3 className='style'>风格1</h3></div>
            <div className="grid-item"><img src={image0} alt="style2" /><h3 className='style'>风格2</h3></div>
            <div className="grid-item"><img src={image0} alt="style3" /><h3 className='style'>风格3</h3></div>
            <div className="grid-item"><img src={image0}  alt="style4"/><h3 className='style'>风格4</h3></div>
            <div className="grid-item"><img src={image0}  alt="style5" /><h3 className='style'>风格5</h3></div>
            <div className="grid-item"><img src={image0}  alt="style6"/><h3 className='style'>风格6</h3></div>
            <div className="grid-item"><img src={image0} alt="style7"/><h3 className='style'>风格7</h3></div>
            <div className="grid-item"><img src={image0}  alt="style8"/><h3 className='style'>风格8</h3></div>
            <div className="grid-item"><img src={image0}  alt="style9"/><h3 className='style'>风格9</h3></div>
            <div className="grid-item"><img src={image0} alt="style10" /><h3 className='style'>风格10</h3></div>
            <div className="grid-item"><img src={image0}  alt="style11"/><h3 className='style'>风格11</h3></div>
          </div>
          <h2 className='line2'>其他设置</h2>
          <div className='style1'>种子设置</div>
          <input
            type="text"
            value={seed}
            onChange={(e) => setSeed(e.target.value)}
            placeholder="输入一串数字"
            style={{
              marginLeft:'20px',
              width: '100%',
              marginTop: '0px',
              fontSize: '16px',
              width: '50%',
              padding:'10px',
              borderRadius:'7px',
            }}
          />
          <div style={{ marginTop: '15px' }}>
            <label htmlFor="imageCount" className='style1'>图片数量</label>
            <input
              id="imageCount"
              type="number"
              value={imageCount}
              onChange={(e) => setImageCount(parseInt(e.target.value))}
              min="1"
              max="10"
              style={{
                marginLeft:'20px',
                fontSize: '16px',
                padding:'8px',
                borderRadius:'7px',
              }}
            />
          </div>
          <div style={{ marginTop: '15px' }}>
            <label htmlFor="imageSize" className='style1'>图片尺寸</label>
            <select
              id="imageSize"
              value={imageSize}
              onChange={(e) => setImageSize(e.target.value)}
              style={{
                marginLeft:'20px',
                fontSize: '16px',
                padding:'8px',
                borderRadius:'7px',
              }}
            >
              <option value="small">小</option>
              <option value="medium">中</option>
              <option value="large">大</option>
            </select>
          </div>
          <button 
            onClick={handleGenerateClick} 
            style={{
              placeItems:'center',
              width: '50%', 
              marginTop: '20px', 
              background: 'linear-gradient(to bottom right, rgb(204, 238, 85), rgb(255, 187, 255))',
              fontSize:'24px',
              fontFamily:'font1',
              borderRadius:'10px',
              padding:'5px',
            }}>
            生成图片
          </button>
        </div>
        <div style={{ flex: 1, border: '1px solid #ccc', padding: '20px' }}>
          {generatedImage && <img src={generatedImage} alt="Generated" style={{ maxWidth: '100%', maxHeight: '400px' }} />}
          <div>
            <h1 style={{ textAlign: 'center' }}>左侧输入内容，开启绘图之旅</h1>
              {/* <div className="image-grid">
                {images.map((image, index) => (
                  <img key={index} src={image.url} alt={`Image ${index}`} />
                ))}
              </div> */}
          </div>
        </div>
      </div>n
    </div>
  );
}
export default App;
