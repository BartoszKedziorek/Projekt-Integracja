import React from 'react';
import { Route, Navigate } from 'react-router-dom';

const ProtectedRoute = ({ element: Component, isLoggedIn, ...rest }) => {
    return (
        <Route
            {...rest}
            element={
                isLoggedIn ? (
                    <Component {...rest} />
                ) : (
                    <Navigate to="/login" />
                )
            }
        />
    );
};

export default ProtectedRoute;
