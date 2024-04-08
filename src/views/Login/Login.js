import React, {useContext, useState} from 'react';
import AuthContext from "../../AuthContext"
import { useNavigate } from 'react-router-dom';

function LoginForm() {

    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const {login} = useContext(AuthContext);
    const navigate = useNavigate();

    const handleLogin = async (event) => {
        event.preventDefault(); // 阻止表单默认提交行为
        try {
            const response = await fetch('http://47.103.101.128:8888/api/login', { // 这里应该是你的登录 API URL
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ username, password })
            });

            if (response.ok) {
                const data = await response.json();

                console.log('登录成功:', data);
                login(username);
                navigate('/'); // 导航至应用的主页

            } else {
                // 处理错误，例如显示错误消息
                const error = await response.json();
                alert(error.message);
            }
        } catch (error) {
            // 处理请求发送失败
            alert('请求发送失败');
        }
    };

    return (
        <form onSubmit={handleLogin} className="mt-5">
            <div className="row justify-content-center">
                <div className="col-md-4"> {/* 你可以根据需要调整 col-md-4 这个值 */}
                    <div className="card">
                        <div className="card-header text-center">
                            <h3>登录</h3>
                        </div>
                        <div className="card-body">
                            <div className="form-group">
                                <label htmlFor="username">用户名:</label>
                                <input
                                    type="text"
                                    className="form-control"
                                    id="username"
                                    value={username}
                                    onChange={(e) => setUsername(e.target.value)}
                                    placeholder="请输入用户名"
                                />
                            </div>
                            <div className="form-group">
                                <label htmlFor="password">密码:</label>
                                <input
                                    type="password"
                                    className="form-control"
                                    id="password"
                                    value={password}
                                    onChange={(e) => setPassword(e.target.value)}
                                    placeholder="请输入密码"
                                />
                            </div>
                            <button type="submit" className="btn btn-primary btn-block">登录</button>
                        </div>
                    </div>
                </div>
            </div>
        </form>


    );
}

export default LoginForm;
