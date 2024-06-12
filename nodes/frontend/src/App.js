import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Route, Routes, Link, Navigate } from 'react-router-dom';
import Login from './components/Login';
import Register from './components/Register';
import GraphComparison from './components/GraphComparison';
import './App.css';

const App = () => {
    const [isLoggedIn, setIsLoggedIn] = useState(false);

    useEffect(() => {
        const token = localStorage.getItem('token');
        if (token) {
            setIsLoggedIn(true);
        }
    }, []);

    const handleLogout = () => {
        localStorage.removeItem('token');
        setIsLoggedIn(false);
    };

    return (
        <Router>
            <nav className="top-nav">
                <ul>
                    <li><Link to="/"><button>Home</button></Link></li>
                    {!isLoggedIn && <li><Link to="/login"><button>Login</button></Link></li>}
                    {!isLoggedIn && <li><Link to="/register"><button>Registration</button></Link></li>}
                    {isLoggedIn && <li><Link to="/graph-comparison"><button>Compare Graphs</button></Link></li>}
                    {isLoggedIn && <li><button onClick={handleLogout}>Logout</button></li>}
                </ul>
            </nav>
            <div className="container">
                <h1>Projekt zaliczeniowy z przedmiotu: Integracja systemów</h1>
                <h2>Backend: Bartosz Kędziorek</h2>
                <h2>Frontend: Eryk Kołodziejczyk</h2>
                <h1>Temat: Porównanie poziomu dostępu do internetu - łącz szerokopasmowych w stosunku do liczby mieszkańców i poziomu bezrobocia w państwach świata </h1>
                <Routes>
                    <Route path="/login" element={<Login />} />
                    <Route path="/register" element={<Register />} />
                    <Route path="/graph-comparison" element={isLoggedIn ? <GraphComparison /> : <Navigate to="/graph-comparison" />} />
                </Routes>
            </div>
        </Router>
    );
};

export default App;
