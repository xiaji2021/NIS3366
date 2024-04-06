import React from 'react';
import { Link } from 'react-router-dom';

const NavigationBar = () => {
  return (
    <nav>
      <ul>
        <li><Link to="/">Home</Link></li>
        <li><Link to="/text-image">文生图</Link></li>
        <li><Link to="/watermark-generation">生成水印</Link></li>
        <li><Link to="/watermark-detection">水印检测</Link></li>
        <li><Link to="/entity-extraction">实体抽取</Link></li>
        <li><Link to="/user">用户</Link></li>
      </ul>
    </nav>
  );
};

export default NavigationBar;