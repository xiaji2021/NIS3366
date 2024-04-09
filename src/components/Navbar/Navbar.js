import React, {useContext} from 'react';
import { NavLink } from 'react-router-dom';
import './Navbar.css';
import logo from './logo.png'
import AuthContext from "../../AuthContext"

function Navbar() {
    const {user,logout} = useContext(AuthContext);
    const handleLogout = () => {
        logout();
    }
    return (
        <nav className="navbar navbar-expand-lg navbar-light bg-light ">
            <div className="container-fluid">
                <NavLink className="navbar-brand nav-links" to="/">
                    <img src={logo} alt="logo" height="30" className="d-inline-block align-top "/> AI图片工具
                </NavLink>
                <button className="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNavDropdown"
                        aria-controls="navbarNavDropdown" aria-expanded="false" aria-label="Toggle navigation">
                    <span className="navbar-toggler-icon"></span>
                </button>
                <div className="collapse navbar-collapse" id="navbarNavDropdown">
                    <ul className="navbar-nav ms-auto">
                        <li className="nav-item nav-links">
                            <NavLink exact to="/" className="nav-link" activeClassName="active">
                                文生图
                            </NavLink>
                        </li>
                        <li className="nav-item nav-links">
                            <NavLink to="/watermark" className="nav-link" activeClassName="active">
                                水印检测与生成
                            </NavLink>
                        </li>
                        <li className="nav-item nav-links">
                            <NavLink to="/entity" className="nav-link" activeClassName="active">
                                实体检测
                            </NavLink>
                        </li>
                        <li className="nav-item dropdown nav-links">
                            <a className="nav-link dropdown-toggle" href="#" id="navbarDropdownMenuLink" role="button"
                               data-bs-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                                账户
                            </a>
                            <div className="dropdown-menu" aria-labelledby="navbarDropdownMenuLink">
                                {user ? (
                                    <>
                                        <span className="dropdown-item-text">{user.username},你好！</span>
                                        <button onClick={handleLogout} className="dropdown-item">
                                            登出
                                        </button>
                                    </>
                                ) : (
                                    <>
                                        <NavLink to="/login" className="dropdown-item" activeClassName="active">
                                            登录
                                        </NavLink>
                                        <NavLink to="/register" className="dropdown-item" activeClassName="active">
                                            注册
                                        </NavLink>
                                    </>
                                )}
                            </div>
                        </li>
                    </ul>
                </div>
            </div>
        </nav>




        //     <nav className="navbar">
        //         <div className="nav-container">
        //             <ul className="nav-logo">
        //                 <img src={logo} alt="logo"/>
        //             </ul>
        //             <ul className='welcome'>╭(●｀∀´●)╯AI图片工具╰(●’◡’●)╮</ul>
        //             <ul className="nav-menu">
        //                 <li className="nav-item">
        //                     <NavLink exact to="/" activeClassName="active" className="nav-links">
        //                         文生图
        //                     </NavLink>
        //                 </li>
        //                 <li className="nav-item">
        //                     <NavLink to="/watermark" activeClassName="active" className="nav-links">
        //                         水印检测与生成
        //                     </NavLink>
        //                 </li>
        //
        //                 <li className="nav-item">
        //                     <NavLink to="/entity" activeClassName="active" className="nav-links">
        //                         实体抽取
        //                     </NavLink>
        //                 </li>
        //                 <li className="nav-item user-dropdown">
        //                     {user ? (
        //                         <>
        //                     <span className="nav-links dropdown-toggle" role="button">
        //                         {user},你好！
        //                     </span>
        //                             <div className="dropdown-content">
        //                                 {/*<NavLink to="/usercenter" activeClassName="active" className="dropdown-item">*/}
        //                                 {/*    用户中心*/}
        //                                 {/*</NavLink>*/}
        //                                 <button onClick={handleLogout} className="dropdown-item">
        //                                     登出
        //                                 </button>
        //                             </div>
        //                         </>
        //                     ) : (
        //                         <>
        //                     <span className="nav-links dropdown-toggle" role="button">
        //                         账户
        //                     </span>
        //                             <div className="dropdown-content">
        //                                 <NavLink to="/login" activeClassName="active" className="dropdown-item">
        //                                     登录
        //                                 </NavLink>
        //                                 <NavLink to="/register" activeClassName="active" className="dropdown-item">
        //                                     注册
        //                                 </NavLink>
        //                             </div>
        //                         </>
        //                     )}
        //                 </li>
        //             </ul>
        //         </div>
        //     </nav>
    );
}

export default Navbar;
