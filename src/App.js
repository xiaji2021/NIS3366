import React, { createContext, useContext, useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate, Outlet } from 'react-router-dom';
import Navbar from './components/Navbar/Navbar';
import ImageGenerator from './views/T2I/ImageGenerator';
import ImageUploader from "./views/WaterMark/WaterMark";
import LoginForm from "./views/Login/Login";
import Entity from "./views/Entity/Entity";
import RegisterForm from "./views/Login/Register";

import AuthContext from './AuthContext';
const useAuth = () => {
    return useContext(AuthContext);
};

const RequireAuth = ({ children }) => {
    const auth = useAuth();
    if (!auth.user) {
        // 用户未登录，重定向至登录页面
        return <Navigate to="/login" />;
    }
    return children; // 用户已登录，渲染对应的组件
};

function App() {
    const [user, setUser] = useState(null);
    const login = (username) => {
        setUser({ username });
    };
    const logout = () => {
        setUser(null);
    };

    return (
        <AuthContext.Provider value={{ user, login, logout }}>
            <Router>
                <Navbar />
                <Routes>

                    <Route path="/login" element={<LoginForm />} />
                    <Route path="/register" element={<RegisterForm />} />
                    {/* 使用 RequireAuth 来包裹需要认证的组件 */}
                    <Route element={<RequireAuth />}>
                        <Route path="/" element={<ImageGenerator />} />
                        <Route path="/watermark" element={<ImageUploader />} />
                        <Route path="/image-generator" element={<ImageGenerator />} />
                        <Route path="/entity" element={<Entity />} />
                    </Route>
                </Routes>
            </Router>
        </AuthContext.Provider>
    );
}

export default App;



// import React, { createContext, useContext, useState } from 'react';
// import { BrowserRouter as Router, Route, Routes,Redirect } from 'react-router-dom';
// import Navbar from './components/Navbar/Navbar';
// import ImageGenerator from './views/T2I/ImageGenerator';
// import ImageUploader from "./views/WaterMark/WaterMark";
// import LoginForm from "./views/Login/Login";
// import Entity from "./views/Entity/Entity";
// import RegisterForm from "./views/Login/Register";
// const AuthContext = createContext(null);
// const useAuth = () => {
//     return useContext(AuthContext);
// };
//
// const PrivateRoute = ({ component: Component, ...rest }) => {
//     const auth = useAuth();
//     return (
//         <Route
//             {...rest}
//             render={(props) =>
//                 auth.user ? (
//                     <Component {...props} />
//                 ) : (
//                     <Redirect to={{ pathname: "/login" }} />
//                 )
//             }
//         />
//     );
// };
//
// function App() {
//     const [user, setUser] = useState(null);
//     const login = (username) => {
//         // 假设登录成功并设置 user
//         setUser({ username });
//     };
//     const logout = () => {
//         setUser(null);
//     };
//     return (
//         <AuthContext.Provider value={{ user, login, logout }}>
//       <Router>
//       <div>
//           <Navbar />
//           <Routes>
//               <PrivateRoute path="/watermark" element={<ImageUploader />} />
//               <PrivateRoute path="/image-generator" element={<ImageGenerator />} />
//               <PrivateRoute path="/entity" element={<Entity />} />
//               <PrivateRoute path="/" element={<ImageGenerator />} />
//               <Route path="/login" component={LoginForm} />
//               <Route path="/register" component={RegisterForm} />
//           </Routes>
//       </div>
//       </Router>
//         </AuthContext.Provider>
//
//     );
// }
// export default App;