import React from 'react';
import { NavLink } from 'react-router-dom';
import './Navbar.css';

function Navbar() {
  return (
    <div className="navcontainer">
      <nav className="navbox">
        <li className="nav-items" id="moren" >用户</li>
        <li className="nav-items" >文生图</li>
        <li className="nav-items">水印生成</li>
        <li className="nav-items">水印检测</li>
        <li className="nav-items">实体抽取</li>
        <img src="列表.png" title="更多" />
      </nav>
    </div>
  );
}
export default Navbar;
