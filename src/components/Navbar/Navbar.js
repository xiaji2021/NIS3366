import React from 'react';
import { NavLink } from 'react-router-dom';
import './Navbar.css';

function Navbar() {
    return (
        <nav className="navbar">
            <NavLink to="/text-to-image" activeClassName="active">文生图</NavLink>
            <NavLink to="/image-to-image" activeClassName="active">图生图</NavLink>
        </nav>
    );
}

export default Navbar;
