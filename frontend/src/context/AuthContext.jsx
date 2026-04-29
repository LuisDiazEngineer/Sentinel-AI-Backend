import React, { createContext, useState, useContext } from 'react';

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
    // Usamos funciones para que SOLO lean el storage al cargar la página
    const [token, setToken] = useState(() => {
        const saved = localStorage.getItem('token');
        return (saved && saved !== "undefined") ? saved : null;
    });

    const [isAuthenticated, setIsAuthenticated] = useState(() => {
        const saved = localStorage.getItem('token');
        return !!saved && saved !== "undefined";
    });
    const login = (newToken) => {
        if (!newToken) return;
        localStorage.setItem('token', newToken);
        setToken(newToken);
        setIsAuthenticated(true);
    };

    const logout = () => {
        localStorage.removeItem('token');
        setToken(null);
        setIsAuthenticated(false);
        localStorage.clear();
        // Opcional: Redirigir al inicio para limpiar el estado visual
        window.location.href = '/';
    };

    return (
        <AuthContext.Provider value={{ token, isAuthenticated, login, logout }}>
            {children}
        </AuthContext.Provider>
    );
};

export const useAuth = () => {
    return useContext(AuthContext);
};
