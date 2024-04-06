import React from 'react';
import { NavLink } from 'react-router-dom';
import './Navbar.css';
import logo from './logo.png'
function Navbar() {
    return (
        <nav className="navbar">
            <div className="nav-container">
                <ul className="nav-logo">
                    <img src={logo} alt="logo"/>
                </ul>
                <ul className='welcome'>╭(●｀∀´●)╯AI图片工具╰(●’◡’●)╮</ul>
                <ul className="nav-menu">
                    <li className="nav-item">
                        <NavLink exact to="/" activeClassName="active" className="nav-links">
                            文生图
                        </NavLink>
                    </li>
                    <li className="nav-item">
                        <NavLink to="/about" activeClassName="active" className="nav-links">
                            水印检测
                        </NavLink>
                    </li>
                    <li className="nav-item">
                        <NavLink to="/services" activeClassName="active" className="nav-links">
                            水印生成
                        </NavLink>
                    </li>
                    <li className="nav-item">
                        <NavLink to="/contact" activeClassName="active" className="nav-links">
                            实体抽取
                        </NavLink>
                    </li>
                </ul>
            </div>
        </nav>
);
}

export default Navbar;
