import React, { useState, useContext } from "react";
import { AuthContext } from "../context/AuthContext";
import {
  Container,
  Paper,
  TextField,
  Button,
  Typography,
  Box,
} from "@mui/material";

function LoginPage() {
  const { login } = useContext(AuthContext);
  const [email, setEmail] = useState("");
  const [senha, setSenha] = useState("");

  async function handleLogin(e) {
    e.preventDefault();
    try {
      await login(email, senha);
    } catch (error) {
      alert("Erro no login! Verifique email e senha.");
    }
  }

  return (
    <Container maxWidth="xs" sx={{ mt: 15 }}>
      <Paper
        elevation={3}
        sx={{
          p: 4,
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
        }}
      >
        <Typography
          component="h1"
          variant="h5"
          sx={{ mb: 3, fontWeight: "bold", color: "#1976d2" }}
        >
          Rodofrio Login
        </Typography>
        <Box component="form" onSubmit={handleLogin} sx={{ width: "100%" }}>
          <TextField
            label="Email / Login"
            fullWidth
            margin="normal"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
          <TextField
            label="Senha"
            type="password"
            fullWidth
            margin="normal"
            value={senha}
            onChange={(e) => setSenha(e.target.value)}
            required
          />
          <Button
            type="submit"
            fullWidth
            variant="contained"
            sx={{ mt: 3, mb: 2, height: 50 }}
          >
            Entrar no Sistema
          </Button>
        </Box>
      </Paper>
    </Container>
  );
}

export default LoginPage;
