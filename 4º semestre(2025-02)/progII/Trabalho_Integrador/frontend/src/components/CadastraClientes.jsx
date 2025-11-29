import React, { useState } from 'react';
import api from '../services/api';
import { Box, TextField, Button, Typography, Paper } from '@mui/material';

function CadastrarCliente() {
    const [nome, setNome] = useState('');
    const [telefone, setTelefone] = useState('');
    const [email, setEmail] = useState('');

    async function acaoBotao(e) {
        e.preventDefault();

        try {
            await api.post('/clientes', { nome, telefone, email });
            alert('Cliente cadastrado com sucesso!');
            setNome('');
            setTelefone('');
            setEmail('');
        } catch (error) {
            alert('Erro ao cadastrar');
        }
    }

    return (
        <Paper elevation={3} sx={{ p: 4, mt: 4, maxWidth: 500, mx: 'auto' }}>
            <Typography variant="h5" gutterBottom>Novo Cliente</Typography>
            
            <Box component="form" onSubmit={acaoBotao} sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
                
                <TextField 
                    label="Nome Completo" 
                    variant="outlined"
                    value={nome}
                    onChange={(e) => setNome(e.target.value)}
                    required
                />

                <TextField 
                    label="Telefone" 
                    variant="outlined"
                    value={telefone}
                    onChange={(e) => setTelefone(e.target.value)}
                    required
                />

                <TextField 
                    label="E-mail" 
                    variant="outlined"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    required
                />

                <Button type="submit" variant="contained" size="large">
                    Salvar Cliente
                </Button>
            </Box>
        </Paper>
    );
}

export default CadastrarCliente;