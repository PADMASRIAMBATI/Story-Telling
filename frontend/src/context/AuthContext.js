import React, { createContext, useContext, useState, useEffect } from 'react';
import { getToken, getUser, setAuth, clearAuth, isAuthenticated } from '../services/auth';

const AuthContext = createContext();

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = getToken();
    const userData = getUser();
    
    if (token && userData) {
      setUser(userData);
    }
    setLoading(false);
  }, []);

  const login = (token, userData) => {
    setAuth(token, userData);
    setUser(userData);
  };

  const logout = () => {
    clearAuth();
    setUser(null);
  };

  const value = {
    user,
    login,
    logout,
    isAuthenticated: isAuthenticated(),
    loading
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};