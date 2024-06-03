import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import './Form.css'; // Import the CSS file

const Login = () => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const navigate = useNavigate();

    const handleLogin = async (e) => {
        e.preventDefault();
        setError(''); // Reset errors
        if (!username || !password) {
            setError('Please fill in all fields.');
            return;
        }
        try {
            const response = await axios.post('http://127.0.0.1:8001/login', {
                username: username,
                password: password
            });
            // Save the token and handle further authenticated requests
            localStorage.setItem('token', response.data.token);
            navigate('/graph-comparison'); // Redirect to GraphComparison page after successful login
        } catch (error) {
            setError(error.response?.data.detail || 'Unknown error');
        }
    };

    return (
        <div className="container">
            <h2>Login</h2>
            <form onSubmit={handleLogin}>
                <div className="form-group">
                    <label>Username:</label>
                    <input type="text" value={username} onChange={(e) => setUsername(e.target.value)} />
                </div>
                <div className="form-group">
                    <label>Password:</label>
                    <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} />
                </div>
                <button type="submit">Login</button>
                {error && <p className="error-message">{error}</p>}
            </form>
        </div>
    );
};

export default Login;
