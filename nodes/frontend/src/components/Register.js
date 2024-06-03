import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import './Form.css'; // Import the CSS file

const Register = () => {
    const [formData, setFormData] = useState({
        username: '',
        first_name: '',
        last_name: '',
        email: '',
        password: '',
        password2: ''
    });
    const [message, setMessage] = useState('');
    const [error, setError] = useState('');
    const navigate = useNavigate();

    const handleChange = (e) => {
        setFormData({
            ...formData,
            [e.target.name]: e.target.value
        });
    };

    const handleRegister = async (e) => {
        e.preventDefault();
        const { username, first_name, last_name, email, password, password2 } = formData;
        setError(''); // Reset errors
        setMessage(''); // Reset messages
        if (password !== password2) {
            setError("Passwords do not match");
            return;
        }
        try {
            const response = await axios.post('http://127.0.0.1:8001/register', {
                username,
                first_name,
                last_name,
                email,
                password,
                password2
            });
            setMessage('Registered successfully');
            setTimeout(() => {
                navigate('/login'); // Redirect to login page after successful registration
            }, 2000); // Redirect to homepage after 2 seconds
        } catch (error) {
            setError('Registration failed: ' + (error.response?.data.detail || 'Unknown error'));
        }
    };

    return (
        <div className="container">
            <h2>Register</h2>
            <form onSubmit={handleRegister}>
                <div className="form-group">
                    <label>Username:</label>
                    <input 
                        type="text" 
                        name="username" 
                        value={formData.username} 
                        onChange={handleChange}
                        className={error ? 'input-error' : ''}
                    />
                </div>
                <div className="form-group">
                    <label>First Name:</label>
                    <input 
                        type="text" 
                        name="first_name" 
                        value={formData.first_name} 
                        onChange={handleChange}
                        className={error ? 'input-error' : ''}
                    />
                </div>
                <div className="form-group">
                    <label>Last Name:</label>
                    <input 
                        type="text" 
                        name="last_name" 
                        value={formData.last_name} 
                        onChange={handleChange}
                        className={error ? 'input-error' : ''}
                    />
                </div>
                <div className="form-group">
                    <label>Email:</label>
                    <input 
                        type="email" 
                        name="email" 
                        value={formData.email} 
                        onChange={handleChange}
                        className={error ? 'input-error' : ''}
                    />
                </div>
                <div className="form-group">
                    <label>Password:</label>
                    <input 
                        type="password" 
                        name="password" 
                        value={formData.password} 
                        onChange={handleChange}
                        className={error ? 'input-error' : ''}
                    />
                </div>
                <div className="form-group">
                    <label>Confirm Password:</label>
                    <input 
                        type="password" 
                        name="password2" 
                        value={formData.password2} 
                        onChange={handleChange}
                        className={error ? 'input-error' : ''}
                    />
                </div>
                <button type="submit">Register</button>
                {message && <p className="success-message">{message}</p>}
                {error && <p className="error-message">{error}</p>}
            </form>
        </div>
    );
};

export default Register;
