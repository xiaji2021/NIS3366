import React from 'react';
import { NavLink } from 'react-router-dom';
import './Navbar.css';

function Navbar() {
  return (
      <nav className="navbar">
          <div className="nav-container">
              <NavLink exact to="/" className="nav-logo">
                  LOGO
              </NavLink>
              <ul className="nav-menu">
                  <li className="nav-item">
                      <NavLink exact to="/" activeClassName="active" className="nav-links">
                          主页
                      </NavLink>
                  </li>
                  <li className="nav-item">
                      <NavLink to="/about" activeClassName="active" className="nav-links">
                          关于我们
                      </NavLink>
                  </li>
                  <li className="nav-item">
                      <NavLink to="/services" activeClassName="active" className="nav-links">
                          服务
                      </NavLink>
                  </li>
                  <li className="nav-item">
                      <NavLink to="/contact" activeClassName="active" className="nav-links">
                          联系我们
                      </NavLink>
                  </li>
              </ul>
          </div>
      </nav>


  );
}

export default Navbar;
