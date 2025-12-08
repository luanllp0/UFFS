import React, { useContext } from "react";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { AuthProvider, AuthContext } from "./context/AuthContext";
import { CssBaseline, AppBar, Toolbar, Typography, Box } from "@mui/material";

import LoginPage from "./components/LoginPage";
import MenuLateral from "./components/MenuLateral";

import PaginaClientes from "./pages/PaginaClientes";
import PaginaCaminhoes from "./pages/PaginaCaminhoes";
import PaginaServicos from "./pages/PaginaServicos";
import PaginaDashboard from "./pages/PaginaDashboard";

function RotaPrivada({ children }) {
  const { signed, loading } = useContext(AuthContext);

  if (loading) return <div>Carregando...</div>;

  return signed ? children : <Navigate to="/login" />;
}

function RotaAdmin({ children }) {
  const { user, loading } = useContext(AuthContext);

  if (loading) return <div>Carregando...</div>;

  if (user?.tipo !== "Colaborador Interno" && user?.tipo !== "admin") {
    return (
      <div style={{ padding: 40, textAlign: "center" }}>
        <Typography variant="h5" color="error">
          ⛔ Acesso Negado
        </Typography>
        <Typography>
          Você não tem permissão para acessar esta página.
        </Typography>
      </div>
    );
  }

  return children;
}

function LayoutDoSistema({ children }) {
  const { user } = useContext(AuthContext);
  return (
    <Box sx={{ display: "flex" }}>
      <AppBar
        position="fixed"
        sx={{ zIndex: (theme) => theme.zIndex.drawer + 1 }}
      >
        <Toolbar>
          <Typography variant="h6" noWrap component="div">
            Sistema Rodofrio - {user?.nome} ({user?.tipo})
          </Typography>
        </Toolbar>
      </AppBar>
      <MenuLateral>{children}</MenuLateral>
    </Box>
  );
}

function AppRoutes() {
  const { signed } = useContext(AuthContext);

  return (
    <Routes>
      <Route
        path="/login"
        element={signed ? <Navigate to="/" /> : <LoginPage />}
      />

      <Route
        path="/"
        element={
          <RotaPrivada>
            <LayoutDoSistema>
              <PaginaDashboard />
            </LayoutDoSistema>
          </RotaPrivada>
        }
      />

      <Route
        path="/clientes"
        element={
          <RotaPrivada>
            <RotaAdmin>
              <LayoutDoSistema>
                <PaginaClientes />
              </LayoutDoSistema>
            </RotaAdmin>
          </RotaPrivada>
        }
      />

      <Route
        path="/caminhoes"
        element={
          <RotaPrivada>
            <RotaAdmin>
              <LayoutDoSistema>
                <PaginaCaminhoes />
              </LayoutDoSistema>
            </RotaAdmin>
          </RotaPrivada>
        }
      />

      <Route
        path="/servicos"
        element={
          <RotaPrivada>
            <LayoutDoSistema>
              <PaginaServicos />
            </LayoutDoSistema>
          </RotaPrivada>
        }
      />
    </Routes>
  );
}

function App() {
  return (
    <AuthProvider>
      <CssBaseline />
      <BrowserRouter>
        <AppRoutes />
      </BrowserRouter>
    </AuthProvider>
  );
}

export default App;
