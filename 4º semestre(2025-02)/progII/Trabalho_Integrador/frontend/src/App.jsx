import React from 'react';
import ListaClientes from './components/ListaClientes';
import CadastrarCliente from './components/CadastraClientes'; // <--- Importamos o novo
import { CssBaseline, Container, Box } from '@mui/material';

function App() {
  return (
    <>
      <CssBaseline />
      <Container maxWidth="md" sx={{ mb: 4 }}>
        
        <Box sx={{ my: 4 }}>
            <CadastrarCliente />
        </Box>

        <Box sx={{ my: 4 }}>
            <ListaClientes />
        </Box>

      </Container>
    </>
  );
}

export default App;