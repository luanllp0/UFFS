import React, { useContext } from 'react';
import { AuthProvider, AuthContext } from './context/AuthContext';
import { CssBaseline, Container, Box, Typography, Divider, Grid, Button, AppBar, Toolbar } from '@mui/material';

import ListaClientes from './components/ListaClientes';
import CadastrarCliente from './components/CadastraClientes';
import ListaCaminhoes from './components/ListaCaminhoes';
import CadastrarCaminhao from './components/CadastraCaminhoes';
import ListaServicos from './components/ListaServicos';
import CadastrarServico from './components/CadastrarServico';
import LoginPage from './components/LoginPage';

function ConteudoDoSistema() {
    const { logout, user } = useContext(AuthContext);

    return (
        <>
            <AppBar position="static">
                <Toolbar>
                    <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
                        Sistema Rodofrio - Olá, {user?.nome}
                    </Typography>
                    <Button color="inherit" onClick={logout}>Sair</Button>
                </Toolbar>
            </AppBar>

            <Container maxWidth="lg" sx={{ mb: 8 }}>
                
                <Typography variant="h5" sx={{ mt: 4, mb: 2 }}>1. Gestão de Clientes</Typography>
                <Grid container spacing={4}>
                    <Grid item xs={12} md={4}><CadastrarCliente /></Grid>
                    <Grid item xs={12} md={8}><ListaClientes /></Grid>
                </Grid>

                <Divider sx={{ my: 6 }} />

                <Typography variant="h5" sx={{ mt: 4, mb: 2 }}>2. Gestão de Caminhões</Typography>
                <Grid container spacing={4}>
                    <Grid item xs={12} md={4}><CadastrarCaminhao /></Grid>
                    <Grid item xs={12} md={8}><ListaCaminhoes /></Grid>
                </Grid>

                <Divider sx={{ my: 6 }} />

                <Typography variant="h5" sx={{ mt: 4, mb: 2 }}>3. Ordens de Serviço</Typography>
                <Box sx={{ my: 4 }}>
                    <CadastrarServico /> 
                    <Box sx={{ mt: 4 }}>
                        <ListaServicos />
                    </Box>
                </Box>

            </Container>
        </>
    );
}

function Routes() {
    const { signed } = useContext(AuthContext);
    return signed ? <ConteudoDoSistema /> : <LoginPage />;
}

function App() {
  return (
    <AuthProvider>
      <CssBaseline />
      <Routes />
    </AuthProvider>
  );
}

export default App;