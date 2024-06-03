import React from 'react';
import { useNavigate } from 'react-router-dom';

const Logout = () => {
    const navigate = useNavigate();

    const handleLogout = () => {
        // Usuwanie tokena po wylogowaniu
        localStorage.removeItem('token');
        // Przekierowanie użytkownika na stronę logowania
        navigate('/login');
    };

    return (
        <div>
            <button onClick={handleLogout}>Logout</button>
        </div>
    );
};

export default Logout;
