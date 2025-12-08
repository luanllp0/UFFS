import React, { createContext, useState, useEffect } from "react";
import api from "../services/api";

export const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const storagedUser = localStorage.getItem("user");
    const storagedToken = localStorage.getItem("token");

    if (storagedUser && storagedToken) {
      setUser(JSON.parse(storagedUser));
      api.defaults.headers.Authorization = `Bearer ${storagedToken}`;
    }
    setLoading(false);
  }, []);

  async function login(email, senha) {
    const response = await api.post("/login", { email, senha });

    setUser(response.data.user);
    api.defaults.headers.Authorization = `Bearer ${response.data.token}`;

    localStorage.setItem("user", JSON.stringify(response.data.user));
    localStorage.setItem("token", response.data.token);
  }

  function logout() {
    setUser(null);
    localStorage.removeItem("user");
    localStorage.removeItem("token");
  }

  return (
    <AuthContext.Provider
      value={{ signed: !!user, user, loading, login, logout }}
    >
      {children}
    </AuthContext.Provider>
  );
};
