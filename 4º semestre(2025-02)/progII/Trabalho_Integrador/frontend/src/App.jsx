import React from 'react';
import { CssBaseline, Container, Box, Typography, Divider, Grid } from '@mui/material';

import ListaClientes from './components/ListaClientes';
import CadastrarCliente from './components/CadastraClientes';

import ListaCaminhoes from './components/ListaCaminhoes';
import CadastrarCaminhao from './components/CadastraCaminhoes';

function App() {
  return (
    <>
      <CssBaseline />
      <Container maxWidth="lg" sx={{ mb: 8 }}>
        <Typography
          variant="h3"
          align="center"
          sx={{ my: 4, fontWeight: "bold", color: "#1976d2" }}
        >
          Sistema Rodofrio
        </Typography>

        <Typography variant="h5" sx={{ mt: 4, mb: 2 }}>
          1. Gestão de Clientes
        </Typography>
        <Grid container spacing={4}>
          <Grid item xs={12} md={4}>
            <CadastrarCliente />
          </Grid>
          <Grid item xs={12} md={8}>
            <ListaClientes />
          </Grid>
        </Grid>

        <Divider sx={{ my: 6 }} />

        <Typography variant="h5" sx={{ mt: 4, mb: 2 }}>
          2. Gestão de Caminhões
        </Typography>
        <Grid container spacing={4}>
          <Grid item xs={12} md={4}>
            <CadastrarCaminhao />
          </Grid>
          <Grid item xs={12} md={8}>
            <ListaCaminhoes />
          </Grid>
        </Grid>
      </Container>
    </>
  );
}

export default App;