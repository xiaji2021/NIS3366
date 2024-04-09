import React, { useState } from 'react';
import {useNavigate } from "react-router-dom";

function RegisterForm() {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [email, setEmail] = useState('');
    const navigate = useNavigate();

    const handleRegister = async (event) => {
        event.preventDefault();
// 检查是否所有必填字段都已填写
        if (!username || !password || !email) {
            alert('请填写所有必填字段');
            return;
        }

        // 检查邮箱格式
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(email)) {
            alert('请输入有效的邮箱地址');
            return;
        }

        // 检查密码强度，例如最小长度、包含数字和字母等
        // 这里假设密码长度至少为8，且必须包含数字和字母
        const passwordRegex = /^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$/;
        if (!passwordRegex.test(password)) {
            alert('密码不符合要求。请确保密码长度至少为8个字符，并包含数字和字母。');
            return;
        }

        try {
            const response = await fetch('http://39.107.60.129:8888/api/register', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ username, password, email })
            });

            const data = await response.json();
            if (response.ok) {
                console.log('注册成功:', data);
                navigate('/login');

            } else {
                alert(data.message);
            }
        } catch (error) {
            alert('请求发送失败');
        }
    };

    return (<form onSubmit={handleRegister} className="my-5">
            <div className="row justify-content-center">
                <div className="col-md-4">
                    <div className="card">
                        <h5 className="card-header text-center">注册账号</h5>
                        <div className="card-body">
                            <div className="mb-3">
                                <label htmlFor="username" className="form-label">用户名:</label>
                                <input
                                    type="text"
                                    className="form-control"
                                    id="username"
                                    value={username}
                                    onChange={(e) => setUsername(e.target.value)}
                                    placeholder="请输入用户名"
                                    required
                                />
                            </div>
                            <div className="mb-3">
                                <label htmlFor="password" className="form-label">密码:</label>
                                <input
                                    type="password"
                                    className="form-control"
                                    id="password"
                                    value={password}
                                    onChange={(e) => setPassword(e.target.value)}
                                    placeholder="请输入密码"
                                    required
                                />
                            </div>
                            <div className="mb-3">
                                <label htmlFor="email" className="form-label">邮箱:</label>
                                <input
                                    type="email"
                                    className="form-control"
                                    id="email"
                                    value={email}
                                    onChange={(e) => setEmail(e.target.value)}
                                    placeholder="请输入邮箱地址"
                                    required
                                />
                            </div>
                            <button type="submit" className="btn btn-primary w-100">注册</button>
                        </div>
                    </div>
                </div>
            </div>
        </form>

    );
}

export default RegisterForm;
